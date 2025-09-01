# Veridano Intelligence Platform

> **Professional cybersecurity intelligence platform powered by Amazon Bedrock AgentCore Gateway**

The Veridano Intelligence Platform provides AI agents with comprehensive access to U.S. government cybersecurity intelligence through a unified MCP (Model Context Protocol) server interface.

## 🎯 Overview

Veridano aggregates and indexes cybersecurity intelligence from 11 authoritative U.S. government sources, making it instantly searchable and accessible to AI agents via MCP server protocols. The platform is designed specifically for AI agent integration, not direct human use.

### Key Capabilities

- **Real-time intelligence search** across 11 USG cybersecurity data sources
- **Vector similarity search** with semantic understanding of threat context
- **MCP server compliance** for seamless AI agent integration
- **High-performance architecture** supporting 1000+ concurrent agent sessions
- **Automated data ingestion** with regular updates from government sources

## 🏛️ Data Sources

The platform continuously monitors and indexes content from:

| Source | Update Frequency | Content Type |
|--------|------------------|--------------|
| **CISA** | 4 hours (RSS), Weekly (Comprehensive) | Advisories, Emergency Directives, Alerts |
| **FBI Cyber** | Weekly | Private Industry Notifications, Cyber Bulletins |
| **NIST** | 6 hours (NVD), Weekly (Publications) | CVE Database, Cybersecurity Framework, SP 800 Series |
| **DHS** | Weekly | Sector-Specific Guidance, Cybersecurity Directives |
| **NSA Cybersecurity** | Weekly | APT Reports, Cryptographic Guidance, Technical Advisories |
| **USCYBERCOM** | Weekly | Threat Intelligence, Attribution Reports |
| **White House** | Daily | Executive Orders, National Cyber Strategy, Policy Directives |
| **NVD** | 12 hours | CVE Vulnerability Database, CVSS Scoring |
| **ICS-CERT** | Weekly | Industrial Control Systems Advisories |
| **US-CERT** | 8 hours | Cybersecurity Alerts, Analysis Reports, IOCs |
| **FedRAMP** | Weekly | Cloud Security Controls, Compliance Frameworks |

## 🤖 MCP Server Integration

### Endpoint Configuration

```json
{
  "mcp_server": {
    "name": "veridano-intelligence",
    "endpoint": "https://api.veridano.com/mcp",
    "version": "2.0",
    "capabilities": ["search", "semantic_search", "source_filtering"]
  }
}
```

### Authentication

Veridano uses AWS Cognito for secure access:

```python
# Example MCP client configuration
import mcp_client

client = mcp_client.MCPClient(
    endpoint="https://api.veridano.com/mcp",
    auth_provider="aws_cognito",
    user_pool_id="us-east-1_HgeKuWISD",
    client_id="7eh15ia3csfmmrqnlv6t6aq877"
)
```

## 🔧 Available Tools

### semantic_search
Search across all government cybersecurity intelligence with vector similarity.

```json
{
  "tool": "semantic_search",
  "parameters": {
    "query": "ransomware attack vectors critical infrastructure",
    "top_k": 10,
    "min_score": 0.7,
    "sources": ["CISA", "FBI", "ICS-CERT"]
  }
}
```

### source_search  
Target specific government agencies for focused intelligence.

```json
{
  "tool": "source_search", 
  "parameters": {
    "query": "CVE-2025 zero-day vulnerabilities",
    "source": "NVD",
    "limit": 20
  }
}
```

### threat_correlation
Cross-reference threats across multiple government sources.

```json
{
  "tool": "threat_correlation",
  "parameters": {
    "indicators": ["malicious_ip", "malware_hash"],
    "timeframe": "30_days",
    "correlation_threshold": 0.8
  }
}
```

## 🏗️ Architecture

### Infrastructure Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    AI Agent Clients                         │
└─────────────────────┬───────────────────────────────────────┘
                      │ MCP Protocol
┌─────────────────────▼───────────────────────────────────────┐
│              Amazon Bedrock AgentCore Gateway               │
│                  (Intelligent Routing)                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                Specialized Lambda Targets                  │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐│
│  │  CISA   │ │   FBI   │ │  NIST   │ │   DHS   │ │   ...   ││
│  │ Target  │ │ Target  │ │ Target  │ │ Target  │ │ Targets ││
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘│
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│           Aurora PostgreSQL + pgvector                     │
│              (Vector Intelligence Database)                │
└─────────────────────────────────────────────────────────────┘
```

### Technical Stack

- **Compute**: AWS Lambda (Python 3.9)
- **AI/ML**: Amazon Bedrock (Claude 3.5 Sonnet, Titan Embeddings)
- **Database**: Aurora PostgreSQL with pgvector extensions
- **Storage**: S3 for raw document storage
- **Orchestration**: Bedrock AgentCore Gateway with MCP protocol
- **Authentication**: AWS Cognito OAuth 2.0
- **Monitoring**: CloudWatch with custom dashboards
- **Scheduling**: EventBridge for automated data collection

## 🚀 Getting Started for AI Agents

### 1. Authentication Setup

Request access credentials from Veridano:
- **User Pool ID**: `us-east-1_HgeKuWISD`
- **Client ID**: Contact Veridano for agent-specific client credentials
- **Region**: `us-east-1`

### 2. MCP Client Implementation

```python
import asyncio
import mcp_client

async def setup_veridano_client():
    client = mcp_client.MCPClient(
        endpoint="https://api.veridano.com/mcp",
        auth_method="cognito_client_credentials",
        region="us-east-1"
    )
    
    # List available tools
    tools = await client.list_tools()
    print("Available Veridano tools:", tools)
    
    return client

