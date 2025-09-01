#!/usr/bin/env python3
"""
Advanced Threat Monitoring Agent
Demonstrates continuous monitoring and automated alerting capabilities
"""

import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Callable
from dataclasses import dataclass

@dataclass
class ThreatAlert:
    id: str
    title: str
    source: str
    severity: str
    cvss_score: float
    published_date: str
    summary: str
    recommended_action: str

class VeridanoThreatMonitor:
    """Advanced threat monitoring agent with automated alerting"""
    
    def __init__(self, alert_callback: Callable = None):
        self.veridano = None  # Initialize with actual MCP client
        self.alert_callback = alert_callback or self._default_alert_handler
        self.monitoring_active = False
        self.last_check = datetime.now() - timedelta(hours=24)
        
        # Monitoring thresholds
        self.critical_cvss_threshold = 9.0
        self.high_cvss_threshold = 7.0
        self.alert_keywords = [
            "zero-day", "active exploitation", "emergency directive",
            "critical vulnerability", "nation-state", "APT campaign"
        ]
    
    async def start_monitoring(self, interval_minutes: int = 15):
        """Start continuous threat monitoring"""
        
        print(f"🚀 Starting Veridano threat monitoring (check every {interval_minutes} minutes)")
        self.monitoring_active = True
        
        while self.monitoring_active:
            try:
                await self._monitoring_cycle()
                print(f"✅ Monitoring cycle complete - next check in {interval_minutes} minutes")
                await asyncio.sleep(interval_minutes * 60)
                
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
                await asyncio.sleep(60)  # Wait 1 minute on error
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.monitoring_active = False
        print("🛑 Threat monitoring stopped")
    
    async def _monitoring_cycle(self):
        """Execute a single monitoring cycle"""
        
        print(f"\n🔍 Threat monitoring cycle - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        alerts = []
        
        # Check for critical vulnerabilities
        critical_vulns = await self._check_critical_vulnerabilities()
        alerts.extend(critical_vulns)
        
        # Check for emergency directives
        emergency_alerts = await self._check_emergency_directives()
        alerts.extend(emergency_alerts)
        
        # Check for APT activity
        apt_alerts = await self._check_apt_activity()
        alerts.extend(apt_alerts)
        
        # Check for zero-day exploits
        zeroday_alerts = await self._check_zeroday_activity()
        alerts.extend(zeroday_alerts)
        
        # Check for critical infrastructure threats
        infra_alerts = await self._check_infrastructure_threats()
        alerts.extend(infra_alerts)
        
        # Process alerts
        if alerts:
            print(f"🚨 {len(alerts)} new threat alerts detected")
            await self.alert_callback(alerts)
        else:
            print("✅ No new critical threats detected")
        
        self.last_check = datetime.now()
    
    async def _check_critical_vulnerabilities(self) -> List[ThreatAlert]:
        """Check for new critical CVSS 9.0+ vulnerabilities"""
        
        # Mock implementation - replace with actual Veridano call
        print("  🛡️ Checking critical vulnerabilities...")
        
        results = await self._mock_search(
            query="critical vulnerability CVSS score 9.0",
            sources=["NVD", "CISA", "US-CERT"],
            timeframe="last_24_hours"
        )
        
        alerts = []
        for doc in results.get("documents", []):
            cvss = doc.get("cvss_score", 0)
            if cvss >= self.critical_cvss_threshold:
                alert = ThreatAlert(
                    id=doc["id"],
                    title=doc["title"],
                    source=doc["source"],
                    severity="CRITICAL",
                    cvss_score=cvss,
                    published_date=doc["published_date"],
                    summary=doc["content"][:200] + "...",
                    recommended_action="IMMEDIATE patching required"
                )
                alerts.append(alert)
        
        return alerts
    
    async def _check_emergency_directives(self) -> List[ThreatAlert]:
        """Check for new CISA emergency directives"""
        
        print("  🚨 Checking emergency directives...")
        
        results = await self._mock_search(
            query="emergency directive immediate action required",
            sources=["CISA", "DHS"],
            timeframe="last_48_hours"
        )
        
        alerts = []
        for doc in results.get("documents", []):
            if "emergency" in doc["title"].lower():
                alert = ThreatAlert(
                    id=doc["id"],
                    title=doc["title"], 
                    source=doc["source"],
                    severity="EMERGENCY",
                    cvss_score=10.0,  # Max severity for emergency directives
                    published_date=doc["published_date"],
                    summary=doc["content"][:200] + "...",
                    recommended_action="COMPLY immediately - Federal mandate"
                )
                alerts.append(alert)
        
        return alerts
    
    async def _check_apt_activity(self) -> List[ThreatAlert]:
        """Check for new APT/nation-state activity"""
        
        print("  🎯 Checking APT activity...")
        
        results = await self._mock_search(
            query="advanced persistent threat nation-state attribution campaign",
            sources=["NSA", "FBI", "USCYBERCOM"],
            timeframe="last_72_hours"
        )
        
        alerts = []
        for doc in results.get("documents", []):
            if any(keyword in doc["content"].lower() for keyword in ["apt", "nation-state", "attribution"]):
                alert = ThreatAlert(
                    id=doc["id"],
                    title=doc["title"],
                    source=doc["source"], 
                    severity="HIGH",
                    cvss_score=8.5,
                    published_date=doc["published_date"],
                    summary=doc["content"][:200] + "...",
                    recommended_action="Review threat indicators and enhance monitoring"
                )
                alerts.append(alert)
        
        return alerts
    
    async def _check_zeroday_activity(self) -> List[ThreatAlert]:
        """Check for zero-day exploitation reports"""
        
        print("  🕳️ Checking zero-day activity...")
        
        results = await self._mock_search(
            query="zero-day exploit active exploitation in the wild",
            sources=["FBI", "CISA", "US-CERT"],
            timeframe="last_48_hours"
        )
        
        alerts = []
        for doc in results.get("documents", []):
            if "zero-day" in doc["content"].lower():
                alert = ThreatAlert(
                    id=doc["id"],
                    title=doc["title"],
                    source=doc["source"],
                    severity="CRITICAL",
                    cvss_score=9.5,
                    published_date=doc["published_date"],
                    summary=doc["content"][:200] + "...",
                    recommended_action="URGENT - Implement defensive measures immediately"
                )
                alerts.append(alert)
        
        return alerts
    
    async def _check_infrastructure_threats(self) -> List[ThreatAlert]:
        """Check for critical infrastructure threats"""
        
        print("  🏭 Checking infrastructure threats...")
        
        results = await self._mock_search(
            query="critical infrastructure attack energy water transportation",
            sources=["CISA", "DHS", "ICS-CERT"],
            timeframe="last_48_hours"
        )
        
        alerts = []
        for doc in results.get("documents", []):
            if any(sector in doc["content"].lower() for sector in ["energy", "water", "transportation", "manufacturing"]):
                alert = ThreatAlert(
                    id=doc["id"],
                    title=doc["title"],
                    source=doc["source"],
                    severity="HIGH",
                    cvss_score=8.0,
                    published_date=doc["published_date"],
                    summary=doc["content"][:200] + "...",
                    recommended_action="Coordinate with sector security teams"
                )
                alerts.append(alert)
        
        return alerts
    
    async def _mock_search(self, query: str, sources: List[str], timeframe: str) -> Dict[str, Any]:
        """Mock search function - replace with actual Veridano MCP call"""
        
        # This would be replaced with:
        # return await self.veridano.semantic_search(
        #     query=query,
        #     sources=sources, 
        #     timeframe=timeframe,
        #     min_score=0.8
        # )
        
        return {
            "documents": [
                {
                    "id": "MOCK-001",
                    "title": f"Mock threat intelligence for: {query[:50]}...",
                    "content": f"Mock content related to {query}. This would contain actual government intelligence in production.",
                    "source": sources[0] if sources else "MOCK",
                    "cvss_score": 8.5,
                    "published_date": datetime.now().isoformat()
                }
            ],
            "total_results": 1
        }
    
    async def _default_alert_handler(self, alerts: List[ThreatAlert]):
        """Default alert handler - prints to console"""
        
        print(f"\n🚨 THREAT ALERT SUMMARY - {len(alerts)} new threats")
        print("=" * 80)
        
        # Sort alerts by severity
        severity_order = {"EMERGENCY": 0, "CRITICAL": 1, "HIGH": 2, "MEDIUM": 3, "LOW": 4}
        sorted_alerts = sorted(alerts, key=lambda x: severity_order.get(x.severity, 5))
        
        for i, alert in enumerate(sorted_alerts, 1):
            print(f"\n{i}. [{alert.severity}] {alert.title}")
            print(f"   Source: {alert.source}")
            print(f"   CVSS: {alert.cvss_score}")
            print(f"   Published: {alert.published_date}")
            print(f"   Action: {alert.recommended_action}")
            print(f"   Summary: {alert.summary}")
        
        print("\n" + "=" * 80)

class CustomAlertHandler:
    """Example custom alert handler with multiple notification methods"""
    
    def __init__(self):
        self.alert_history = []
    
    async def handle_alerts(self, alerts: List[ThreatAlert]):
        """Custom alert processing with multiple notification channels"""
        
        for alert in alerts:
            # Store in history
            self.alert_history.append(alert)
            
            # Process based on severity
            if alert.severity in ["EMERGENCY", "CRITICAL"]:
                await self._send_urgent_notification(alert)
            elif alert.severity == "HIGH":
                await self._send_standard_notification(alert)
            else:
                await self._log_alert(alert)
    
    async def _send_urgent_notification(self, alert: ThreatAlert):
        """Send urgent notification for critical threats"""
        print(f"📱 URGENT NOTIFICATION: {alert.title}")
        # In production: send to Slack, email, SMS, etc.
        
    async def _send_standard_notification(self, alert: ThreatAlert):
        """Send standard notification"""
        print(f"📧 Standard notification: {alert.title}")
        # In production: send to email, Slack channel, etc.
        
    async def _log_alert(self, alert: ThreatAlert):
        """Log alert for review"""
        print(f"📝 Logged alert: {alert.title}")
        # In production: write to log file, database, etc.

async def example_usage():
    """Demonstrate threat monitoring agent usage"""
    
    # Option 1: Use default alert handler
    monitor = VeridanoThreatMonitor()
    
    # Option 2: Use custom alert handler
    custom_handler = CustomAlertHandler()
    monitor_custom = VeridanoThreatMonitor(alert_callback=custom_handler.handle_alerts)
    
    print("Starting threat monitoring examples...")
    
    # Run a single monitoring cycle
    await monitor._monitoring_cycle()
    
    print("\n✅ Threat monitoring example completed")
    print("In production, call monitor.start_monitoring() for continuous operation")

if __name__ == "__main__":
    asyncio.run(example_usage())