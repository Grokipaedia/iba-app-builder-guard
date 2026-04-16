# iba-app-builder-guard

**Build apps safely. Human intent required.**

Claude can now generate full apps from a single prompt — complete with frontend, backend, auth, databases, and direct publishing.

This tool adds real cryptographic governance.

Wrap any app-building request with a signed **IBA Intent Certificate** so the generated app can only be used under your exact approved rules.

## Features
- Requires IBA-signed intent before any app generation or deployment
- Enforces scope (research only, no production deployment, no sensitive data, etc.)
- Optional safe hollowing / blocking of high-risk components (auth, databases, external APIs)
- Works with any prompt-based app builder (Claude Code, etc.)

## Quick Start
```bash
git clone https://github.com/Grokipaedia/iba-app-builder-guard.git
cd iba-app-builder-guard
pip install -r requirements.txt
python guard.py "build a todo app with user auth" --hollow medium