async def search_threat_intelligence(query: str):
    client = await setup_veridano_client()
    
    # Semantic search across all sources
    results = await client.call_tool(
        "semantic_search",
        query=query,
        top_k=10,
        min_score=0.7
    )
    
    return results["documents"]

# Example usage
if __name__ == "__main__":
    results = asyncio.run(search_threat_intelligence(
        "APT29 latest campaign tactics techniques procedures"
    ))
```

### 3. Query Examples

#### Vulnerability Research
```python
# Search for specific CVEs
cve_results = await client.call_tool(
    "source_search",
    query="CVE-2024-38063 remote code execution",
    source="NVD"
)

# Find related vulnerabilities
related = await client.call_tool(
    "semantic_search", 
    query="Windows TCP/IP remote code execution",
    sources=["NVD", "CISA", "FBI"]
)
```

#### Threat Intelligence
```python
# Cross-source threat analysis
apt_intel = await client.call_tool(
    "threat_correlation",
    query="Lazarus Group cryptocurrency targeting",
    sources=["FBI", "NSA", "USCYBERCOM"],
    timeframe="90_days"
)

# Industrial control systems threats  
ics_threats = await client.call_tool(
    "source_search",
    query="SCADA vulnerability manufacturing",
    source="ICS-CERT"
)
```

#### Compliance Research
```python
# FedRAMP requirements
compliance = await client.call_tool(
    "semantic_search",
    query="moderate baseline security controls cloud",
    sources=["FedRAMP", "NIST"]
)

# Policy guidance
policy = await client.call_tool(
    "source_search", 
    query="executive order critical infrastructure cybersecurity",
    source="White House"
)
```

## 📊 Performance Characteristics

- **Average query response**: 150-300ms
- **Peak throughput**: 200 queries/second (with quota increases)
- **Database size**: 500,000+ government cybersecurity documents
- **Update frequency**: Every 4-12 hours for time-sensitive sources
- **Availability**: 99.9% uptime SLA

## 🔒 Security Features

- **Authentication**: AWS Cognito with MFA support
- **Authorization**: Role-based access control
- **Encryption**: All data encrypted in transit and at rest
- **Compliance**: FedRAMP-ready architecture
- **Audit**: Full CloudTrail logging of all agent queries

## 📝 Response Format

All MCP tool responses follow this standardized format:

```json
{
  "documents": [
    {
      "id": "AA24-131A",
      "title": "CISA Analysis of Ransomware Trends and Tactics",
      "content": "Comprehensive analysis of ransomware trends...",
      "source": "CISA",
      "category": "threat_intelligence", 
      "document_type": "cybersecurity_advisory",
      "score": 0.95,
      "published_date": "2024-05-10T00:00:00Z",
      "url": "https://www.cisa.gov/news-events/cybersecurity-advisories/aa24-131a",
      "metadata": {
        "similarity_threshold": 0.7,
        "query_matches": 3,
        "embedding_status": "✅ Generated"
      }
    }
  ],
  "total_results": 1,
  "query": "ransomware attack vectors",
  "search_backend": "Aurora_Serverless_v2_pgvector",
  "timestamp": "2025-09-01T01:21:21.356Z"
}
```

## ⚡ Rate Limits & Quotas

**Current Limits (Production):**
- **Authenticated agents**: 1000 concurrent sessions
- **Query rate**: 200 queries/second (pending AWS quota increase)
- **Search complexity**: No limit on query complexity
- **Result size**: Up to 50 documents per query

**Fair Usage:**
- Implement exponential backoff for rate limit handling
- Cache results locally when appropriate  
- Use source filtering to reduce unnecessary load

## 🛠️ Setup Instructions

### For AI Agent Developers

1. **Request Access**
   - Contact Veridano for agent credentials
   - Provide agent use case and expected volume
   - Receive client ID and integration guide

2. **Install MCP Client**
   ```bash
   pip install mcp-client requests boto3
   ```

3. **Configure Authentication**
   ```python
   # Environment variables
   export VERIDANO_CLIENT_ID="your_client_id" 
   export VERIDANO_CLIENT_SECRET="your_client_secret"
   export VERIDANO_REGION="us-east-1"
   ```

4. **Test Connection**
   ```python
   import veridano_mcp_client
   
   client = veridano_mcp_client.connect()
   health = await client.health_check()
   print(f"Veridano status: {health['status']}")
   ```

### For Enterprise Deployment

1. **Infrastructure Requirements**
   - AWS Account with Bedrock access
   - Aurora PostgreSQL with pgvector
   - Lambda execution role with appropriate permissions
   - S3 bucket for document storage

2. **Deployment Options**
   - **SaaS**: Use hosted Veridano instance (recommended)
   - **Self-hosted**: Deploy using provided CloudFormation templates
   - **Hybrid**: Custom integration with existing security infrastructure

## 📚 Documentation

- **[API Reference](./docs/api-reference.md)** - Complete MCP tool documentation
- **[Setup Guide](./docs/setup-guide.md)** - Detailed installation instructions  
- **[Integration Examples](./examples/)** - Sample agent implementations
- **[Performance Guide](./docs/performance.md)** - Optimization best practices
- **[Troubleshooting](./docs/troubleshooting.md)** - Common issues and solutions

## 🤝 Support

- **Issues**: [GitHub Issues](https://github.com/Veridano/veridano-intelligence-platform/issues)
- **Documentation**: [docs.veridano.com](https://docs.veridano.com)
- **Enterprise Support**: enterprise@veridano.com
- **Community**: [Veridano Discord](https://discord.gg/veridano)

## 📄 License

Copyright © 2025 Veridano Intelligence Platform. All rights reserved.

**Enterprise License** - Contact for commercial licensing terms.

---

**Built for AI Agents. Powered by AWS. Secured by Government Intelligence.**