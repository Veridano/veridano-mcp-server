# Veridano Performance Guide

## Performance Characteristics

### Response Times
- **Average query response**: 150-300ms
- **Fastest queries**: 50-100ms (cached or simple lookups)
- **Complex correlation queries**: 300-800ms
- **Batch operations**: 100-200ms per query

### Throughput Limits
- **Current production**: 200 queries/second (pending AWS quota increase)
- **Per-agent limit**: 50 queries/second
- **Burst capacity**: 500 queries/second for up to 5 minutes
- **Concurrent agents**: 1000+ supported

### Database Performance
- **Total documents**: 500,000+ government cybersecurity documents
- **Vector dimensions**: 1536 (AWS Titan Embeddings v2)
- **Index type**: pgvector HNSW for sub-100ms similarity search
- **Update frequency**: Real-time indexing of new documents

## Optimization Strategies

### 1. Query Optimization

#### Use Source Filtering
```python
# ✅ Optimized - Search specific sources
result = await client.semantic_search(
    query="Log4Shell vulnerability guidance",
    sources=["CISA", "NIST"],  # Reduces search space by 80%
    top_k=10
)

# ❌ Unoptimized - Search all sources
result = await client.semantic_search(
    query="Log4Shell vulnerability guidance",
    top_k=10  # Searches all 11 sources
)
```

#### Set Appropriate Similarity Thresholds
```python
# ✅ Optimized - Higher threshold for precise results
result = await client.semantic_search(
    query="specific threat actor TTPs",
    min_score=0.8,  # Only highly relevant results
    top_k=10
)

# ❌ Unoptimized - Low threshold returns noise
result = await client.semantic_search(
    query="specific threat actor TTPs", 
    min_score=0.3,  # Many irrelevant results
    top_k=50
)
```

#### Limit Result Sets
```python
# ✅ Optimized - Request only what you need
result = await client.semantic_search(
    query="ransomware mitigation",
    top_k=5  # Fast response, focused results
)

# ❌ Unoptimized - Requesting excess data
result = await client.semantic_search(
    query="ransomware mitigation",
    top_k=100  # Slower response, processing overhead
)
```

### 2. Caching Strategies

#### Result Caching
```python
import time
from functools import lru_cache

class CachedVeridanoClient:
    def __init__(self, client):
        self.client = client
        self.cache = {}
        self.cache_ttl = 600  # 10 minutes
    
    async def cached_search(self, query: str, **kwargs):
        """Search with automatic result caching"""
        
        # Create cache key
        cache_key = f"{query}:{hash(str(kwargs))}"
        
        # Check cache
        if cache_key in self.cache:
            result, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                print(f"💨 Cache hit for: {query[:30]}...")
                return result
        
        # Fetch from Veridano
        result = await self.client.semantic_search(query=query, **kwargs)
        
        # Store in cache
        self.cache[cache_key] = (result, time.time())
        print(f"🔍 Fresh search for: {query[:30]}...")
        
        return result

# Usage
cached_client = CachedVeridanoClient(veridano_client)
result = await cached_client.cached_search("APT29 techniques")
```

#### Intelligent Pre-fetching
```python
class IntelligentCache:
    def __init__(self, client):
        self.client = client
        self.popular_queries = [
            "latest ransomware threats",
            "critical vulnerabilities 2025", 
            "APT campaign intelligence",
            "zero-day exploits active",
            "emergency cybersecurity directives"
        ]
    
    async def warm_cache(self):
        """Pre-fetch popular queries"""
        print("🔥 Warming Veridano cache...")
        
        for query in self.popular_queries:
            try:
                await self.client.semantic_search(
                    query=query,
                    top_k=10,
                    min_score=0.8
                )
                print(f"  ✅ Cached: {query}")
            except Exception as e:
                print(f"  ❌ Failed to cache: {query} - {e}")
```

### 3. Batch Processing

#### Efficient Batch Queries
```python
async def batch_vulnerability_research(cve_list: List[str]):
    """Research multiple CVEs efficiently"""
    
    results = {}
    
    # Process in batches of 5 with rate limiting
    batch_size = 5
    for i in range(0, len(cve_list), batch_size):
        batch = cve_list[i:i + batch_size]
        
        # Create concurrent queries for batch
        tasks = []
        for cve in batch:
            task = client.vulnerability_lookup(cve_id=cve)
            tasks.append(task)
        
        # Execute batch concurrently
        batch_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for cve, result in zip(batch, batch_results):
            if isinstance(result, Exception):
                print(f"❌ Failed to fetch {cve}: {result}")
                results[cve] = {"error": str(result)}
            else:
                results[cve] = result
        
        # Rate limiting between batches
        if i + batch_size < len(cve_list):
            await asyncio.sleep(1.0)  # 1 second between batches
    
    return results
```

