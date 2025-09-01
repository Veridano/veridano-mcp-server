# Veridano Troubleshooting Guide

## Common Issues and Solutions

### Authentication Problems

#### Issue: "Authentication required" error
```
Error: Authentication required - invalid or missing credentials
```

**Solution:**
1. Verify environment variables are set:
   ```bash
   echo $VERIDANO_CLIENT_ID
   echo $VERIDANO_CLIENT_SECRET
   echo $VERIDANO_ENDPOINT
   ```

2. Test credentials manually:
   ```python
   import os
   print("Client ID:", os.getenv('VERIDANO_CLIENT_ID'))
   print("Endpoint:", os.getenv('VERIDANO_ENDPOINT'))
   # Never print client secret in logs
   print("Secret set:", bool(os.getenv('VERIDANO_CLIENT_SECRET')))
   ```

3. Verify AWS Cognito client is active:
   ```bash
   aws cognito-idp describe-user-pool-client \
     --user-pool-id us-east-1_HgeKuWISD \
     --client-id YOUR_CLIENT_ID
   ```

#### Issue: "Token expired" error
```
Error: The provided token has expired
```

**Solution:**
MCP clients should handle token refresh automatically. If not:

```python
async def refresh_connection():
    """Force connection refresh"""
    await client.disconnect()
    await client.connect()
    
    # Test connection
    health = await client.health_check()
    print(f"Refreshed connection: {health['status']}")
```

### Network Connectivity Issues

#### Issue: Connection timeouts
```
Error: Timeout connecting to https://api.veridano.com/mcp
```

**Diagnosis:**
```bash
# Test basic connectivity
curl -I https://api.veridano.com/mcp

# Check DNS resolution
nslookup api.veridano.com

# Test from your exact environment
python -c "
import requests
try:
    r = requests.get('https://api.veridano.com/mcp', timeout=10)
    print(f'Status: {r.status_code}')
except Exception as e:
    print(f'Error: {e}')
"
```

**Solutions:**
1. **Corporate Firewall**: Add `*.veridano.com` to firewall allowlist
2. **Proxy Configuration**: Set HTTP_PROXY and HTTPS_PROXY if needed
3. **Region Issues**: Ensure you're connecting to `us-east-1` region
4. **Timeout Adjustment**: Increase client timeout to 30+ seconds

#### Issue: SSL/TLS certificate errors
```
Error: SSL certificate verification failed
```

**Solution:**
```python
# Temporary workaround (not recommended for production)
import ssl
client = VeridanoMCPClient(
    ssl_context=ssl.create_default_context()
)

# Better solution - update certificates
pip install --upgrade certifi requests
```

### Query Issues

#### Issue: No search results returned
```json
{
  "documents": [],
  "total_results": 0
}
```

**Diagnosis Steps:**
1. **Check query relevance**:
   ```python
   # Test with known good query
   result = await client.semantic_search(
       query="ransomware attack vectors",
       sources=["CISA"],
       min_score=0.5  # Lower threshold for testing
   )
   ```

2. **Verify data sources**:
   ```python
   # Check available sources
   tools = await client.list_tools()
   print("Available tools:", [t['name'] for t in tools])
   ```

3. **Test different parameters**:
   ```python
   # Broader search
   result = await client.semantic_search(
       query="cybersecurity",  # Generic query
       top_k=50,               # More results
       min_score=0.3           # Lower threshold
   )
   ```

**Common Causes:**
- Query too specific for available data
- Similarity threshold too high (`min_score > 0.9`)
- Source filter excluding relevant data
- Typos in query or source names

#### Issue: Slow query performance
```
Query taking > 2 seconds to complete
```

**Optimization Steps:**
1. **Use source filtering**:
   ```python
   # ✅ Fast - specific sources
   result = await client.semantic_search(
       query="CVE-2024-38063",
       sources=["NVD", "CISA"]  # Only 2 sources
   )
   
   # ❌ Slow - all sources
   result = await client.semantic_search(
       query="CVE-2024-38063"  # Searches all 11 sources
   )
   ```

2. **Reduce result size**:
   ```python
   # ✅ Fast - focused results
   result = await client.semantic_search(
       query="threat intelligence",
       top_k=10  # Small result set
   )
   
   # ❌ Slow - large result set
   result = await client.semantic_search(
       query="threat intelligence", 
       top_k=100  # Large result set
   )
   ```

3. **Check database performance**:
   ```python
   import time
   
   start = time.time()
   result = await client.semantic_search(query="test", top_k=1)
   db_time = time.time() - start
   
   print(f"Database response time: {db_time:.3f}s")
   # Healthy: < 0.5s, Degraded: 0.5-2s, Unhealthy: > 2s
   ```

### Rate Limiting Issues

