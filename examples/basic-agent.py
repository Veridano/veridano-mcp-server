#!/usr/bin/env python3
"""
Basic Veridano Intelligence Agent Example
Demonstrates core functionality for cybersecurity intelligence queries
"""

import asyncio
import os
from typing import List, Dict, Any

# Mock MCP client - replace with actual mcp_client library
class VeridanoMCPClient:
    def __init__(self, endpoint: str, client_id: str, client_secret: str):
        self.endpoint = endpoint
        self.client_id = client_id  
        self.client_secret = client_secret
        self.authenticated = False
    
    async def connect(self):
        """Establish connection to Veridano MCP server"""
        print("🔗 Connecting to Veridano Intelligence Platform...")
        # Authentication logic would go here
        self.authenticated = True
        print("✅ Connected successfully")
    
    async def semantic_search(self, query: str, sources: List[str] = None, 
                            top_k: int = 10, min_score: float = 0.7) -> Dict[str, Any]:
        """Perform semantic search across government intelligence"""
        if not self.authenticated:
            await self.connect()
        
        # In real implementation, this would make HTTP request to MCP server
        print(f"🔍 Searching: '{query}' across {sources or 'all sources'}")
        
        # Mock response structure
        return {
            "documents": [
                {
                    "id": "AA24-131A",
                    "title": "CISA Analysis of Ransomware Trends and Tactics",
                    "content": "Comprehensive analysis of ransomware trends including double extortion, supply chain targeting, and critical infrastructure attacks...",
                    "source": "CISA",
                    "category": "threat_intelligence",
                    "score": 0.94,
                    "published_date": "2024-05-10T00:00:00Z"
                }
            ],
            "total_results": 1,
            "query": query,
            "timestamp": "2025-09-01T01:30:00Z"
        }
    
    async def vulnerability_lookup(self, cve_id: str = None, keywords: str = None,
                                 cvss_min: float = 0.0) -> Dict[str, Any]:
        """Look up specific vulnerabilities from NVD"""
        if not self.authenticated:
            await self.connect()
            
        search_term = cve_id or keywords
        print(f"🛡️ Looking up vulnerability: {search_term}")
        
        # Mock response
        return {
            "documents": [
                {
                    "id": "CVE-2024-38063",
                    "title": "Windows TCP/IP Remote Code Execution Vulnerability",
                    "content": "A remote code execution vulnerability exists in Windows TCP/IP...",
                    "source": "NVD", 
                    "cvss_score": 9.8,
                    "published_date": "2024-07-09T00:00:00Z"
                }
            ],
            "total_results": 1
        }

