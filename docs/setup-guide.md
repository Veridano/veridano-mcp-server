# Veridano MCP Server Setup Guide

## ⚡ Quick Setup (No Authentication)

### Prerequisites
- Python 3.8+ environment  
- Network access (HTTPS/443 outbound)

### For Claude Desktop

1. Open Claude Desktop settings
2. Go to **Developer** > **Edit Config**  
3. Add this configuration:

```json
{
  "mcpServers": {
    "veridano": {
      "command": "python",
      "args": ["-c", "import requests; exec(requests.get('https://raw.githubusercontent.com/Veridano/veridano-mcp-server/main/mcp_client.py').text)"]
    }
  }
}
```

4. Restart Claude Desktop
5. **Done!** Start querying cybersecurity intelligence

### For ChatGPT

1. Go to **ChatGPT Settings** > **Beta Features** > **Model Context Protocol**
2. Click **Add MCP Server**
3. Configure:
   - **Name**: `Veridano Intelligence`
   - **URL**: `https://raw.githubusercontent.com/Veridano/veridano-mcp-server/main/mcp_client.py`
   - **Type**: `Python Script`
4. **Enable** the server
5. **Done!** Start querying cybersecurity intelligence

### Alternative: Local Installation

```bash
# Clone repository
git clone https://github.com/Veridano/veridano-mcp-server.git
cd veridano-mcp-server

# Configure in Claude Desktop
{
  "mcpServers": {
    "veridano": {
      "command": "python",
      "args": ["/absolute/path/to/veridano-mcp-server/mcp_client.py"]
    }
  }
}
```

## Basic Usage Test

```python
# Test query in Claude Desktop:
"Use veridano_search to find recent CISA advisories about ransomware"
```

---

## 🔒 Enterprise Setup (With Authentication)

*For organizations requiring authentication and rate limiting:*

### Environment Variables (Optional)

```bash
export VERIDANO_ENDPOINT="https://7lqg8v66p1.execute-api.us-east-1.amazonaws.com/prod/mcp"
export VERIDANO_REGION="us-east-1"
# Uncomment for authenticated access:
# export VERIDANO_CLIENT_ID="your_client_id"  
# export VERIDANO_CLIENT_SECRET="your_client_secret"
```

### 3. Basic Connection Test

```python
#!/usr/bin/env python3
"""
Veridano Connection Test
Verify your agent can connect to the Veridano Intelligence Platform
"""

import asyncio
import os
from mcp_client import MCPClient

async def test_veridano_connection():
    """Test basic connectivity to Veridano"""
    
    client = MCPClient(
        endpoint=os.getenv('VERIDANO_ENDPOINT', 'https://7lqg8v66p1.execute-api.us-east-1.amazonaws.com/prod/mcp')
    )
    
    try:
        # Test 1: Health check
        print("🔍 Testing Veridano connectivity...")
        health = await client.health_check()
        print(f"✅ Health check: {health['status']}")
        
        # Test 2: List available tools
        print("\n🛠️ Available tools:")
        tools = await client.list_tools()
        for tool in tools:
            print(f"  - {tool['name']}: {tool['description']}")
        
        # Test 3: Simple search
        print("\n🔍 Testing search functionality...")
        result = await client.call_tool(
            "veridano_search",
            query="ransomware threat intelligence",
            top_k=3,
            min_score=0.7
        )
        
        print(f"✅ Search test: {result['total_results']} results found")
        if result['documents']:
            print(f"  Sample: {result['documents'][0]['title'][:60]}...")
        
        print("\n🎉 Veridano connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_veridano_connection())
    exit(0 if success else 1)
```

## Configuration Options

### Authentication Methods

#### Client Credentials (Recommended)
```python
client = MCPClient(
    endpoint="https://api.veridano.com/mcp",
    auth_method="cognito_client_credentials",
    client_id="your_client_id",
    client_secret="your_client_secret",
    region="us-east-1"
)
```

#### User Pool Authentication
```python
client = MCPClient(
    endpoint="https://api.veridano.com/mcp", 
    auth_method="cognito_user_pool",
    user_pool_id="us-east-1_HgeKuWISD",
    username="your_username",
    password="your_password"
)
```

### Advanced Configuration

