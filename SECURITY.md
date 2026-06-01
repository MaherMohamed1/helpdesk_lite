# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in HelpDesk Lite, please email us instead of using the issue tracker.

Please include the following in your report:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if available)

We will acknowledge your report within 48 hours and provide a detailed response within 5 business days.

## Supported Versions

| Version | Supported |
| --- | --- |
| Latest | ✅ |
| Earlier versions | ⚠️ Community supported |

## Security Best Practices

When deploying HelpDesk Lite:

1. **Always use HTTPS** in production
2. **Change the SECRET_KEY** - never use the default value
3. **Keep dependencies updated** - run `pip install --upgrade -r requirements.txt` regularly
4. **Use strong database passwords** if using a networked database
5. **Validate and sanitize user input** - the application has built-in protections, but always be cautious
6. **Run behind a reverse proxy** like Nginx in production
7. **Enable CSRF protection** - Flask handles this by default
8. **Set secure headers** - consider using Flask extensions like Flask-Talisman

## Known Issues

None currently reported. Please report any security concerns responsibly.