class CybersecurityIntelligenceAgent:
    """Example AI agent using Veridano for cybersecurity intelligence"""
    
    def __init__(self):
        self.veridano = VeridanoMCPClient(
            endpoint=os.getenv("VERIDANO_ENDPOINT", "https://api.veridano.com/mcp"),
            client_id=os.getenv("VERIDANO_CLIENT_ID"),
            client_secret=os.getenv("VERIDANO_CLIENT_SECRET")
        )
    
    async def research_threat_actor(self, actor_name: str) -> Dict[str, Any]:
        """Research a specific threat actor across all intelligence sources"""
        
        print(f"\n🎯 Researching threat actor: {actor_name}")
        
        # Search for threat intelligence
        intel_results = await self.veridano.semantic_search(
            query=f"{actor_name} tactics techniques procedures campaign",
            sources=["NSA", "FBI", "USCYBERCOM", "CISA"],
            top_k=15,
            min_score=0.8
        )
        
        # Search for associated vulnerabilities
        vuln_results = await self.veridano.semantic_search(
            query=f"{actor_name} exploit vulnerability CVE",
            sources=["NVD", "CISA", "FBI"], 
            top_k=10,
            min_score=0.75
        )
        
        # Search for mitigation guidance
        mitigation_results = await self.veridano.semantic_search(
            query=f"{actor_name} mitigation defense countermeasures",
            sources=["CISA", "NIST", "NSA"],
            top_k=8,
            min_score=0.7
        )
        
        # Compile comprehensive intelligence report
        report = {
            "threat_actor": actor_name,
            "intelligence_summary": {
                "total_documents": (intel_results["total_results"] + 
                                  vuln_results["total_results"] + 
                                  mitigation_results["total_results"]),
                "threat_intelligence": intel_results["documents"],
                "associated_vulnerabilities": vuln_results["documents"],
                "mitigation_guidance": mitigation_results["documents"]
            },
            "key_findings": self._extract_key_findings(intel_results["documents"]),
            "risk_assessment": self._assess_threat_level(intel_results["documents"]),
            "recommended_actions": self._generate_recommendations(mitigation_results["documents"]),
            "report_timestamp": "2025-09-01T01:30:00Z"
        }
        
        return report
    
    async def analyze_vulnerability(self, cve_id: str) -> Dict[str, Any]:
        """Analyze a specific CVE across all relevant sources"""
        
        print(f"\n🛡️ Analyzing vulnerability: {cve_id}")
        
        # Get official CVE details
        nvd_results = await self.veridano.vulnerability_lookup(cve_id=cve_id)
        
        # Search for government guidance
        guidance_results = await self.veridano.semantic_search(
            query=f"{cve_id} mitigation patch guidance",
            sources=["CISA", "NIST", "US-CERT"],
            top_k=10
        )
        
        # Check for threat actor exploitation
        exploitation_results = await self.veridano.semantic_search(
            query=f"{cve_id} active exploitation threat actor",
            sources=["FBI", "NSA", "USCYBERCOM"],
            top_k=8
        )
        
        analysis = {
            "cve_id": cve_id,
            "official_details": nvd_results["documents"],
            "government_guidance": guidance_results["documents"],
            "exploitation_intelligence": exploitation_results["documents"],
            "severity_assessment": self._assess_vulnerability_severity(nvd_results["documents"]),
            "recommended_priority": self._calculate_priority(nvd_results["documents"], exploitation_results["documents"]),
            "analysis_timestamp": "2025-09-01T01:30:00Z"
        }
        
        return analysis
    
    async def monitor_sector_threats(self, sector: str) -> Dict[str, Any]:
        """Monitor threats specific to a critical infrastructure sector"""
        
        print(f"\n🏭 Monitoring {sector} sector threats...")
        
        # Sector-specific threat intelligence
        sector_threats = await self.veridano.semantic_search(
            query=f"{sector} sector cybersecurity threats attack",
            sources=["CISA", "DHS", "ICS-CERT"],
            top_k=20,
            min_score=0.75
        )
        
        # Industrial control systems threats (if applicable)
        ics_threats = await self.veridano.semantic_search(
            query=f"{sector} industrial control systems SCADA vulnerability",
            sources=["ICS-CERT", "CISA"],
            top_k=10,
            min_score=0.7
        )
        
        # Recent policy changes
        policy_updates = await self.veridano.semantic_search(
            query=f"{sector} cybersecurity policy executive order directive",
            sources=["White House", "DHS"],
            top_k=5,
            min_score=0.8
        )
        
        monitoring_report = {
            "sector": sector,
            "threat_landscape": {
                "general_threats": sector_threats["documents"],
                "ics_specific_threats": ics_threats["documents"], 
                "policy_updates": policy_updates["documents"]
            },
            "threat_level": self._assess_sector_risk(sector_threats["documents"]),
            "priority_actions": self._identify_sector_priorities(sector_threats["documents"]),
            "monitoring_timestamp": "2025-09-01T01:30:00Z"
        }
        
        return monitoring_report
    
    def _extract_key_findings(self, documents: List[Dict]) -> List[str]:
        """Extract key findings from intelligence documents"""
        findings = []
        for doc in documents[:5]:  # Top 5 most relevant
            # Extract first sentence or key bullet point
            content = doc.get("content", "")
            if content:
                first_sentence = content.split('.')[0] + '.'
                findings.append(f"{doc['source']}: {first_sentence}")
        return findings
    
    def _assess_threat_level(self, documents: List[Dict]) -> str:
        """Assess overall threat level based on intelligence"""
        if not documents:
            return "UNKNOWN"
        
        # Simple scoring based on document count and recency
        recent_docs = len([d for d in documents if "2024" in d.get("published_date", "")])
        
        if recent_docs >= 5:
            return "HIGH"
        elif recent_docs >= 2:
            return "MEDIUM" 
        else:
            return "LOW"
    
    def _generate_recommendations(self, mitigation_docs: List[Dict]) -> List[str]:
        """Generate actionable recommendations from mitigation guidance"""
        recommendations = []
        for doc in mitigation_docs[:3]:
            content = doc.get("content", "")
            if "recommend" in content.lower():
                # Extract recommendation sentences
                sentences = content.split('.')
                for sentence in sentences:
                    if "recommend" in sentence.lower():
                        recommendations.append(sentence.strip() + '.')
                        break
        return recommendations
    
    def _assess_vulnerability_severity(self, nvd_docs: List[Dict]) -> str:
        """Assess vulnerability severity"""
        if not nvd_docs:
            return "UNKNOWN"
        
        cvss_score = nvd_docs[0].get("cvss_score", 0)
        if cvss_score >= 9.0:
            return "CRITICAL"
        elif cvss_score >= 7.0:
            return "HIGH"
        elif cvss_score >= 4.0:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _calculate_priority(self, nvd_docs: List[Dict], exploit_docs: List[Dict]) -> str:
        """Calculate patching priority based on CVE and exploitation intelligence"""
        cvss = nvd_docs[0].get("cvss_score", 0) if nvd_docs else 0
        exploitation = len(exploit_docs) > 0
        
        if cvss >= 9.0 and exploitation:
            return "EMERGENCY"
        elif cvss >= 7.0 and exploitation:
            return "HIGH"
        elif cvss >= 7.0 or exploitation:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _assess_sector_risk(self, threat_docs: List[Dict]) -> str:
        """Assess risk level for a specific sector"""
        if not threat_docs:
            return "LOW"
        
        # Count recent, high-severity threats
        recent_threats = [d for d in threat_docs if "2024" in d.get("published_date", "")]
        critical_keywords = ["critical", "emergency", "immediate", "active exploitation"]
        
        critical_count = sum(1 for doc in recent_threats 
                           if any(keyword in doc.get("content", "").lower() 
                                for keyword in critical_keywords))
        
        if critical_count >= 3:
            return "CRITICAL"
        elif critical_count >= 1 or len(recent_threats) >= 5:
            return "HIGH"
        elif len(recent_threats) >= 2:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _identify_sector_priorities(self, threat_docs: List[Dict]) -> List[str]:
        """Identify priority actions for a sector"""
        priorities = []
        
        for doc in threat_docs[:3]:
            content = doc.get("content", "")
            title = doc.get("title", "")
            
            if "emergency" in title.lower():
                priorities.append(f"URGENT: Review {doc['source']} emergency guidance - {title}")
            elif "critical" in content.lower():
                priorities.append(f"HIGH: Implement {doc['source']} security recommendations")
            else:
                priorities.append(f"MEDIUM: Monitor {doc['source']} threat developments")
        
        return priorities