### 4. Connection Management

#### Connection Pooling
```python
class VeridanoConnectionPool:
    def __init__(self, pool_size: int = 10):
        self.pool_size = pool_size
        self.available_connections = []
        self.active_connections = set()
    
    async def get_connection(self):
        """Get a connection from the pool"""
        if self.available_connections:
            conn = self.available_connections.pop()
            self.active_connections.add(conn)
            return conn
        
        if len(self.active_connections) < self.pool_size:
            conn = VeridanoMCPClient()
            await conn.connect()
            self.active_connections.add(conn)
            return conn
        
        # Pool exhausted - wait for available connection
        while not self.available_connections:
            await asyncio.sleep(0.1)
        
        return await self.get_connection()
    
    async def return_connection(self, conn):
        """Return a connection to the pool"""
        if conn in self.active_connections:
            self.active_connections.remove(conn)
            self.available_connections.append(conn)

# Usage
pool = VeridanoConnectionPool(pool_size=5)

async def pooled_search(query: str):
    conn = await pool.get_connection()
    try:
        result = await conn.semantic_search(query=query)
        return result
    finally:
        await pool.return_connection(conn)
```

## Performance Monitoring

### Query Performance Tracking
```python
import time
from collections import defaultdict

class PerformanceTracker:
    def __init__(self):
        self.query_times = []
        self.error_count = 0
        self.source_performance = defaultdict(list)
    
    async def tracked_search(self, client, **params):
        """Execute search with performance tracking"""
        start_time = time.time()
        
        try:
            result = await client.semantic_search(**params)
            response_time = time.time() - start_time
            
            # Track metrics
            self.query_times.append(response_time)
            
            # Track per-source performance
            sources = params.get('sources', ['ALL'])
            for source in sources:
                self.source_performance[source].append(response_time)
            
            print(f"📊 Query: {response_time:.3f}s - {result['total_results']} results")
            return result
            
        except Exception as e:
            self.error_count += 1
            print(f"❌ Query failed: {e}")
            raise
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate performance analysis report"""
        if not self.query_times:
            return {"error": "No queries tracked"}
        
        avg_time = sum(self.query_times) / len(self.query_times)
        min_time = min(self.query_times)
        max_time = max(self.query_times)
        
        # Calculate percentiles
        sorted_times = sorted(self.query_times)
        p50 = sorted_times[len(sorted_times) // 2]
        p95 = sorted_times[int(len(sorted_times) * 0.95)]
        p99 = sorted_times[int(len(sorted_times) * 0.99)]
        
        # Source performance analysis
        source_stats = {}
        for source, times in self.source_performance.items():
            source_stats[source] = {
                "avg_time": sum(times) / len(times),
                "query_count": len(times)
            }
        
        return {
            "summary": {
                "total_queries": len(self.query_times),
                "error_count": self.error_count,
                "success_rate": (len(self.query_times) / (len(self.query_times) + self.error_count)) * 100
            },
            "response_times": {
                "average": avg_time,
                "minimum": min_time,
                "maximum": max_time,
                "median": p50,
                "p95": p95,
                "p99": p99
            },
            "source_performance": source_stats
        }

# Usage
tracker = PerformanceTracker()

# Track multiple queries
for query in test_queries:
    await tracker.tracked_search(client, query=query, top_k=10)

# Get performance report
report = tracker.get_performance_report()
print(json.dumps(report, indent=2))
```

### Health Monitoring
```python
async def health_monitor_advanced():
    """Advanced health monitoring with detailed metrics"""
    
    client = VeridanoMCPClient()
    
    health_metrics = {
        "endpoint_health": False,
        "authentication_status": False,
        "search_functionality": False,
        "database_performance": 0.0,
        "last_check": None
    }
    
    try:
        # Test 1: Basic connectivity
        start = time.time()
        health = await client.health_check()
        health_metrics["endpoint_health"] = health.get("status") == "healthy"
        
        # Test 2: Authentication
        tools = await client.list_tools()
        health_metrics["authentication_status"] = len(tools) > 0
        
        # Test 3: Search performance
        search_start = time.time()
        result = await client.semantic_search(
            query="test connectivity",
            top_k=1,
            min_score=0.5
        )
        search_time = time.time() - search_start
        health_metrics["search_functionality"] = result["total_results"] >= 0
        health_metrics["database_performance"] = search_time
        
        health_metrics["last_check"] = datetime.now().isoformat()
        
        # Overall health assessment
        all_healthy = (
            health_metrics["endpoint_health"] and
            health_metrics["authentication_status"] and  
            health_metrics["search_functionality"] and
            health_metrics["database_performance"] < 2.0  # Under 2 seconds
        )
        
        status = "🟢 HEALTHY" if all_healthy else "🟡 DEGRADED"
        print(f"{status} - Response time: {search_time:.3f}s")
        
        return health_metrics
        
    except Exception as e:
        print(f"🔴 UNHEALTHY - {e}")
        health_metrics["last_error"] = str(e)
        health_metrics["last_check"] = datetime.now().isoformat()
        return health_metrics
```

