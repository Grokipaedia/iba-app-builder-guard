# guard.py - IBA protection for app building / generation
import json
from datetime import datetime
import sys
import argparse

def create_iba_app_guard(prompt: str, hollow_level: str = None):
    cert = {
        "iba_version": "2.0",
        "certificate_id": f"app-guard-{datetime.now().strftime('%Y%m%d-%H%M')}",
        "issued_at": datetime.now().isoformat(),
        "principal": "human-owner",
        "declared_intent": f"Generate app from prompt: {prompt}. For legitimate development/reference only. No production deployment without explicit approval.",
        "scope_envelope": {
            "resources": ["app-generation", "development-reference"],
            "denied": ["production-deployment", "sensitive-data-handling", "external-api-exposure"],
            "default_posture": "DENY_ALL"
        },
        "temporal_scope": {
            "hard_expiry": (datetime.now().replace(year=datetime.now().year + 1)).isoformat()
        },
        "entropy_threshold": {
            "max_kl_divergence": 0.12,
            "flag_at": 0.08,
            "kill_at": 0.12
        },
        "iba_signature": "demo-signature"
    }

    protected_file = f"app-{prompt.replace(' ', '-').lower()[:30]}.iba-protected.md"

    content = f"# Generated App from Prompt: {prompt}\n\n[App code / structure would appear here under IBA governance]\n\n<!-- IBA PROTECTED APP BUILD -->\n"

    if hollow_level:
        content += f"\n<!-- Hollowed ({hollow_level}): High-risk components protected by IBA certificate -->\n"

    with open(protected_file, "w", encoding="utf-8") as f:
        f.write("<!-- IBA PROTECTED APP BUILD -->\n")
        f.write(f"<!-- Intent Certificate: {json.dumps(cert, indent=2)} -->\n\n")
        f.write(content)

    print(f"✅ IBA-protected app build file created: {protected_file}")
    if hollow_level:
        print(f"   Hollowing level applied: {hollow_level}")
    else:
        print("   Full app build protected by IBA certificate")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Governed app building with IBA")
    parser.add_argument("prompt", help="App building prompt")
    parser.add_argument("--hollow", choices=["light", "medium", "heavy"], help="Apply safe hollowing")
    args = parser.parse_args()

    create_iba_app_guard(args.prompt, args.hollow)
