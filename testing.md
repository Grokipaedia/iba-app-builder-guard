# Testing iba-app-builder-guard

No terminal required. Test in your browser in 3 minutes using Google Colab.

---

## Browser Test — Google Colab

**Step 1** — Open [colab.research.google.com](https://colab.research.google.com) · New notebook

**Step 2** — Run Cell 1:
```python
!pip install pyyaml
```

**Step 3** — Run Cell 2 — create the app build certificate:
```python
iba_yaml = """
intent:
  description: "Build a prototype todo app with local storage only. No auth. No database. No production deployment."

scope:
  - frontend
  - component
  - ui
  - prototype
  - local
  - mock
  - landing
  - dashboard
  - generate
  - build
  - create
  - todo
  - list

denied:
  - authentication
  - auth system
  - database
  - postgresql
  - stripe
  - payment
  - external_api
  - user_data
  - secrets

default_posture: DENY_ALL

kill_threshold: "production_deploy | production-deployment | payment | authentication_system"

temporal_scope:
  hard_expiry: "2026-12-31"
"""

with open(".iba.yaml", "w") as f:
    f.write(iba_yaml)

print("App build certificate written.")
```

**Step 4** — Run Cell 3 — run the guard:
```python
import json, yaml, os, time
from datetime import datetime, timezone

class IBABlockedError(Exception): pass
class IBATerminatedError(Exception): pass

class IBAAppBuilderGuard:
    def __init__(self):
        self.terminated = False
        self.action_count = 0
        self.block_count = 0
        self.components = []
        self.session_id = f"appbuild-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
        with open(".iba.yaml") as f:
            cfg = yaml.safe_load(f)
        self.scope = [s.lower() for s in cfg.get("scope", [])]
        self.denied = [d.lower() for d in cfg.get("denied", [])]
        self.kill_threshold = [t.strip().lower() for t in str(cfg.get("kill_threshold","")).split("|")]
        self.default_posture = cfg.get("default_posture", "DENY_ALL")
        print(f"✅ IBA App Builder Guard loaded · Session: {self.session_id}")
        print(f"   Scope  : {', '.join(self.scope)}")
        print(f"   Denied : {', '.join(self.denied)}\n")

    def check_action(self, action):
        if self.terminated:
            raise IBATerminatedError("Build session terminated.")
        self.action_count += 1
        a = action.lower()

        if any(k in a for k in self.kill_threshold if k):
            self.terminated = True
            print(f"  ✗ TERMINATE [{action}]\n    → Kill threshold — build session ended")
            raise IBATerminatedError(f"Kill threshold: {action}")

        if any(d in a for d in self.denied if d):
            self.block_count += 1
            print(f"  ✗ BLOCKED   [{action}]\n    → Component in denied list")
            raise IBABlockedError(f"Denied: {action}")

        if self.scope and not any(s in a for s in self.scope):
            if self.default_posture == "DENY_ALL":
                self.block_count += 1
                print(f"  ✗ BLOCKED   [{action}]\n    → Outside declared app scope (DENY_ALL)")
                raise IBABlockedError(f"Out of scope: {action}")

        print(f"  ✓ ALLOWED   [{action}]")
        self.components.append(action)
        return True

guard = IBAAppBuilderGuard()

scenarios = [
    "Generate todo list UI component",
    "Build frontend dashboard with mock data",
    "Create prototype landing page",
    "Add user authentication system",
    "Connect PostgreSQL database",
    "Integrate Stripe payment processing",
    "Deploy application to production-deployment server",
]

for action in scenarios:
    try:
        guard.check_action(action)
    except IBATerminatedError:
        break
    except IBABlockedError:
        pass

print(f"\n{'═'*56}")
print(f"  Actions: {guard.action_count} · Blocked: {guard.block_count} · Built: {len(guard.components)}")
print(f"  Status : {'TERMINATED' if guard.terminated else 'COMPLETE'}")
print(f"{'═'*56}")
```

---

## Expected Output

```
✅ IBA App Builder Guard loaded · Session: appbuild-...

  ✓ ALLOWED   [Generate todo list UI component]
  ✓ ALLOWED   [Build frontend dashboard with mock data]
  ✓ ALLOWED   [Create prototype landing page]
  ✗ BLOCKED   [Add user authentication system]
    → Component in denied list
  ✗ BLOCKED   [Connect PostgreSQL database]
    → Component in denied list
  ✗ TERMINATE [Integrate Stripe payment processing]
    → Kill threshold — build session ended

════════════════════════════════════════════════════════
  Actions: 6 · Blocked: 2 · Built: 3
  Status : TERMINATED
════════════════════════════════════════════════════════
```

---

## With Safe Hollowing

```bash
# Redact high-risk components from build prompt before generation
python guard.py "build a todo app with user auth and stripe" --hollow medium
```

---

## Local Test

```bash
git clone https://github.com/Grokipaedia/iba-app-builder-guard.git
cd iba-app-builder-guard
pip install -r requirements.txt
python guard.py --demo
```

---

## Live Demo

**governinglayer.com/governor-html/**

Edit the cert. Run any app builder action. See the gate fire.

---

IBA Intent Bound Authorization · Patent GB2603013.0 Pending
IBA@intentbound.com · IntentBound.com
