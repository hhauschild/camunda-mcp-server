# Security Policy

## Supported Versions

We actively support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability, please follow these steps:

### For Security Issues

**Please do NOT create a public GitHub issue for security vulnerabilities.**

Instead, please:

1. **Email us directly** at [your-email@domain.com] with:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if you have one)

2. **Allow time for response** - We aim to respond within 48 hours

3. **Coordinate disclosure** - We'll work with you to understand and fix the issue before public disclosure

### What to Report

Please report any of the following:

- **Authentication bypass** - Issues with Camunda authentication
- **Credential exposure** - Unintended exposure of passwords/tokens
- **Code injection** - Ability to execute arbitrary code
- **Path traversal** - Access to files outside intended scope
- **Denial of service** - Crashes or resource exhaustion
- **Information disclosure** - Unauthorized access to sensitive data

### Security Best Practices

When using this MCP server:

#### Environment Security
- **Never commit** `.env` files or credentials to version control
- **Use environment variables** or secure vaults for credentials
- **Restrict network access** to Camunda servers when possible
- **Use HTTPS** for production Camunda connections

#### Authentication
- **Use strong passwords** for Camunda accounts
- **Consider OAuth** instead of basic authentication
- **Rotate credentials** regularly
- **Use least-privilege** service accounts

#### Deployment Security
- **Run containers** as non-root users (already configured)
- **Limit container resources** to prevent DoS
- **Use read-only filesystems** where possible
- **Keep dependencies updated**

#### MCP Server Security
- **Validate all inputs** from AI assistants
- **Sanitize outputs** before returning to AI
- **Log security events** for monitoring
- **Use secure communication** (stdio protocol is secure by design)

### Example Secure Configuration

```json
{
  "camunda-mcp-server": {
    "type": "stdio",
    "command": "docker",
    "args": ["exec", "-i", "camunda-mcp-server", "python", "-m", "src.server"],
    "env": {
      "CAMUNDA_URL": "https://secure-camunda.company.com/engine-rest",
      "CAMUNDA_AUTH_TYPE": "oauth"
    }
  }
}
```

### Security Updates

- Security patches will be released as soon as possible
- Critical vulnerabilities will be patched within 48 hours
- Users will be notified via GitHub releases and security advisories
- We recommend enabling GitHub security alerts for this repository

### Responsible Disclosure Timeline

1. **Day 0**: Vulnerability reported
2. **Day 1-2**: Initial response and assessment
3. **Day 3-14**: Fix development and testing
4. **Day 14-30**: Coordinated disclosure and patch release
5. **Day 30+**: Public disclosure (if fix is available)

### Bug Bounty

We don't currently offer a formal bug bounty program, but we greatly appreciate security researchers who help improve our project's security.

### Contact

For security-related questions or concerns:
- **Security issues**: [your-security-email@domain.com]
- **General questions**: Create a GitHub issue with the "security" label

Thank you for helping keep the Camunda MCP Server secure!