#### Issue: "Rate limit exceeded" error
```
Error: Rate limit exceeded - 200 requests per second limit reached
```

**Solutions:**
1. **Implement exponential backoff**:
   ```python
   import asyncio
   import random
   
   async def resilient_search(query: str, max_retries: int = 3):
       for attempt in range(max_retries):
           try:
               return await client.semantic_search(query=query)
           except RateLimitError as e:
               if attempt == max_retries - 1:
                   raise
               
               delay = (2 ** attempt) + random.uniform(0, 1)
               print(f"Rate limited - waiting {delay:.1f}s")
               await asyncio.sleep(delay)
   ```

2. **Implement client-side rate limiting**:
   ```python
   import asyncio
   from collections import deque
   
   class RateLimiter:
       def __init__(self, max_requests: int, time_window: int):
           self.max_requests = max_requests
           self.time_window = time_window
           self.requests = deque()
       
       async def acquire(self):
           now = time.time()
           
           # Remove old requests outside time window
           while self.requests and self.requests[0] <= now - self.time_window:
               self.requests.popleft()
           
           # Check if we can make a request
           if len(self.requests) >= self.max_requests:
               sleep_time = self.time_window - (now - self.requests[0])
               await asyncio.sleep(sleep_time + 0.1)
           
           self.requests.append(now)
   
   # Usage
   limiter = RateLimiter(max_requests=50, time_window=60)  # 50 req/min
   
   async def rate_limited_search(query: str):
       await limiter.acquire()
       return await client.semantic_search(query=query)
   ```

### Data Quality Issues

#### Issue: Irrelevant search results
```json
{
  "documents": [
    {"title": "Unrelated document", "score": 0.4}
  ]
}
```

**Solutions:**
1. **Increase similarity threshold**:
   ```python
   result = await client.semantic_search(
       query="specific threat actor APT29",
       min_score=0.8  # Higher threshold for precision
   )
   ```

2. **Use more specific queries**:
   ```python
   # ✅ Specific
   "APT29 Cozy Bear tactics techniques procedures Windows"
   
   # ❌ Vague  
   "cybersecurity threats"
   ```

3. **Combine with source filtering**:
   ```python
   result = await client.semantic_search(
       query="Log4Shell vulnerability",
       sources=["CISA", "NIST"],  # Authoritative sources
       min_score=0.75
   )
   ```

#### Issue: Missing recent intelligence
```
Expected recent threat intelligence but only getting old documents
```

**Solutions:**
1. **Use timeframe filtering**:
   ```python
   result = await client.semantic_search(
       query="ransomware campaign 2025",
       timeframe="last_30_days",
       sources=["CISA", "FBI", "US-CERT"]
   )
   ```

2. **Check data ingestion status**:
   ```python
   # Check when sources were last updated
   health = await client.health_check()
   print("Last data update:", health.get("last_data_update"))
   ```

### Performance Issues

#### Issue: High memory usage
```
Agent consuming excessive memory during batch processing
```

**Solutions:**
1. **Process in smaller batches**:
   ```python
   async def memory_efficient_batch(indicators: List[str]):
       batch_size = 10  # Smaller batches
       results = []
       
       for i in range(0, len(indicators), batch_size):
           batch = indicators[i:i + batch_size]
           batch_results = await process_batch(batch)
           results.extend(batch_results)
           
           # Force garbage collection between batches
           import gc
           gc.collect()
       
       return results
   ```

2. **Use streaming for large result sets**:
   ```python
   async def stream_results(query: str):
       """Stream results instead of loading all at once"""
       
       async for document in client.stream_search(query=query):
           yield document  # Process one at a time
   ```

#### Issue: Agent crashes under load
```
Agent terminates unexpectedly during high-volume operations
```

**Solutions:**
1. **Implement circuit breaker**:
   ```python
   class CircuitBreaker:
       def __init__(self, failure_threshold=5, timeout=60):
           self.failure_threshold = failure_threshold
           self.timeout = timeout
           self.failure_count = 0
           self.last_failure_time = None
           self.state = "CLOSED"
       
       async def call(self, func, *args, **kwargs):
           if self.state == "OPEN":
               if time.time() - self.last_failure_time > self.timeout:
                   self.state = "HALF_OPEN"
               else:
                   raise Exception("Circuit breaker is OPEN")
           
           try:
               result = await func(*args, **kwargs)
               if self.state == "HALF_OPEN":
                   self.state = "CLOSED"
               self.failure_count = 0
               return result
               
           except Exception as e:
               self.failure_count += 1
               self.last_failure_time = time.time()
               
               if self.failure_count >= self.failure_threshold:
                   self.state = "OPEN"
               
               raise
   ```