## Rate Limiting Best Practices

### Exponential Backoff
```python
import random

async def smart_retry(func, *args, max_retries=3, **kwargs):
    """Retry with exponential backoff and jitter"""
    
    for attempt in range(max_retries):
        try:
            return await func(*args, **kwargs)
            
        except QuotaExceededException as e:
            if attempt == max_retries - 1:
                raise
            
            # Exponential backoff with jitter
            base_delay = 2 ** attempt
            jitter = random.uniform(0.1, 0.5)
            delay = base_delay + jitter
            
            print(f"⏳ Rate limited - backing off {delay:.1f}s")
            await asyncio.sleep(delay)
            
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            
            print(f"⚠️ Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(1.0)
```

### Rate Limiting Token Bucket
```python
import asyncio
import time

class TokenBucket:
    """Token bucket rate limiter"""
    
    def __init__(self, rate: float, capacity: int):
        self.rate = rate  # tokens per second
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.time()
    
    async def acquire(self, tokens: int = 1) -> bool:
        """Acquire tokens from bucket"""
        now = time.time()
        
        # Add tokens based on elapsed time
        elapsed = now - self.last_update
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_update = now
        
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        
        # Calculate wait time
        wait_time = (tokens - self.tokens) / self.rate
        await asyncio.sleep(wait_time)
        
        self.tokens = max(0, self.tokens - tokens)
        return True

class RateLimitedVeridanoClient:
    def __init__(self, client, queries_per_second: float = 50):
        self.client = client
        self.rate_limiter = TokenBucket(rate=queries_per_second, capacity=int(queries_per_second * 2))
    
    async def semantic_search(self, **kwargs):
        """Rate-limited semantic search"""
        await self.rate_limiter.acquire()
        return await self.client.semantic_search(**kwargs)
```

## Concurrent Processing

### Parallel Query Execution
```python
async def parallel_intelligence_gathering(indicators: List[str]):
    """Process multiple indicators concurrently"""
    
    # Create semaphore to limit concurrent requests
    semaphore = asyncio.Semaphore(10)  # Max 10 concurrent
    
    async def process_indicator(indicator: str):
        async with semaphore:
            try:
                # Search for threat intelligence
                result = await client.semantic_search(
                    query=f"{indicator} threat intelligence IOC",
                    sources=["FBI", "CISA", "US-CERT"],
                    top_k=5
                )
                return {"indicator": indicator, "intelligence": result}
                
            except Exception as e:
                return {"indicator": indicator, "error": str(e)}
    
    # Execute all searches concurrently
    tasks = [process_indicator(indicator) for indicator in indicators]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    return results
```

### Streaming Results
```python
async def stream_threat_intelligence(query: str, sources: List[str]):
    """Stream results from multiple sources as they complete"""
    
    async def search_source(source: str):
        try:
            result = await client.source_search(
                query=query,
                source=source, 
                limit=10
            )
            return {"source": source, "result": result}
        except Exception as e:
            return {"source": source, "error": str(e)}
    
    # Create tasks for each source
    tasks = [search_source(source) for source in sources]
    
    # Process results as they complete
    for coro in asyncio.as_completed(tasks):
        source_result = await coro
        
        if "error" in source_result:
            print(f"❌ {source_result['source']}: {source_result['error']}")
        else:
            result = source_result["result"]
            print(f"✅ {source_result['source']}: {result['total_results']} documents")
            
            # Process results immediately
            for doc in result["documents"]:
                yield doc
```

## Load Testing

