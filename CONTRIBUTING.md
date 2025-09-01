# Contributing to Veridano Intelligence Platform

Thank you for your interest in contributing to the Veridano Intelligence Platform! This document provides guidelines for contributing to our cybersecurity intelligence platform designed for AI agents.

## 🎯 Contribution Focus Areas

### High-Priority Contributions
1. **New Government Data Sources** - Additional USG cybersecurity intelligence feeds
2. **MCP Tool Enhancements** - New search and analysis capabilities for AI agents
3. **Performance Optimizations** - Query optimization and caching improvements
4. **Integration Examples** - Sample agent implementations and use cases
5. **Documentation** - Setup guides, API documentation, troubleshooting

### Medium-Priority Contributions
- Bug fixes and error handling improvements
- Test coverage expansion
- Monitoring and alerting enhancements
- Security hardening

## 🔒 Security Requirements

**IMPORTANT**: Veridano is a defensive cybersecurity platform. We only accept contributions that:

✅ **Allowed:**
- Defensive security tools and capabilities
- Threat intelligence analysis and detection
- Vulnerability research and mitigation guidance
- Compliance and framework documentation
- Security monitoring and alerting systems

❌ **Prohibited:**
- Offensive security tools or exploits
- Malicious code or attack techniques
- Tools that could be used for unauthorized access
- Code that exposes or logs secrets/credentials

All contributions must pass security review before merge.

## 🚀 Getting Started

### Development Environment Setup

1. **Prerequisites**
   ```bash
   python 3.8+
   AWS CLI configured
   Access to Veridano test environment
   ```

2. **Clone and Setup**
   ```bash
   git clone https://github.com/Veridano/veridano-intelligence-platform.git
   cd veridano-intelligence-platform
   pip install -r requirements.txt
   ```

3. **Environment Variables**
   ```bash
   export VERIDANO_TEST_ENDPOINT="https://test-api.veridano.com/mcp"
   export VERIDANO_TEST_CLIENT_ID="test_client_id"
   export VERIDANO_TEST_CLIENT_SECRET="test_client_secret"
   ```

4. **Run Tests**
   ```bash
   python -m pytest tests/ -v
   python examples/basic-agent.py  # Test basic functionality
   ```

## 📝 Contribution Process

### 1. Issue Creation
Before starting work, create an issue describing:
- **Problem/Feature**: What you're trying to solve or add
- **Scope**: Which components will be affected
- **Implementation Plan**: High-level approach
- **Testing Strategy**: How you'll verify the changes

### 2. Development Guidelines

#### Code Standards
- **Language**: Python 3.8+ for backend, HTML/JavaScript for frontend
- **Style**: Follow PEP 8 for Python, use type hints
- **Documentation**: Docstrings for all public functions
- **Error Handling**: Comprehensive exception handling with logging

#### MCP Tool Development
```python
# Example MCP tool implementation
async def new_analysis_tool(
    client: MCPClient,
    query: str,
    analysis_type: str = "threat_landscape",
    sources: List[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    New analysis tool for Veridano MCP server
    
    Args:
        query: Analysis query string
        analysis_type: Type of analysis to perform
        sources: Government sources to include
        **kwargs: Additional parameters
        
    Returns:
        Analysis results in standard Veridano format
        
    Raises:
        MCPError: If analysis fails
        AuthenticationError: If client not authenticated
    """
    
    # Validate inputs
    if not query or len(query.strip()) < 3:
        raise ValueError("Query must be at least 3 characters")
    
    # Implementation
    try:
        # Your analysis logic here
        results = await client.semantic_search(
            query=query,
            sources=sources,
            **kwargs
        )
        
        # Process and enhance results
        enhanced_results = enhance_analysis_results(results, analysis_type)
        
        return enhanced_results
        
    except Exception as e:
        logger.error(f"Analysis tool failed: {e}")
        raise MCPError(f"Analysis failed: {str(e)}")
```

#### Data Source Integration
```python
# Example new data source scraper
class NewGovernmentSourceScraper:
    """Template for new government data source scrapers"""
    
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.processed_count = 0
        self.error_count = 0
    
    async def scrape_latest_content(self, max_documents: int = 50) -> Dict[str, Any]:
        """Main scraping method - must implement this interface"""
        
        # 1. Fetch document listings from government website
        documents = await self.fetch_document_listings()
        
        # 2. Download full content for each document
        processed_docs = []
        for doc in documents[:max_documents]:
            try:
                full_doc = await self.fetch_document_content(doc)
                standardized_doc = self.standardize_document(full_doc)
                
                if await self.save_to_s3(standardized_doc):
                    processed_docs.append(standardized_doc)
                    
            except Exception as e:
                logger.error(f"Failed to process {doc.get('id')}: {e}")
                self.error_count += 1
        
        return {
            "source": self.source_name,
            "processed_count": len(processed_docs),
            "error_count": self.error_count,
            "timestamp": datetime.now().isoformat()
        }
    
    def standardize_document(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """Convert to standard Veridano document format"""
        return {
            "id": doc.get("id", "unknown"),
            "title": doc.get("title", ""),
            "content": doc.get("content", ""),
            "source": self.source_name,
            "category": doc.get("category", "government_intelligence"),
            "document_type": doc.get("type", "advisory"),
            "url": doc.get("url", ""),
            "published_date": doc.get("published_date"),
            "metadata": {
                "scrape_timestamp": datetime.now().isoformat(),
                "content_length": len(doc.get("content", "")),
                "original_format": doc.get("format", "html")
            }
        }
```

### 3. Testing Requirements