async def main():
    """Example usage of the Cybersecurity Intelligence Agent"""
    
    # Initialize agent
    agent = CybersecurityIntelligenceAgent()
    
    try:
        # Example 1: Research threat actor
        print("=" * 60)
        print("EXAMPLE 1: Threat Actor Research")
        print("=" * 60)
        
        apt_report = await agent.research_threat_actor("APT29")
        print(f"📊 Research complete - {apt_report['intelligence_summary']['total_documents']} documents analyzed")
        print(f"🎯 Key findings: {len(apt_report['key_findings'])} critical insights")
        print(f"⚠️ Risk level: {apt_report['risk_assessment']}")
        
        # Example 2: Vulnerability analysis
        print("\n" + "=" * 60)
        print("EXAMPLE 2: Vulnerability Analysis") 
        print("=" * 60)
        
        vuln_analysis = await agent.analyze_vulnerability("CVE-2024-38063")
        print(f"🛡️ Analysis complete for CVE-2024-38063")
        print(f"📈 Severity: {vuln_analysis['severity_assessment']}")
        print(f"🚨 Priority: {vuln_analysis['recommended_priority']}")
        
        # Example 3: Sector monitoring
        print("\n" + "=" * 60)
        print("EXAMPLE 3: Critical Infrastructure Monitoring")
        print("=" * 60)
        
        energy_report = await agent.monitor_sector_threats("energy")
        print(f"🏭 Energy sector monitoring complete")
        print(f"📊 Threat level: {energy_report['threat_level']}")
        print(f"📋 Priority actions: {len(energy_report['priority_actions'])}")
        
        print("\n✅ All examples completed successfully!")
        
    except Exception as e:
        print(f"❌ Agent execution failed: {e}")

if __name__ == "__main__":
    # Ensure required environment variables are set
    required_vars = ["VERIDANO_CLIENT_ID", "VERIDANO_CLIENT_SECRET"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set the following:")
        for var in missing_vars:
            print(f"  export {var}='your_value_here'")
        exit(1)
    
    # Run the example
    asyncio.run(main())