### Performance Benchmarking
```python
async def benchmark_veridano_performance():
    """Comprehensive performance benchmark"""
    
    client = VeridanoMCPClient()
    
    test_scenarios = [
        {
            "name": "Simple Lookup",
            "params": {"query": "CVE-2024-38063", "top_k": 1}
        },
        {
            "name": "Complex Semantic Search", 
            "params": {"query": "APT29 persistence mechanisms Windows Active Directory", "top_k": 20}
        },
        {
            "name": "Multi-source Search",
            "params": {"query": "ransomware critical infrastructure", "sources": ["CISA", "FBI", "ICS-CERT"], "top_k": 15}
        },
        {
            "name": "High-precision Search",
            "params": {"query": "zero-day exploit", "min_score": 0.95, "top_k": 10}
        }
    ]
    
    benchmark_results = {}
    
    for scenario in test_scenarios:
        print(f"\n🧪 Testing: {scenario['name']}")
        
        times = []
        errors = 0
        
        # Run each scenario 10 times
        for i in range(10):
            try:
                start = time.time()
                result = await client.semantic_search(**scenario['params'])
                response_time = time.time() - start
                times.append(response_time)
                
                print(f"  Run {i+1}: {response_time:.3f}s - {result['total_results']} results")
                
            except Exception as e:
                errors += 1
                print(f"  Run {i+1}: ERROR - {e}")
            
            await asyncio.sleep(0.5)  # Small delay between runs
        
        if times:
            benchmark_results[scenario['name']] = {
                "avg_time": sum(times) / len(times),
                "min_time": min(times),
                "max_time": max(times),
                "success_rate": len(times) / 10 * 100,
                "error_count": errors
            }
    
    # Print benchmark report
    print("\n" + "=" * 60)
    print("VERIDANO PERFORMANCE BENCHMARK RESULTS")
    print("=" * 60)
    
    for scenario, metrics in benchmark_results.items():
        print(f"\n{scenario}:")
        print(f"  Average: {metrics['avg_time']:.3f}s")
        print(f"  Range: {metrics['min_time']:.3f}s - {metrics['max_time']:.3f}s") 
        print(f"  Success Rate: {metrics['success_rate']:.1f}%")
    
    return benchmark_results
```

### Stress Testing
```python
async def stress_test_veridano(concurrent_agents: int = 50, duration_minutes: int = 5):
    """Stress test Veridano with multiple concurrent agents"""
    
    print(f"🔥 Starting stress test: {concurrent_agents} agents for {duration_minutes} minutes")
    
    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)
    
    query_count = 0
    error_count = 0
    response_times = []
    
    async def agent_worker(agent_id: int):
        """Individual agent worker"""
        nonlocal query_count, error_count, response_times
        
        client = VeridanoMCPClient()
        await client.connect()
        
        test_queries = [
            "ransomware attack vectors",
            "APT campaign intelligence", 
            "critical vulnerabilities",
            "zero-day exploits",
            "emergency cybersecurity directives"
        ]
        
        while time.time() < end_time:
            try:
                query = random.choice(test_queries)
                
                query_start = time.time()
                result = await client.semantic_search(
                    query=query,
                    top_k=5,
                    min_score=0.7
                )
                query_time = time.time() - query_start
                
                query_count += 1
                response_times.append(query_time)
                
                if query_count % 100 == 0:
                    print(f"  Agent {agent_id}: {query_count} queries completed")
                
            except Exception as e:
                error_count += 1
                if error_count % 10 == 0:
                    print(f"  Agent {agent_id}: {error_count} errors encountered")
            
            await asyncio.sleep(random.uniform(1.0, 3.0))  # Variable query interval
    
    # Launch concurrent agents
    tasks = [agent_worker(i) for i in range(concurrent_agents)]
    await asyncio.gather(*tasks, return_exceptions=True)
    
    # Calculate final metrics
    total_time = time.time() - start_time
    avg_response = sum(response_times) / len(response_times) if response_times else 0
    queries_per_second = query_count / total_time
    
    print(f"\n📊 STRESS TEST RESULTS")
    print(f"Duration: {total_time:.1f}s")
    print(f"Total Queries: {query_count}")
    print(f"Errors: {error_count}")
    print(f"Success Rate: {(query_count / (query_count + error_count)) * 100:.1f}%")
    print(f"Queries/Second: {queries_per_second:.1f}")
    print(f"Average Response: {avg_response:.3f}s")
```

## Production Optimization Checklist

### ✅ Pre-deployment
- [ ] Configure appropriate cache TTL for your use case
- [ ] Set up connection pooling for high-throughput scenarios
- [ ] Implement exponential backoff retry logic
- [ ] Configure rate limiting within your application
- [ ] Set up performance monitoring and alerting

### ✅ Runtime Optimization  
- [ ] Use source filtering whenever possible
- [ ] Set appropriate similarity thresholds (0.7+ recommended)
- [ ] Limit result sets to actual needs
- [ ] Implement result caching for repeated queries
- [ ] Monitor and optimize query patterns

### ✅ Monitoring & Alerting
- [ ] Track query response times and success rates
- [ ] Monitor for rate limiting and adjust accordingly
- [ ] Set up alerts for service degradation
- [ ] Implement circuit breaker pattern for resilience
- [ ] Log performance metrics for analysis

For additional performance optimization assistance, contact Veridano enterprise support.