#### Unit Tests
```python
import pytest
from unittest.mock import Mock, patch

class TestNewAnalysisTool:
    @pytest.mark.asyncio
    async def test_basic_analysis(self):
        """Test basic analysis functionality"""
        
        # Mock MCP client
        mock_client = Mock()
        mock_client.semantic_search.return_value = {
            "documents": [{"id": "test", "title": "Test", "content": "Test content"}],
            "total_results": 1
        }
        
        # Test the tool
        result = await new_analysis_tool(
            client=mock_client,
            query="test query",
            analysis_type="threat_landscape"
        )
        
        assert result is not None
        assert "documents" in result
        mock_client.semantic_search.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_invalid_query(self):
        """Test error handling for invalid queries"""
        
        mock_client = Mock()
        
        with pytest.raises(ValueError):
            await new_analysis_tool(
                client=mock_client,
                query="",  # Invalid empty query
                analysis_type="threat_landscape"
            )
```

#### Integration Tests
```python
@pytest.mark.integration
class TestVeridanoIntegration:
    @pytest.mark.asyncio
    async def test_real_search_functionality(self):
        """Test against real Veridano test environment"""
        
        client = VeridanoMCPClient(
            endpoint=os.getenv("VERIDANO_TEST_ENDPOINT"),
            client_id=os.getenv("VERIDANO_TEST_CLIENT_ID"),
            client_secret=os.getenv("VERIDANO_TEST_CLIENT_SECRET")
        )
        
        # Test basic search
        result = await client.semantic_search(
            query="test cybersecurity intelligence",
            top_k=1
        )
        
        assert result["total_results"] >= 0
        assert "documents" in result
        assert "timestamp" in result
```

### 4. Pull Request Process

#### PR Checklist
- [ ] Issue linked to PR
- [ ] Code follows project style guidelines
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Documentation updated
- [ ] Security review completed
- [ ] Performance impact assessed

#### PR Template
```markdown
## Summary
Brief description of changes

## Related Issue
Fixes #[issue number]

## Changes Made
- [ ] Added new MCP tool: `tool_name`
- [ ] Enhanced existing functionality
- [ ] Fixed bug in component X
- [ ] Updated documentation

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass  
- [ ] Manual testing completed
- [ ] Performance benchmarks run

## Security Review
- [ ] No sensitive data exposed
- [ ] Input validation implemented
- [ ] Authentication/authorization preserved
- [ ] Defensive security only

## Performance Impact
- Query response time: +/- X ms
- Memory usage: +/- X MB
- New dependencies: [list any new dependencies]

## Documentation Updates
- [ ] API documentation updated
- [ ] Examples updated
- [ ] Setup guide updated
- [ ] Performance guide updated
```

## 📊 New Data Source Guidelines

### Data Source Evaluation Criteria
1. **Authority**: Official U.S. government cybersecurity source
2. **Relevance**: Contains actionable threat intelligence
3. **Accessibility**: Publicly available or authorized for platform use
4. **Quality**: Structured, reliable, and regularly updated
5. **Volume**: Sufficient content to justify integration effort

### Implementation Requirements
1. **Scraper Architecture**: Follow existing scraper patterns
2. **Data Standardization**: Convert to standard Veridano document format
3. **Error Handling**: Robust error handling and retry logic
4. **Rate Limiting**: Respect source website rate limits
5. **Scheduling**: Appropriate update frequency for content type
6. **Testing**: Comprehensive testing with real data

### Example Data Sources (Future Consideration)
- **CERT/CC** - Computer Emergency Response Team Coordination Center
- **MS-ISAC** - Multi-State Information Sharing and Analysis Center  
- **ENISA** - European Network and Information Security Agency (if relevant)
- **MITRE ATT&CK** - Tactics, techniques, and procedures framework
- **STIX/TAXII** - Structured threat information feeds

## 🤝 Community Guidelines

### Code of Conduct
- **Professional**: Maintain professional cybersecurity focus
- **Collaborative**: Work together to improve platform capabilities
- **Security-First**: Always prioritize defensive security applications
- **Quality**: Ensure high-quality, production-ready contributions

### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and design discussions
- **Email**: enterprise@veridano.com for sensitive security discussions
- **Discord**: Community chat and real-time collaboration

### Review Process
1. **Security Review**: All PRs undergo security review
2. **Code Review**: Technical review by maintainers
3. **Testing**: Automated and manual testing validation
4. **Documentation**: Ensure adequate documentation
5. **Performance**: Performance impact assessment

## 🏆 Recognition

Contributors who make significant contributions will be:
- Recognized in the project README
- Invited to contribute to roadmap planning
- Given priority access to new features
- Eligible for Veridano contributor rewards program

## 📞 Getting Help

### Before Contributing
- Review existing issues and PRs
- Check documentation for similar functionality
- Test your development environment setup
- Join our Discord for real-time discussion

### During Development
- Ask questions in GitHub Discussions
- Request guidance on implementation approach
- Share work-in-progress for early feedback
- Coordinate with other contributors

### After Submission
- Respond to review feedback promptly
- Update PR based on review comments
- Participate in testing and validation
- Help with documentation updates

## 📋 Contributor License Agreement

By contributing to Veridano, you agree that:
1. Your contributions are your original work or properly licensed
2. You grant Veridano rights to use your contributions
3. Your contributions follow defensive security principles
4. You will not contribute malicious or offensive security code

---

**Ready to contribute?** Start by browsing our [good first issues](https://github.com/Veridano/veridano-intelligence-platform/labels/good%20first%20issue) or proposing a new data source integration!