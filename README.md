# Veridano Intelligence API

> **Government cybersecurity intelligence MCP server for AI agents**

Access **14 US, UK, and EU government cybersecurity agencies** through a hosted MCP server with **6,000+ curated intelligence documents** including CISA KEV, MITRE ATT&CK, NIST SP 800, and international threat intelligence.

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

- **Real-time intelligence search** across 14 US/UK/EU government agencies
- **7 MCP tools** for threat intelligence, CVE analysis, and APT tracking
- **Complete CISA KEV catalog** - All known exploited vulnerabilities with BOD 22-01 compliance
- **MITRE ATT&CK integration** - 1,450+ techniques, groups, and mitigations
- **International coverage** - NCSC (UK) and ENISA (EU) threat intelligence
- **Vector similarity search** with semantic understanding via AWS Titan V2 embeddings
- **Query expansion** - Automatic abbreviation expansion (BOD, KEV, APT, etc.)
- **Citation support** - Proper APA/MLA citations for government sources
- **Zero-config setup** - Works immediately after MCP server connection
- **High-performance** - Sub-second response times with Aurora + pgvector

## 🏛️ Data Sources (14 Agencies)

The platform continuously monitors and indexes content from:

### US Government Sources
| Source | Update Frequency | Content Type | Documents |
|--------|------------------|--------------|-----------|
| **CISA** | 1-6 hours | KEV, Advisories, BODs, Emergency Directives | 400+ |
| **FBI IC3** | 12 hours | Private Industry Advisories | 50+ |
| **NIST** | 6 hours | SP 800 Series, CVE Database | 200+ |
| **DHS** | Daily | Binding Operational Directives | 25+ |
| **NSA** | Weekly | APT Reports, Cryptographic Guidance | 25+ |
| **USCYBERCOM** | Weekly | Threat Intelligence, Attribution | 20+ |
| **Treasury/FinCEN** | Daily | Financial Cyber Crime | 15+ |
| **DoD/DC3** | Daily | Defense Cyber Crime | 30+ |
| **White House** | Daily | Executive Orders, Policy | 15+ |
| **US-CERT** | 8 hours | Alerts, Analysis Reports | 25+ |
| **ICS-CERT** | Weekly | Industrial Control Systems | 30+ |

### Frameworks & International
| Source | Update Frequency | Content Type | Documents |
|--------|------------------|--------------|-----------|
| **MITRE ATT&CK** | Weekly | Techniques, Groups, Mitigations | 1,450+ |
| **NCSC (UK)** | Daily | UK Threat Reports, Guidance | ~2,000/year |
| **ENISA (EU)** | Daily | EU Cybersecurity Policy | ~500/year |

**Total Coverage:** ~6,000+ documents across 14 agencies

## 🔧 MCP Tools Available

Once connected, AI agents have access to 7 specialized tools:

1. **veridano_search** - Semantic search across all sources
   - Parameters: `query`, `top_k`, `sources`
   - Best for: General threat intelligence queries

2. **get_latest** - Recent documents (last N hours)
   - Parameters: `hours`, `limit`, `sources`, `critical_only`
   - Best for: "What's new?", breaking alerts

3. **batch_search** - Multiple queries at once
   - Parameters: `queries` (array of query objects)
   - Best for: Multi-topic research, 3-10x faster

4. **analyze_threat_trends** - Historical trend analysis
   - Parameters: `threat_category`, `days`
   - Best for: Temporal patterns, activity analysis

5. **compare_vulnerabilities** - Side-by-side CVE comparison
   - Parameters: `cve_ids` (array)
   - Best for: Vulnerability prioritization

6. **get_remediation_guidance** - Mitigation steps
   - Parameters: `threat_or_cve`
   - Best for: Actionable remediation advice

7. **track_threat_actor** - APT group tracking
   - Parameters: `actor_name`
   - Best for: APT profiling and attribution

## 📊 Search Parameters

**veridano_search parameters:**
- `query` (string) - Search query (supports query expansion)
- `top_k` (integer) - Number of results (default: 5)
- `min_score` (float) - Similarity score 0.0-1.0 (default: 0.6)
- `sources` (array) - Filter: `["CISA", "FBI", "NIST", "DHS", "NSA", "USCYBERCOM", "MITRE", "NCSC", "ENISA", "Treasury", "DoD", "White House", "US-CERT", "ICS-CERT"]`

## 📝 Example Queries

**Vulnerability Research:**
- *"Use veridano_search to find CVE-2024-3400 across all sources"*
- *"Compare CVE-2024-3400 and CVE-2023-44487 using compare_vulnerabilities"*
- *"Get remediation guidance for Log4Shell"*
- *"Find BOD 22-01 compliance requirements from CISA"*