```python
client = MCPClient(
    endpoint="https://api.veridano.com/mcp",
    auth_method="cognito_client_credentials",
    client_id=os.getenv('VERIDANO_CLIENT_ID'),
    client_secret=os.getenv('VERIDANO_CLIENT_SECRET'),
    
    # Performance tuning
    timeout=30,  # Request timeout in seconds
    retry_attempts=3,  # Number of retry attempts
    retry_backoff=2.0,  # Exponential backoff multiplier
    
    # Connection pooling
    max_connections=10,  # Connection pool size
    keep_alive=True,     # Maintain persistent connections
    
    # Rate limiting
    max_requests_per_second=50,  # Client-side rate limiting
    
    # Caching
    cache_enabled=True,   # Enable response caching
    cache_ttl=300,       # Cache time-to-live in seconds
)
```

## Integration Patterns

### 1. Standalone Agent Integration

```python
"""
Simple agent that queries Veridano for threat intelligence
"""
import asyncio
from veridano_mcp_client import VeridanoClient

class ThreatIntelligenceAgent:
    def __init__(self):
        self.veridano = VeridanoClient()
    
    async def research_threat(self, threat_name: str):
        """Research a specific threat across all sources"""
        
        # Search for threat intelligence
        intel = await self.veridano.veridano_search(
            query=f"{threat_name} tactics techniques procedures",
            sources=["NSA", "FBI", "USCYBERCOM"],
            top_k=20,
            min_score=0.8
        )
        
        # Search for vulnerabilities
        vulns = await self.veridano.vulnerability_lookup(
            keywords=threat_name,
            cvss_min=7.0
        )
        
        # Search for mitigation guidance
        mitigations = await self.veridano.veridano_search(
            query=f"{threat_name} mitigation defense recommendations",
            sources=["CISA", "NIST"],
            top_k=10
        )
        
        return {
            "threat_intelligence": intel,
            "vulnerabilities": vulns,
            "mitigations": mitigations
        }

# Usage
agent = ThreatIntelligenceAgent()
result = await agent.research_threat("Lazarus Group")
```

### 2. ChatBot Integration

```python
"""
ChatBot that uses Veridano for cybersecurity Q&A
"""
import asyncio
from veridano_mcp_client import VeridanoClient

class CyberSecurityChatBot:
    def __init__(self):
        self.veridano = VeridanoClient()
        self.conversation_history = []
    
    async def answer_question(self, question: str):
        """Answer cybersecurity questions using government intelligence"""
        
        # Determine query type
        if "CVE" in question.upper():
            # Vulnerability question
            results = await self.veridano.vulnerability_lookup(
                keywords=question,
                cvss_min=0.0
            )
        elif any(word in question.lower() for word in ["policy", "compliance", "framework"]):
            # Compliance question
            results = await self.veridano.veridano_search(
                query=question,
                sources=["FedRAMP", "NIST", "White House"],
                top_k=10
            )
        elif any(word in question.lower() for word in ["industrial", "scada", "ics", "ot"]):
            # Industrial systems question
            results = await self.veridano.source_search(
                query=question,
                source="ICS-CERT"
            )
        else:
            # General threat intelligence
            results = await self.veridano.veridano_search(
                query=question,
                top_k=15,
                min_score=0.7
            )
        
        # Generate response based on results
        if results["total_results"] > 0:
            response = self.generate_response(question, results["documents"])
        else:
            response = "I couldn't find specific government intelligence on that topic."
        
        self.conversation_history.append({
            "question": question,
            "response": response,
            "sources_consulted": len(results.get("documents", []))
        })
        
        return response
    
    def generate_response(self, question: str, documents: list) -> str:
        """Generate natural language response from search results"""
        
        if not documents:
            return "No relevant government intelligence found."
        
        # Extract key information
        sources = list(set(doc["source"] for doc in documents))
        latest_doc = max(documents, key=lambda x: x.get("published_date", ""))
        
        response = f"Based on {len(documents)} government intelligence sources "
        response += f"({', '.join(sources)}), "
        
        # Add most relevant finding
        top_doc = documents[0]
        response += f"the latest intelligence indicates: {top_doc['content'][:200]}..."
        
        # Add source attribution
        response += f"\n\nSource: {top_doc['source']} - {top_doc['title']}"
        response += f"\nPublished: {latest_doc.get('published_date', 'Unknown')}"
        
        return response

# Usage
bot = CyberSecurityChatBot()
answer = await bot.answer_question("What are the latest ransomware threats?")
print(answer)
```

### 3. Automated Threat Monitoring

