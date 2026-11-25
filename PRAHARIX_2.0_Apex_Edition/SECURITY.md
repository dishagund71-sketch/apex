# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| 2.0.x (Apex Edition) | ✅ Active |
| 1.x | ❌ End of life |

## Reporting a Vulnerability

**Do NOT open a public GitHub issue for security vulnerabilities.**

If you discover a security vulnerability in PRAHARIX 2.0, please:

1. **Email the maintainers directly** (see repository contacts).
2. Include a clear description of the vulnerability, steps to reproduce, and potential impact.
3. We will acknowledge receipt within **48 hours** and provide a timeline for a fix.

## Security Best Practices for Deployment

- Always generate a **new `SECRET_KEY`** for production:
  ```bash
  python -c "import secrets; print(secrets.token_hex(32))"
  ```
- Set `SESSION_COOKIE_SECURE=True` when running over HTTPS.
- Use strong passwords for `ADMIN_PASSWORD` and `USER_PASSWORD`.
- Never expose `FLASK_DEBUG=True` in production.
- Restrict network access to the application port.
- Rotate credentials regularly.
- Do **not** commit `.env` files to version control.
