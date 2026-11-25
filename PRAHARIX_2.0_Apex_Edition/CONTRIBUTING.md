# Contributing to PRAHARIX 2.0 Apex Edition

Thank you for your interest in contributing! 🎉

## How to Contribute

### 1. Fork & Clone

```bash
git clone https://github.com/YOUR_USERNAME/PRAHARIX_2.0_Apex_Edition.git
cd PRAHARIX_2.0_Apex_Edition
```

### 2. Create a Branch

Use a descriptive branch name:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 3. Set Up Your Environment

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows PowerShell
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your local values
```

### 4. Make Your Changes

- Follow **PEP 8** Python style guidelines.
- Keep functions focused and well-documented with docstrings.
- Do not commit `.env`, `*.db`, `__pycache__/`, or generated PDFs.
- Test your changes locally before submitting.

### 5. Commit & Push

```bash
git add .
git commit -m "feat: add SAR zone priority scoring"
git push origin feature/your-feature-name
```

### 6. Open a Pull Request

- Target the `main` branch.
- Describe what you changed and why.
- Reference any related issues.

---

## Code Style

- Python 3.11+
- Docstrings for all public functions and classes
- Type hints encouraged
- Keep modules focused on their domain (e.g., `sar_module.py` for SAR only)

## Reporting Bugs

Open a GitHub Issue with:
- Steps to reproduce
- Expected vs. actual behavior
- Python version and OS
- Any relevant log output

## Security Issues

For security vulnerabilities, **do not open a public issue.** Contact the maintainers directly.