```python
"""
Automated monitoring agent that watches for new threats
"""
import asyncio
from datetime import datetime, timedelta
from veridano_mcp_client import VeridanoClient

class ThreatMonitoringAgent:
    def __init__(self, alert_callback=None):
        self.veridano = VeridanoClient()
        self.alert_callback = alert_callback
        self.last_check = datetime.now()
    
    async def monitor_critical_threats(self):
        """Continuously monitor for critical new threats"""
        
        while True:
            try:
                # Check for new critical vulnerabilities
                critical_cves = await self.veridano.vulnerability_lookup(
                    cvss_min=9.0,
                    published_after=self.last_check.isoformat()
                )
                
                # Check for new emergency directives
                emergency_alerts = await self.veridano.veridano_search(
                    query="emergency directive critical alert immediate action",
                    sources=["CISA", "US-CERT"],
                    timeframe="last_24_hours",
                    min_score=0.9
                )
                
                # Check for APT activity
                apt_activity = await self.veridano.veridano_search(
                    query="advanced persistent threat campaign attribution",
                    sources=["NSA", "FBI", "USCYBERCOM"],
                    timeframe="last_48_hours", 
                    min_score=0.85
                )
                
                # Process alerts
                new_threats = []
                if critical_cves["total_results"] > 0:
                    new_threats.extend(critical_cves["documents"])
                if emergency_alerts["total_results"] > 0:
                    new_threats.extend(emergency_alerts["documents"])
                if apt_activity["total_results"] > 0:
                    new_threats.extend(apt_activity["documents"])
                
                if new_threats and self.alert_callback:
                    await self.alert_callback(new_threats)
                
                self.last_check = datetime.now()
                print(f"✅ Threat monitoring cycle complete - {len(new_threats)} new threats detected")
                
                # Wait 10 minutes before next check
                await asyncio.sleep(600)
                
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
                await asyncio.sleep(60)  # Wait 1 minute on error

    async def alert_handler(self, threats: list):
        """Handle threat alerts"""
        for threat in threats:
            severity = "CRITICAL" if threat.get("cvss_score", 0) >= 9.0 else "HIGH"
            print(f"🚨 {severity} THREAT DETECTED")
            print(f"   Title: {threat['title']}")
            print(f"   Source: {threat['source']}")
            print(f"   Published: {threat['published_date']}")
            print(f"   Score: {threat.get('score', 'N/A')}")
            print()

# Usage
monitor = ThreatMonitoringAgent(alert_callback=monitor.alert_handler)
await monitor.monitor_critical_threats()
```

## Performance Optimization

### Connection Pooling
```python
# Reuse client instances
class VeridanoClientPool:
    def __init__(self, pool_size=5):
        self.pool = []
        self.pool_size = pool_size
    
    async def get_client(self):
        if not self.pool:
            client = VeridanoClient()
            await client.connect()
            return client
        return self.pool.pop()
    
    async def return_client(self, client):
        if len(self.pool) < self.pool_size:
            self.pool.append(client)
        else:
            await client.disconnect()
```

### Query Caching
```python
import time
from functools import wraps

def cache_results(ttl=300):
    """Cache search results for specified TTL"""
    cache = {}
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Create cache key
            key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Check cache
            if key in cache:
                result, timestamp = cache[key]
                if time.time() - timestamp < ttl:
                    return result
            
            # Execute and cache
            result = await func(*args, **kwargs)
            cache[key] = (result, time.time())
            
            return result
        return wrapper
    return decorator

class CachedVeridanoClient(VeridanoClient):
    @cache_results(ttl=600)  # 10 minute cache
    async def veridano_search(self, **kwargs):
        return await super().veridano_search(**kwargs)
```

## Error Handling & Resilience

### Retry with Exponential Backoff
```python
import asyncio
import random

async def resilient_search(client, **search_params):
    """Search with automatic retry and backoff"""
    
    max_retries = 3
    base_delay = 1.0
    
    for attempt in range(max_retries):
        try:
            result = await client.veridano_search(**search_params)
            return result
            
        except QuotaExceededException as e:
            if attempt == max_retries - 1:
                raise
            
            # Exponential backoff with jitter
            delay = (base_delay * (2 ** attempt)) + random.uniform(0, 1)
            print(f"⏳ Rate limited, retrying in {delay:.1f}s...")
            await asyncio.sleep(delay)
            
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            
            print(f"⚠️ Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(base_delay)
```

### Circuit Breaker Pattern
```python
class VeridanoCircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    async def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = await func(*args, **kwargs)
            
            # Success - reset failure count
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
            self.failure_count = 0
            
            return result
            
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                print(f"🔴 Circuit breaker OPEN - too many failures")
            
            raise
```

## Production Deployment