**Threat Intelligence:**
- *"Track APT29 activity using track_threat_actor"*
- *"Use veridano_search for ransomware guidance from CISA and FBI"*
- *"Analyze ransomware trends over the last 90 days"*
- *"Show me critical alerts from the last 24 hours using get_latest"*

**Compliance & Frameworks:**
- *"Search for NIST SP 800-207 zero trust architecture"*
- *"Find all CISA binding operational directives"*
- *"Search for MITRE ATT&CK techniques used by APT29"*
- *"Get recent UK threat intelligence from NCSC"*

## 🏗️ Architecture

```
AI Agent → MCP Client → Veridano MCP Server → Enhanced Scraper Network → Government Data Sources
```

### Data Collection (September 2025)
Veridano operates **20 specialized scrapers** for comprehensive government intelligence:

**Enhanced Scrapers (8):**
- CISA RSS (4 hours), CISA KEV (6 hours), CISA BOD (daily)
- FBI IC3 (12 hours), NIST Comprehensive (6 hours), NIST SP 800 (daily)
- DoD/DC3 (daily), Treasury/FinCEN (daily)

**Specialized Intelligence (3):**
- MITRE ATT&CK (weekly) - 1,450+ techniques, groups, mitigations
- International Sources (daily) - NCSC (UK), ENISA (EU)
- Real-time Alerting - Critical event notifications

**Legacy Scrapers (9):**
- NSA, USCYBERCOM, White House, US-CERT, ICS-CERT, NVD, FedRAMP

### Technical Stack
- **Compute**: AWS Lambda (29 functions, Python 3.11, ARM64)
- **AI/ML**: Amazon Bedrock (Titan V2 Embeddings, 1024 dimensions)
- **Database**: Aurora Serverless v2 with pgvector for semantic search
- **Connection Pooling**: RDS Proxy (40-60% overhead reduction)
- **Storage**: S3 (10 buckets, lifecycle policies)
- **Protocol**: Model Context Protocol (MCP) + REST APIs
- **Scheduling**: EventBridge (14 schedules, 1-hour to weekly)
- **Monitoring**: CloudWatch Dashboard, SNS Alerting
- **Quality**: Data validation pipeline with duplicate detection

## 🚀 Usage Examples

Once configured, you can immediately start querying cybersecurity intelligence:

**Ask Claude Desktop:**
- *"Use veridano_search to find CISA ransomware guidance"*
- *"Show me critical cybersecurity alerts from the last 24 hours using get_latest"*
- *"Track APT29 activity across government reports"*
- *"Compare CVE-2024-3400 with CVE-2023-44487 using compare_vulnerabilities"*
- *"Get remediation guidance for Log4Shell"*
- *"Analyze ransomware trends over the last 90 days"*
- *"Search for MITRE ATT&CK techniques used by APT29"*
- *"Find UK threat intelligence from NCSC about state-sponsored attacks"*

## 📊 Performance

- **Response time**: <1 second average (150-300ms typical)
- **Database**: **6,000+ curated government cybersecurity documents**
- **Coverage**: 14 agencies (US, UK, EU)
- **MITRE ATT&CK**: Complete (1,450+ documents)
- **Updates**: Every 1-6 hours for real-time sources, daily/weekly for comprehensive sources
- **Rate Limit**: 1,000 requests/second
- **Uptime**: 99.9% target
- **Tools**: 7 MCP tools + 5 analytics APIs
- **Infrastructure**: 29 Lambda functions, RDS Proxy, Aurora Serverless v2

## 📝 Response Format

```json
{
  "results": [
    {
      "document_id": "cisa-aa24-131",
      "title": "CISA Ransomware Guide",
      "quick_summary": "First 500 characters for rapid assessment...",
      "content": "Full content...",
      "source": "CISA",
      "url": "https://...",
      "published_date": "2024-05-10",
      "relevance_score": 0.94,
      "citation": {
        "apa": "CISA. (2024). Ransomware Guide 2024. Retrieved from https://...",
        "mla": "CISA. \"Ransomware Guide 2024.\" 10 May 2024, https://...",
        "permalink": "https://www.cisa.gov/..."
      },
      "source_metadata": {
        "organization": "CISA",
        "authority_level": "federal_mandate",
        "reliability_score": 1.0,
        "document_type": "cybersecurity_advisory",
        "classification": "public"
      }
    }
  ],
  "search_metadata": {
    "sources_searched": ["CISA", "FBI"],
    "embedding_model": "AWS_Titan_V2",
    "min_score_threshold": 0.6,
    "search_backend": "Aurora_pgvector"
  }
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