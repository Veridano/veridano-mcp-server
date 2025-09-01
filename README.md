# Veridano Intelligence API

> **Cybersecurity intelligence API for AI agents - Hosted service, no setup required**

Access 11 U.S. government cybersecurity data sources through a hosted API service.

## ⚡ Direct API Access

**API Endpoint:** `https://7lqg8v66p1.execute-api.us-east-1.amazonaws.com/prod/api/search`

**Example Query:**
```bash
curl -X POST "https://7lqg8v66p1.execute-api.us-east-1.amazonaws.com/prod/api/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "CISA ransomware advisory", "top_k": 5}'
```

**That's it!** No installation, no configuration, no authentication required.

## 🎯 Overview

Veridano provides AI agents with comprehensive access to U.S. government cybersecurity intelligence through a unified MCP server interface.

### Key Capabilities

- **Real-time intelligence search** across 11 USG cybersecurity data sources  
- **Vector similarity search** with semantic understanding of threat context
- **Zero-config setup** - works immediately after installation
- **High-performance architecture** supporting concurrent agent sessions
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

## 📊 API Parameters

**Required:**
- `query` (string) - Search query for cybersecurity intelligence

**Optional:**
- `top_k` (integer) - Number of results to return (default: 5)
- `min_score` (float) - Minimum similarity score 0.0-1.0 (default: 0.6)  
- `sources` (array) - Filter by specific sources: `["CISA", "FBI", "NIST", "DHS", "NSA", "USCYBERCOM", "White House", "NVD", "ICS-CERT", "US-CERT", "FedRAMP"]`

## 📝 Example Queries

**Vulnerability Research:**
- *"Search for CVE-2024-1234 vulnerability details"*
- *"Find recent Windows remote code execution vulnerabilities"*

**Threat Intelligence:**  
- *"Search CISA advisories for ransomware threats"*
- *"Get APT threat intelligence summary for last 30 days"*

**Compliance Research:**
- *"Find FedRAMP moderate baseline requirements"*
- *"Search White House cybersecurity executive orders"*

## 🏗️ Architecture

```
AI Agent → MCP Client → Veridano MCP Server → Government Data Sources
```

### Technical Stack
- **Compute**: AWS Lambda (Python 3.9)
- **AI/ML**: Amazon Bedrock (Titan Embeddings) 
- **Database**: Aurora PostgreSQL with pgvector
- **Storage**: S3 for document storage
- **Protocol**: Model Context Protocol (MCP)
- **Scheduling**: EventBridge for automated updates

## 🚀 Usage Examples

Once configured, you can immediately start querying cybersecurity intelligence:

**Ask Claude Desktop:**
- *"Search for recent CISA ransomware advisories"*
- *"Get details for CVE-2024-1234"* 
- *"Find APT threat intelligence from the last 30 days"*
- *"Search for industrial control system vulnerabilities"*
- *"Find White House cybersecurity executive orders"*

## 📊 Performance

- **Response time**: 150-300ms average
- **Database**: 500,000+ government cybersecurity documents  
- **Updates**: Every 4-12 hours for time-sensitive sources
- **Uptime**: 99.9% availability

## 📝 Response Format

```json
{
  "documents": [
    {
      "id": "AA24-131A",
      "title": "CISA Analysis of Ransomware Trends and Tactics",
      "content": "Comprehensive analysis of ransomware trends...",
      "source": "CISA",
      "score": 0.95,
      "published_date": "2024-05-10T00:00:00Z",
      "url": "https://www.cisa.gov/news-events/cybersecurity-advisories/aa24-131a"
    }
  ],
  "total_results": 1,
  "timestamp": "2025-09-01T01:21:21.356Z"
}
```

## ⚡ Usage Guidelines

- **Concurrent sessions**: 1000+ supported
- **Query complexity**: No limits
- **Result size**: Up to 50 documents per query
- **Fair usage**: Please cache results when appropriate

## 💡 Alternative Setup Methods

### Local Installation
```bash
git clone https://github.com/Veridano/veridano-mcp-server.git
cd veridano-mcp-server

# Configure with full path in Claude Desktop:
{
  "mcpServers": {
    "veridano": {
      "command": "python",
      "args": ["/full/path/to/veridano-mcp-server/mcp_client.py"]
    }
  }
}
```

### Enterprise Options
Contact enterprise@veridano.com for:
- Custom authentication requirements
- Private deployment options  
- Volume licensing and SLAs

## 📚 Documentation

- **[API Reference](./docs/api-reference.md)** - Complete MCP tool documentation
- **[Setup Guide](./docs/setup-guide.md)** - Detailed installation instructions  
- **[Integration Examples](./examples/)** - Sample agent implementations
- **[Performance Guide](./docs/performance.md)** - Optimization best practices
- **[Troubleshooting](./docs/troubleshooting.md)** - Common issues and solutions

## 🤝 Support

- **Issues**: [GitHub Issues](https://github.com/Veridano/veridano-mcp-server/issues)
- **Enterprise Support**: enterprise@veridano.com

## 📄 License

MIT License - See LICENSE file for details.

---

**Built for AI Agents. Powered by U.S. Government Intelligence.**