---
name: Bug Report
about: Report a bug or issue with the Veridano Intelligence Platform
title: '[BUG] '
labels: bug
assignees: ''
---

## Bug Description
A clear and concise description of what the bug is.

## Environment
- **Agent Type**: [e.g., Claude Code, Custom MCP Client, etc.]
- **Veridano Client Version**: [e.g., 1.0.0]
- **Python Version**: [e.g., 3.9.1]
- **Operating System**: [e.g., Ubuntu 20.04, macOS 12.0, Windows 11]

## Steps to Reproduce
1. Go to '...'
2. Execute query '...'
3. Set parameters '...'
4. See error

## Expected Behavior
A clear description of what you expected to happen.

## Actual Behavior
A clear description of what actually happened.

## Error Messages
```
Paste any error messages, stack traces, or logs here
```

## Query Details
- **Query**: `your search query here`
- **Sources**: `[list of sources used]`
- **Parameters**: 
  ```json
  {
    "top_k": 10,
    "min_score": 0.7,
    "sources": ["CISA", "FBI"]
  }
  ```

## Response Time
- **Expected**: `< 500ms`
- **Actual**: `1500ms` or `timeout`

## Network Information
- **Region**: [e.g., us-east-1]
- **Endpoint**: [e.g., https://api.veridano.com/mcp]
- **Network latency to AWS**: [if known]

## Additional Context
Add any other context about the problem here, including:
- Frequency of the issue (always, sometimes, once)
- Time of day when issue occurs
- Related queries that work/don't work
- Any workarounds you've found

## Potential Impact
- [ ] Blocks critical threat intelligence gathering
- [ ] Affects production agent operations  
- [ ] Causes performance degradation
- [ ] Minor inconvenience

## Screenshots
If applicable, add screenshots to help explain your problem.