2. **Add resource monitoring**:
   ```python
   import psutil
   import asyncio
   
   async def monitor_resources():
       """Monitor agent resource usage"""
       while True:
           memory_percent = psutil.virtual_memory().percent
           cpu_percent = psutil.cpu_percent()
           
           if memory_percent > 90:
               print(f"⚠️ High memory usage: {memory_percent}%")
           if cpu_percent > 90:
               print(f"⚠️ High CPU usage: {cpu_percent}%")
           
           await asyncio.sleep(30)
   ```

## Debugging Tools

### Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

client = VeridanoMCPClient(
    endpoint="https://api.veridano.com/mcp",
    debug=True,           # Enable debug output
    log_queries=True,     # Log all queries
    log_responses=True    # Log all responses
)
```

### Query Analysis
```python
async def analyze_query_performance(query: str):
    """Analyze why a query might be slow or failing"""
    
    print(f"🔍 Analyzing query: '{query}'")
    
    # Test with minimal parameters
    start = time.time()
    try:
        result = await client.semantic_search(
            query=query,
            top_k=1,
            min_score=0.1
        )
        basic_time = time.time() - start
        print(f"  Basic search: {basic_time:.3f}s - {result['total_results']} total available")
    except Exception as e:
        print(f"  Basic search failed: {e}")
        return
    
    # Test with source filtering
    for source in ["CISA", "FBI", "NIST"]:
        try:
            start = time.time()
            result = await client.semantic_search(
                query=query,
                sources=[source],
                top_k=5
            )
            source_time = time.time() - start
            print(f"  {source}: {source_time:.3f}s - {result['total_results']} results")
        except Exception as e:
            print(f"  {source} failed: {e}")
```

### Connection Diagnostics
```python
async def diagnose_connection():
    """Comprehensive connection diagnostics"""
    
    diagnostics = {
        "endpoint_reachable": False,
        "dns_resolution": False,
        "ssl_handshake": False,
        "authentication": False,
        "mcp_protocol": False
    }
    
    try:
        # Test 1: DNS resolution
        import socket
        socket.gethostbyname("api.veridano.com")
        diagnostics["dns_resolution"] = True
        print("✅ DNS resolution successful")
    except Exception as e:
        print(f"❌ DNS resolution failed: {e}")
    
    try:
        # Test 2: Basic HTTP connectivity
        import requests
        response = requests.get("https://api.veridano.com/health", timeout=10)
        diagnostics["endpoint_reachable"] = response.status_code < 500
        print(f"✅ Endpoint reachable: {response.status_code}")
    except Exception as e:
        print(f"❌ Endpoint unreachable: {e}")
    
    try:
        # Test 3: MCP protocol
        client = VeridanoMCPClient()
        await client.connect()
        diagnostics["authentication"] = True
        print("✅ Authentication successful")
        
        tools = await client.list_tools()
        diagnostics["mcp_protocol"] = len(tools) > 0
        print(f"✅ MCP protocol working: {len(tools)} tools available")
        
    except Exception as e:
        print(f"❌ MCP connection failed: {e}")
    
    return diagnostics
```

## Error Reference

### Authentication Errors

| Error Code | Description | Solution |
|------------|-------------|----------|
| `AUTH_REQUIRED` | Missing or invalid credentials | Check client ID and secret |
| `TOKEN_EXPIRED` | Authentication token expired | Refresh connection |
| `INVALID_CLIENT` | Client ID not found | Verify client ID in Cognito |
| `ACCESS_DENIED` | Insufficient permissions | Contact Veridano support |

### Query Errors

| Error Code | Description | Solution |
|------------|-------------|----------|
| `INVALID_QUERY` | Malformed query parameters | Validate query syntax |
| `QUERY_TOO_LONG` | Query exceeds length limits | Shorten query string |
| `INVALID_SOURCE` | Unknown data source specified | Check available sources |
| `SEARCH_TIMEOUT` | Query execution timeout | Simplify query or add source filter |

### Network Errors

| Error Code | Description | Solution |
|------------|-------------|----------|
| `CONNECTION_TIMEOUT` | Network timeout | Check connectivity, increase timeout |
| `DNS_RESOLUTION` | Cannot resolve hostname | Check DNS settings |
| `SSL_ERROR` | SSL/TLS handshake failed | Update certificates |
| `PROXY_ERROR` | Proxy configuration issue | Configure proxy settings |

### Rate Limiting Errors

| Error Code | Description | Solution |
|------------|-------------|----------|
| `QUOTA_EXCEEDED` | Rate limit exceeded | Implement backoff, reduce query rate |
| `BURST_LIMIT` | Burst capacity exceeded | Space out queries over time |
| `CONCURRENT_LIMIT` | Too many concurrent requests | Reduce concurrent operations |

## Performance Troubleshooting

### Slow Queries Checklist
- [ ] **Query specificity**: Is the query specific enough?
- [ ] **Source filtering**: Are you filtering to relevant sources?
- [ ] **Result size**: Are you requesting only needed results?
- [ ] **Similarity threshold**: Is min_score appropriate (0.6-0.8)?
- [ ] **Network latency**: Test from different locations
- [ ] **Database load**: Check during off-peak hours

### Memory Issues Checklist
- [ ] **Batch size**: Process in smaller batches
- [ ] **Result caching**: Clear cache periodically
- [ ] **Connection pooling**: Limit concurrent connections
- [ ] **Garbage collection**: Force GC between large operations
- [ ] **Streaming**: Use streaming for large result sets

## Logging and Diagnostics

### Enable Comprehensive Logging
```python
import logging

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('veridano_agent.log'),
        logging.StreamHandler()
    ]
)

