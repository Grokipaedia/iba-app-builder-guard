# iba-app-builder-guard

> **Build apps safely. Human intent declared before the first line of code.**

---

## The Moment

Claude Code just announced routines — scheduled, event-triggered, API-callable agent runs on Anthropic infrastructure. Configure once. Run indefinitely. On a schedule. From an API call. In response to an event.

The agent builds frontend, backend, auth, databases, and publishes — autonomously, without you watching.

Who authorized it to do any of that?

---

## The Gap

Claude Code, Lovable, Bolt, Replit, Emergent, Multica Autopilot, OpenCode, Codex — every prompt-based app builder can now:

- Generate a full-stack application from a single prompt
- Write and deploy authentication systems
- Connect to databases
- Call external APIs
- Publish directly to production
- Run on a schedule without human oversight

**The agent builds what it can build — not what you authorized it to build.**

One prompt. No declared scope. No kill threshold. No audit chain.

---

## The IBA Layer

```
┌─────────────────────────────────────────────────┐
│                HUMAN PRINCIPAL                  │
│   Signs .iba.yaml before the agent builds       │
│   anything                                      │
└───────────────────────┬─────────────────────────┘
                        │  Signed Intent Certificate
                        │  · Declared app scope
                        │  · Permitted components
                        │  · Forbidden: production, auth, payments
                        │  · Kill threshold
                        │  · Session expiry
                        ▼
┌─────────────────────────────────────────────────┐
│         IBA APP BUILDER GUARD                   │
│   Validates certificate before every            │
│   component generation or deployment            │
│                                                 │
│   No cert = No app generation                   │
└───────────────────────┬─────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────┐
│         YOUR APP BUILDER                        │
│   Claude Code · Lovable · Bolt · Replit         │
│   Emergent · Multica Autopilot · OpenCode       │
│   Codex · Hermes · OpenClaw · Any LLM builder  │
└─────────────────────────────────────────────────┘
```

---

## Quick Start

```bash
git clone https://github.com/Grokipaedia/iba-app-builder-guard.git
cd iba-app-builder-guard
pip install -r requirements.txt
python guard.py "build a todo app with user auth" --hollow medium
```

---

## Configuration — .iba.yaml

```yaml
intent:
  description: "Build a prototype todo app with local storage. No auth. No database. No production deployment."

scope:
  - frontend
  - component
  - ui
  - prototype
  - local_storage
  - mock

denied:
  - production_deploy
  - authentication
  - database
  - payment
  - external_api
  - user_data
  - secrets

default_posture: DENY_ALL

kill_threshold: "production_deploy | payment | authentication_system | user_data_collection"

hollowing:
  block_components:
    - auth
    - database
    - payment_integration
    - external_api_calls
    - user_tracking

temporal_scope:
  hard_expiry: "2026-12-31"
  session_max_hours: 4

audit:
  chain: witnessbound
  log_every_component: true
```

---

## Gate Logic

```
Certificate valid?                        → PROCEED
Component outside declared scope?         → BLOCK
Forbidden component requested?            → BLOCK
Kill threshold triggered?                 → TERMINATE + LOG
Production deployment attempted?          → TERMINATE
No certificate present?                   → BLOCK
```

**No cert = No app generation.**

---

## Safe Hollowing

Block high-risk components before generation begins:

```bash
# Light — block production deployment only
python guard.py "build a SaaS dashboard" --hollow light

# Medium — block auth + database + production
python guard.py "build a SaaS dashboard" --hollow medium

# Deep — block all external components
python guard.py "build a SaaS dashboard" --hollow deep
```

The agent cannot generate what was hollowed — even if instructed to.

---

## The App Builder Authorization Events

| Component | Without IBA | With IBA |
|-----------|-------------|---------|
| Generate UI component | Implicit — any framework | Explicit — declared stack only |
| Write authentication system | No boundary exists | FORBIDDEN — BLOCK |
| Connect database | No boundary exists | FORBIDDEN — BLOCK |
| Collect user data | No boundary exists | FORBIDDEN — BLOCK |
| Integrate payments | No boundary exists | KILL THRESHOLD — TERMINATE |
| Deploy to production | No boundary exists | KILL THRESHOLD — TERMINATE |
| Run on schedule (routines) | No boundary exists | Certificate required per routine |
| Call external APIs | No boundary exists | Declared endpoints only |

---

## Claude Code Routines — The New Authorization Gap

Claude Code just shipped routines. Configure once. Run on a schedule. From an API call. In response to an event.

The routine builds, deploys, and modifies — autonomously, indefinitely, without oversight.

```yaml
# Without IBA — a Claude Code routine runs unconstrained
routine:
  trigger: "every Monday 9am"
  prompt: "Update the app with latest features"
  # No declared scope
  # No kill threshold  
  # No audit chain
  # No expiry
```

```yaml
# With IBA — every routine execution requires a valid cert
routine:
  trigger: "every Monday 9am"
  iba_cert: ".iba.yaml"
  # Scope: frontend updates only
  # Kill threshold: production_deploy | auth_change
  # Audit chain: witnessbound
  # Expiry: session only
```

The cert is not a prompt. It cannot be overridden by the routine's output.

---

## Live Demo

**governinglayer.com/governor-html/**

Edit the cert. Run any app builder action. Watch the gate fire — ALLOW · BLOCK · TERMINATE. Sub-1ms gate latency confirmed.

---

## Patent & Standards Record

```
Patent:   GB2603013.0 (Pending) · UK IPO · Filed February 5, 2026
PCT:      150+ countries · Protected until August 2028
IETF:     draft-williams-intent-token-00 · CONFIRMED LIVE
          datatracker.ietf.org/doc/draft-williams-intent-token/
NIST:     13 filings · NIST-2025-0035
NCCoE:    10 filings · AI Agent Identity & Authorization
```

---

## Related Repos

| Repo | Gap closed |
|------|-----------|
| [iba-governor](https://github.com/Grokipaedia/iba-governor) | Full production governance · working implementation |
| [iba-devstack-governor](https://github.com/Grokipaedia/iba-devstack-governor) | Govern the full dev stack |
| [agent-vibe-governor](https://github.com/Grokipaedia/agent-vibe-governor) | Governed vibe coding · token tracking |
| [iba-code-guard](https://github.com/Grokipaedia/iba-code-guard) | They got the commit. They didn't get the cert. |
| [iba-mythos-governor](https://github.com/Grokipaedia/iba-mythos-governor) | Mythos-ready VulnOps governance |

---

## Acquisition Enquiries

IBA Intent Bound Authorization is available for acquisition.

**Jeffrey Williams**
IBA@intentbound.com
IntentBound.com
Patent GB2603013.0 Pending · IETF draft-williams-intent-token-00
