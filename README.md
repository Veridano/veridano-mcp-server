# Veridano Intelligence API

> **Cybersecurity intelligence API for AI agents - Hosted service, no setup required**

Access 7+ U.S. government cybersecurity agencies through a hosted API service with **2,000+ curated intelligence documents** including the complete CISA Known Exploited Vulnerabilities (KEV) catalog.

## ⚡ Quick Start

### For Claude Desktop

**Step 1:** Open Claude Desktop application

**Step 2:** Click **Settings** → **Features** → **Model Context Protocol**

**Step 3:** Click **Add custom connector**

**Step 4:** Fill in the connector details:
- **Name**: `Veridano`
- **Remote MCP server URL**: `https://7lqg8v66p1.execute-api.us-east-1.amazonaws.com/prod/mcp`

**Step 5:** Click **Add** then restart Claude Desktop

**That's it!** No downloads required - Claude connects directly to the hosted MCP server.

### For ChatGPT

**Step 1:** Go to ChatGPT Settings > Beta Features > Model Context Protocol

**Step 2:** Add Custom MCP Server:
- **Name**: `Veridano Intelligence`
- **Server URL**: `https://7lqg8v66p1.execute-api.us-east-1.amazonaws.com/prod/mcp`

**Step 3:** Enable the server

**That's it!** Start querying: *"Use veridano_search to find CISA ransomware advisories"*

## 🔗 Direct API Access  

**For direct REST API access without MCP:**

```bash
curl -X POST "https://7lqg8v66p1.execute-api.us-east-1.amazonaws.com/prod/api/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "CISA ransomware advisory", "top_k": 5}'
```

## 🎯 Overview

Veridano provides AI agents with comprehensive access to U.S. government cybersecurity intelligence through a unified MCP server interface.

### Key Capabilities

- **Real-time intelligence search** across 7+ USG cybersecurity agencies  
- **Complete CISA KEV catalog** - All 1,413+ known exploited vulnerabilities with BOD 22-01 compliance data
- **Vector similarity search** with semantic understanding of threat context
- **Zero-config setup** - works immediately after installation
- **High-performance architecture** supporting concurrent agent sessions
- **Enhanced automated data ingestion** with complete source coverage and regular updates

## 🏛️ Data Sources

The platform continuously monitors and indexes content from:

| Source | Update Frequency | Content Type | Documents |
|--------|------------------|--------------|-----------|
| **CISA KEV** | **6 hours** | **Complete Known Exploited Vulnerabilities Catalog** | **1,413** |
| **CISA** | 1 hour (RSS), Weekly (Comprehensive) | Advisories, Emergency Directives, Alerts | 400+ |
| **NIST SP 800** | **Daily** | **Complete SP 800 Series Publications** | **200+** |
| **FBI IC3** | 12 hours | Private Industry Cyber Advisories, Crime Alerts | 50+ |
| **DHS BODs** | Daily | Binding Operational Directives, Federal Compliance | 25+ |
| **FBI Cyber** | Weekly | Private Industry Notifications, Cyber Bulletins | 15+ |
| **NIST NVD** | 6 hours | CVE Database, CVSS Scoring | Variable |
| **NSA Cybersecurity** | Weekly | APT Reports, Cryptographic Guidance, Technical Advisories | 25+ |
| **USCYBERCOM** | Weekly | Threat Intelligence, Attribution Reports | 20+ |
| **White House** | Daily | Executive Orders, National Cyber Strategy, Policy Directives | 15+ |
| **ICS-CERT** | Weekly | Industrial Control Systems Advisories | 30+ |
| **US-CERT** | 8 hours | Cybersecurity Alerts, Analysis Reports, IOCs | 25+ |

## 📊 API Parameters

**Required:**
- `query` (string) - Search query for cybersecurity intelligence

**Optional:**
- `top_k` (integer) - Number of results to return (default: 5)
- `min_score` (float) - Minimum similarity score 0.0-1.0 (default: 0.6)  
- `sources` (array) - Filter by specific sources: `["CISA", "FBI", "NIST", "DHS", "NSA", "USCYBERCOM", "White House", "NVD", "ICS-CERT", "US-CERT", "FedRAMP"]`

## 📝 Example Queries

**Vulnerability Research:**
- *"Use veridano_search to find CVE-2024-3400 from the CISA KEV catalog"*
- *"Search for all known exploited vulnerabilities in Microsoft Exchange"*
- *"Find BOD 22-01 compliance deadlines for recent KEV additions"*

**Threat Intelligence:**  
- *"Use veridano_search for Chinese APT Salt Typhoon telecommunications targeting"*
- *"Find Ghost Cring ransomware IOCs MITRE ATT&CK"*

**Compliance Research:**
- *"Search for complete NIST SP 800-207 zero trust architecture framework"*
- *"Find all CISA binding operational directives for federal compliance"*
- *"Search for BOD 22-01 vulnerability remediation requirements"*

## 🏗️ Architecture

```
AI Agent → MCP Client → Veridano MCP Server → Enhanced Scraper Network → Government Data Sources
```

### Enhanced Data Collection (September 2025)
Veridano now operates **5 specialized enhanced scrapers** that provide complete coverage of critical government cybersecurity sources:

1. **CISA KEV Complete Scraper** - Processes all 1,413 known exploited vulnerabilities every 6 hours
2. **NIST SP 800 Complete Scraper** - Collects the full SP 800 publication series daily  
3. **CISA RSS Real-time Scraper** - Monitors 9 CISA RSS feeds hourly for immediate threat intelligence
4. **FBI IC3 Complete Scraper** - Harvests all private industry cyber advisories every 12 hours
5. **CISA BOD Complete Scraper** - Maintains comprehensive federal compliance directive coverage

### Technical Stack
- **Compute**: AWS Lambda (Python 3.11) with 5 specialized functions
- **AI/ML**: Amazon Bedrock (Titan V2 Embeddings, 1024 dimensions) 
- **Database**: Aurora PostgreSQL with pgvector for semantic search
- **Storage**: S3 with organized folder structure by source and type
- **Protocol**: Model Context Protocol (MCP)
- **Scheduling**: EventBridge cron scheduling for automated real-time updates
- **Processing**: BeautifulSoup4 + requests for robust content extraction

## 🚀 Usage Examples

Once configured, you can immediately start querying cybersecurity intelligence:

**Ask Claude Desktop:**
- *"Use veridano_search to find all known exploited vulnerabilities in VMware"*
- *"Search for CISA KEV entries with federal compliance deadlines in 2025"* 
- *"Find complete NIST SP 800 cybersecurity framework documents"*
- *"Search for BOD 22-01 vulnerability remediation requirements"*
- *"Use veridano_search for FBI IC3 private industry cyber advisories"*

## 📊 Performance

- **Response time**: 150-300ms average
- **Database**: **2,000+ curated government cybersecurity documents**
- **CISA KEV Coverage**: **100% complete** (1,413 vulnerabilities)
- **Updates**: Every 1-6 hours for real-time sources, daily for comprehensive catalogs
- **Uptime**: 99.9+ availability with enhanced infrastructure
- **Enhanced Processing**: 5 specialized scrapers with automated S3 storage and dashboard integration

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

### Local Development Setup
For developers who want to modify or test the MCP client locally:

```bash
git clone https://github.com/Veridano/veridano-mcp-server.git
cd veridano-mcp-server

# For Claude Desktop development (legacy method):
{
  "mcpServers": {
    "veridano-local": {
      "command": "python",
      "args": ["/full/path/to/veridano-mcp-server/mcp_client.py"]
    }
  }
}
```

**Note**: Custom Connector (direct URL) is recommended for regular usage.

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