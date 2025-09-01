#!/usr/bin/env python3
"""
Veridano MCP Server Client
Simple MCP client that connects to the Veridano Intelligence Platform
"""

import asyncio
import json
import sys
from typing import Any, Dict, List
import aiohttp
from mcp.server.stdio import stdio_server
from mcp.server import Server
from mcp import types

# Veridano API endpoint - no authentication required
VERIDANO_ENDPOINT = "https://kapnlkosgwhjrzzfpp2ettgh4i0rqrbu.lambda-url.us-east-1.on.aws"

# Initialize MCP server
server = Server("veridano-intelligence")

@server.list_tools()
async def list_tools() -> List[types.Tool]:
    """List available Veridano intelligence tools"""
    return [
        types.Tool(
            name="semantic_search",
            description="Search across 11 U.S. government cybersecurity data sources using semantic similarity",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query for cybersecurity intelligence"
                    },
                    "top_k": {
                        "type": "integer", 
                        "description": "Number of results to return (default: 5)",
                        "default": 5
                    },
                    "min_score": {
                        "type": "number",
                        "description": "Minimum similarity score (0.0-1.0, default: 0.6)",
                        "default": 0.6
                    },
                    "sources": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Specific sources to search: CISA, FBI, NIST, DHS, NSA, USCYBERCOM, White House, NVD, ICS-CERT, US-CERT, FedRAMP"
                    }
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="get_cve_details",
            description="Get detailed information about specific CVE vulnerabilities from NIST NVD",
            inputSchema={
                "type": "object", 
                "properties": {
                    "cve_id": {
                        "type": "string",
                        "description": "CVE identifier (e.g., CVE-2024-1234)"
                    }
                },
                "required": ["cve_id"]
            }
        ),
        types.Tool(
            name="threat_intelligence_summary",
            description="Get summarized threat intelligence for specific threats or attack patterns",
            inputSchema={
                "type": "object",
                "properties": {
                    "threat_type": {
                        "type": "string", 
                        "description": "Type of threat (e.g., ransomware, APT, supply chain)"
                    },
                    "time_range": {
                        "type": "string",
                        "description": "Time range for analysis (e.g., '30_days', '90_days', 'year')",
                        "default": "30_days"
                    }
                },
                "required": ["threat_type"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Execute Veridano intelligence tools"""
    
    try:
        async with aiohttp.ClientSession() as session:
            
            if name == "semantic_search":
                query = arguments.get("query", "")
                top_k = arguments.get("top_k", 5)
                min_score = arguments.get("min_score", 0.6)
                sources = arguments.get("sources", [])
                
                payload = {
                    "action": "semantic_search",
                    "query": query,
                    "top_k": top_k,
                    "min_score": min_score
                }
                
                if sources:
                    payload["sources"] = sources
                
                async with session.post(VERIDANO_ENDPOINT, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        return [types.TextContent(
                            type="text",
                            text=json.dumps(result, indent=2)
                        )]
                    else:
                        error_text = await response.text()
                        return [types.TextContent(
                            type="text", 
                            text=f"Error {response.status}: {error_text}"
                        )]
            
            elif name == "get_cve_details":
                cve_id = arguments.get("cve_id", "")
                
                payload = {
                    "action": "get_cve_details",
                    "cve_id": cve_id
                }
                
                async with session.post(VERIDANO_ENDPOINT, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        return [types.TextContent(
                            type="text",
                            text=json.dumps(result, indent=2)
                        )]
                    else:
                        error_text = await response.text()
                        return [types.TextContent(
                            type="text",
                            text=f"Error {response.status}: {error_text}"
                        )]
            
            elif name == "threat_intelligence_summary":
                threat_type = arguments.get("threat_type", "")
                time_range = arguments.get("time_range", "30_days")
                
                payload = {
                    "action": "threat_intelligence_summary", 
                    "threat_type": threat_type,
                    "time_range": time_range
                }
                
                async with session.post(VERIDANO_ENDPOINT, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        return [types.TextContent(
                            type="text",
                            text=json.dumps(result, indent=2)
                        )]
                    else:
                        error_text = await response.text()
                        return [types.TextContent(
                            type="text",
                            text=f"Error {response.status}: {error_text}"
                        )]
            
            else:
                return [types.TextContent(
                    type="text",
                    text=f"Unknown tool: {name}"
                )]
                
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"Error connecting to Veridano: {str(e)}"
        )]

async def main():
    """Run the Veridano MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())