### Environment Configuration
```python
# production_config.py
import os

VERIDANO_CONFIG = {
    "endpoint": os.getenv("VERIDANO_ENDPOINT", "https://api.veridano.com/mcp"),
    "region": os.getenv("VERIDANO_REGION", "us-east-1"),
    "client_id": os.getenv("VERIDANO_CLIENT_ID"),
    "client_secret": os.getenv("VERIDANO_CLIENT_SECRET"),
    
    # Performance settings
    "timeout": int(os.getenv("VERIDANO_TIMEOUT", "30")),
    "max_retries": int(os.getenv("VERIDANO_MAX_RETRIES", "3")),
    "rate_limit": int(os.getenv("VERIDANO_RATE_LIMIT", "50")),
    
    # Caching
    "cache_enabled": os.getenv("VERIDANO_CACHE", "true").lower() == "true",
    "cache_ttl": int(os.getenv("VERIDANO_CACHE_TTL", "600")),
    
    # Logging
    "log_level": os.getenv("VERIDANO_LOG_LEVEL", "INFO"),
    "log_queries": os.getenv("VERIDANO_LOG_QUERIES", "false").lower() == "true"
}
```

### Health Monitoring
```python
async def health_monitor():
    """Monitor Veridano service health"""
    
    client = VeridanoClient()
    
    while True:
        try:
            start_time = time.time()
            health = await client.health_check()
            response_time = (time.time() - start_time) * 1000
            
            if health["status"] == "healthy":
                print(f"✅ Veridano healthy - {response_time:.0f}ms")
            else:
                print(f"⚠️ Veridano degraded: {health}")
                
        except Exception as e:
            print(f"❌ Veridano unreachable: {e}")
            
        await asyncio.sleep(60)  # Check every minute
```

### Logging and Metrics
```python
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('veridano_agent')

class MetricsCollector:
    def __init__(self):
        self.query_count = 0
        self.error_count = 0
        self.total_response_time = 0.0
        
    async def tracked_search(self, client, **params):
        """Search with metrics collection"""
        start_time = time.time()
        
        try:
            result = await client.veridano_search(**params)
            response_time = time.time() - start_time
            
            self.query_count += 1
            self.total_response_time += response_time
            
            logger.info(f"Search completed - {response_time:.3f}s - {result['total_results']} results")
            return result
            
        except Exception as e:
            self.error_count += 1
            logger.error(f"Search failed - {e}")
            raise
    
    def get_stats(self):
        """Get performance statistics"""
        if self.query_count == 0:
            return {"queries": 0, "avg_response_time": 0, "error_rate": 0}
            
        return {
            "queries": self.query_count,
            "avg_response_time": self.total_response_time / self.query_count,
            "error_rate": self.error_count / self.query_count
        }
```

## Troubleshooting

### Common Issues

#### Authentication Failures
```bash
# Verify credentials
export VERIDANO_CLIENT_ID="test_client_id"
python -c "
import os
print('Client ID:', os.getenv('VERIDANO_CLIENT_ID'))
print('Endpoint:', os.getenv('VERIDANO_ENDPOINT'))
"
```

#### Network Connectivity
```bash
# Test endpoint reachability
curl -I https://7lqg8v66p1.execute-api.us-east-1.amazonaws.com/prod/mcp
```

#### Rate Limiting
```python
# Handle rate limits gracefully
try:
    result = await client.veridano_search(query="test")
except QuotaExceededException as e:
    retry_after = e.retry_after
    print(f"Rate limited - retry after {retry_after}s")
    await asyncio.sleep(retry_after)
```

### Debug Mode
```python
client = VeridanoClient(
    debug=True,           # Enable debug logging
    log_queries=True,     # Log all queries
    log_responses=True    # Log all responses
)
```

### Performance Testing
```python
async def performance_test():
    """Test Veridano performance characteristics"""
    
    client = VeridanoClient()
    test_queries = [
        "ransomware attack vectors",
        "CVE-2024 critical vulnerabilities", 
        "APT29 tactics techniques procedures",
        "industrial control systems threats",
        "federal cybersecurity policy"
    ]
    
    response_times = []
    
    for query in test_queries:
        start = time.time()
        result = await client.veridano_search(query=query, top_k=5)
        response_time = time.time() - start
        
        response_times.append(response_time)
        print(f"Query: {query[:30]}... - {response_time:.3f}s - {result['total_results']} results")
    
    avg_time = sum(response_times) / len(response_times)
    print(f"\n📊 Average response time: {avg_time:.3f}s")
```

## Support Resources

- **Documentation**: Complete API reference and examples
- **Issue Tracking**: GitHub Issues for bug reports and feature requests  
- **Performance Monitoring**: Built-in metrics and health checks
- **Enterprise Support**: Direct technical support for production deployments

For additional setup assistance, contact the Veridano team or consult the troubleshooting documentation.