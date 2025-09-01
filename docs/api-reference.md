# Veridano MCP API Reference

## Base Configuration

**MCP Server Endpoint**: `https://api.veridano.com/mcp`  
**Protocol Version**: MCP 2.0  
**Authentication**: AWS Cognito Client Credentials

## Available Tools

### semantic_search

Perform vector similarity search across all government cybersecurity intelligence sources.

**Parameters:**
```json
{
  "query": "string (required) - Natural language search query",
  "top_k": "integer (optional, default: 10) - Maximum results to return",
  "min_score": "float (optional, default: 0.6) - Minimum similarity threshold", 
  "sources": "array (optional) - Filter by specific data sources",
  "timeframe": "string (optional) - published_after date filter"
}
```

**Example Request:**
```json
{
  "tool": "semantic_search",
  "parameters": {
    "query": "APT29 persistence mechanisms Windows",
    "top_k": 15,
    "min_score": 0.8,
    "sources": ["NSA", "FBI", "CISA"]
  }
}
```

**Response Format:**
```json
{
  "documents": [
    {
      "id": "NSA-CSA-U/OO-158123",
      "title": "Russian Foreign Intelligence Service Cyber Operations",
      "content": "Comprehensive analysis of APT29 persistence techniques...",
      "source": "NSA",
      "category": "threat_intelligence",
      "document_type": "cybersecurity_advisory", 
      "score": 0.94,
      "published_date": "2024-12-15T00:00:00Z",
      "url": "https://www.nsa.gov/...",
      "metadata": {
        "similarity_threshold": 0.8,
        "query_matches": 4,
        "embedding_model": "AWS_Titan_V2"
      }
    }
  ],
  "total_results": 15,
  "query": "APT29 persistence mechanisms Windows",
  "search_backend": "Aurora_pgvector",
  "timestamp": "2025-09-01T01:30:00Z"
}
```

### source_search

Search within a specific government agency's intelligence.

**Parameters:**
```json
{
  "query": "string (required) - Search query",
  "source": "string (required) - Government source to search",
  "limit": "integer (optional, default: 20) - Maximum results",
  "category": "string (optional) - Filter by document category"
}
```

**Available Sources:**
- `CISA` - Cybersecurity and Infrastructure Security Agency
- `FBI` - Federal Bureau of Investigation Cyber Division  
- `NIST` - National Institute of Standards and Technology
- `DHS` - Department of Homeland Security
- `NSA` - National Security Agency Cybersecurity
- `USCYBERCOM` - U.S. Cyber Command
- `White House` - Executive Office Cybersecurity Policy
- `NVD` - National Vulnerability Database
- `ICS-CERT` - Industrial Control Systems Computer Emergency Response Team
- `US-CERT` - United States Computer Emergency Response Team
- `FedRAMP` - Federal Risk and Authorization Management Program

**Example Request:**
```json
{
  "tool": "source_search",
  "parameters": {
    "query": "CVE-2025-0282 remote code execution",
    "source": "NVD",
    "limit": 10,
    "category": "vulnerability"
  }
}
```

### threat_correlation

Cross-reference threat indicators across multiple sources to identify related intelligence.

**Parameters:**
```json
{
  "indicators": "array (required) - Threat indicators to correlate",
  "sources": "array (optional) - Sources to search across", 
  "timeframe": "string (optional) - Time window for correlation",
  "correlation_threshold": "float (optional, default: 0.7) - Correlation confidence"
}
```

**Example Request:**
```json
{
  "tool": "threat_correlation", 
  "parameters": {
    "indicators": [
      "192.168.1.100",
      "evil.example.com", 
      "a1b2c3d4e5f6..."
    ],
    "sources": ["FBI", "CISA", "US-CERT"],
    "timeframe": "60_days",
    "correlation_threshold": 0.8
  }
}
```

### vulnerability_lookup

Direct CVE and vulnerability information lookup.

**Parameters:**
```json
{
  "cve_id": "string (optional) - Specific CVE identifier",
  "keywords": "string (optional) - Vulnerability keywords",
  "cvss_min": "float (optional) - Minimum CVSS score",
  "published_after": "string (optional) - ISO date string"
}
```

**Example Request:**
```json
{
  "tool": "vulnerability_lookup",
  "parameters": {
    "cve_id": "CVE-2025-0282",
    "cvss_min": 7.0
  }
}
```

## Error Handling

### Standard Error Response
```json
{
  "error": {
    "code": "SEARCH_FAILED",
    "message": "Query execution failed",
    "details": "Connection timeout to Aurora database",
    "timestamp": "2025-09-01T01:30:00Z"
  }
}
```

### Common Error Codes
- `AUTH_REQUIRED` - Invalid or missing authentication
- `QUOTA_EXCEEDED` - Rate limit exceeded
- `SEARCH_FAILED` - Database query error
- `INVALID_SOURCE` - Unknown data source specified
- `MALFORMED_QUERY` - Invalid query parameters

### Rate Limiting
```json
{
  "error": {
    "code": "QUOTA_EXCEEDED", 
    "message": "Rate limit exceeded",
    "retry_after": 30,
    "current_limit": "200 requests/second"
  }
}
```

## Performance Guidelines

### Query Optimization
- **Use source filtering** when you know the relevant agency
- **Set appropriate min_score** to filter low-relevance results
- **Limit top_k** to actual needs (max 50 recommended)
- **Cache results** for repeated queries

### Best Practices
```python
# ✅ Good - Focused query with source filtering
await client.call_tool(
    "semantic_search",
    query="Log4j vulnerability mitigation guidance",
    sources=["CISA", "NIST"],
    top_k=10,
    min_score=0.75
)

# ❌ Poor - Vague query without filtering
await client.call_tool(
    "semantic_search", 
    query="cybersecurity",
    top_k=100,
    min_score=0.1
)
```

## Integration Patterns

### Batch Processing
```python
async def batch_threat_research(indicators: List[str]):
    client = await setup_veridano_client()
    results = []
    
    for indicator in indicators:
        try:
            result = await client.call_tool(
                "threat_correlation",
                indicators=[indicator],
                correlation_threshold=0.8
            )
            results.append(result)
            
            # Respect rate limits
            await asyncio.sleep(0.1)
            
        except Exception as e:
            print(f"Failed to process {indicator}: {e}")
    
    return results
```

### Real-time Monitoring
```python
async def monitor_new_threats():
    client = await setup_veridano_client()
    
    while True:
        # Check for new high-severity threats
        recent_threats = await client.call_tool(
            "semantic_search",
            query="critical vulnerability zero-day active exploitation",
            sources=["CISA", "FBI", "US-CERT"],
            timeframe="last_24_hours",
            min_score=0.9
        )
        
        if recent_threats["total_results"] > 0:
            await process_urgent_threats(recent_threats["documents"])
        
        await asyncio.sleep(300)  # Check every 5 minutes
```

## Troubleshooting

### Connection Issues
```python
# Test basic connectivity
try:
    health = await client.health_check()
    print(f"Status: {health['status']}")
    print(f"Sources: {len(health['available_sources'])}")
except Exception as e:
    print(f"Connection failed: {e}")
```

### Authentication Debug
```python
# Verify authentication
try:
    tools = await client.list_tools()
    print("✅ Authentication successful")
except AuthenticationError:
    print("❌ Check client credentials")
except Exception as e:
    print(f"❌ Auth error: {e}")
```