# Veridano-specific logger
veridano_logger = logging.getLogger('veridano')
veridano_logger.setLevel(logging.DEBUG)
```

### Custom Diagnostics
```python
class VeridanoDiagnostics:
    def __init__(self, client):
        self.client = client
        self.metrics = {
            "total_queries": 0,
            "failed_queries": 0,
            "avg_response_time": 0.0,
            "slowest_query": 0.0,
            "fastest_query": float('inf')
        }
    
    async def diagnostic_search(self, **kwargs):
        """Search with diagnostic tracking"""
        start_time = time.time()
        
        try:
            result = await self.client.semantic_search(**kwargs)
            response_time = time.time() - start_time
            
            # Update metrics
            self.metrics["total_queries"] += 1
            self.metrics["avg_response_time"] = (
                (self.metrics["avg_response_time"] * (self.metrics["total_queries"] - 1) + response_time) 
                / self.metrics["total_queries"]
            )
            self.metrics["slowest_query"] = max(self.metrics["slowest_query"], response_time)
            self.metrics["fastest_query"] = min(self.metrics["fastest_query"], response_time)
            
            # Log slow queries
            if response_time > 1.0:
                veridano_logger.warning(f"Slow query ({response_time:.3f}s): {kwargs.get('query', '')[:50]}...")
            
            return result
            
        except Exception as e:
            self.metrics["failed_queries"] += 1
            veridano_logger.error(f"Query failed: {e}")
            raise
    
    def print_diagnostics(self):
        """Print diagnostic summary"""
        print("\n📊 VERIDANO DIAGNOSTICS")
        print(f"Total Queries: {self.metrics['total_queries']}")
        print(f"Failed Queries: {self.metrics['failed_queries']}")
        print(f"Success Rate: {((self.metrics['total_queries'] - self.metrics['failed_queries']) / max(self.metrics['total_queries'], 1)) * 100:.1f}%")
        print(f"Average Response: {self.metrics['avg_response_time']:.3f}s")
        print(f"Fastest Query: {self.metrics['fastest_query']:.3f}s")
        print(f"Slowest Query: {self.metrics['slowest_query']:.3f}s")
```

## Getting Help

### Before Contacting Support
1. **Check this troubleshooting guide** for common solutions
2. **Review error logs** for specific error messages
3. **Test with simplified queries** to isolate the issue
4. **Check service status** at status.veridano.com
5. **Try the connection diagnostic script** above

### Information to Provide
When contacting support, include:

```python
# Run this diagnostic script and include output
async def support_diagnostic():
    """Generate support diagnostic information"""
    
    print("VERIDANO SUPPORT DIAGNOSTIC")
    print("=" * 40)
    
    # Environment info
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    # Configuration (don't include secrets)
    print(f"Endpoint: {os.getenv('VERIDANO_ENDPOINT')}")
    print(f"Client ID: {os.getenv('VERIDANO_CLIENT_ID')}")
    print(f"Region: {os.getenv('VERIDANO_REGION', 'us-east-1')}")
    
    # Connection test
    try:
        client = VeridanoMCPClient()
        health = await client.health_check()
        print(f"Health check: {health}")
    except Exception as e:
        print(f"Health check failed: {e}")
    
    # Network test
    try:
        import requests
        response = requests.get("https://api.veridano.com/health", timeout=5)
        print(f"Network test: {response.status_code}")
    except Exception as e:
        print(f"Network test failed: {e}")

# Run diagnostic
await support_diagnostic()
```

### Contact Information
- **GitHub Issues**: [Report bugs and request features](https://github.com/Veridano/veridano-intelligence-platform/issues)
- **Enterprise Support**: enterprise@veridano.com
- **Emergency Issues**: Include "URGENT" in subject line
- **Community**: Discord server for community support

### Service Status
- **Status Page**: https://status.veridano.com
- **Incident Updates**: Automatic notifications for service disruptions
- **Maintenance Windows**: Scheduled during low-usage periods (typically 2-4 AM EST)