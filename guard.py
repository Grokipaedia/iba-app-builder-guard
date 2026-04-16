# guard.py - IBA Intent Bound Authorization · App Builder Guard
# Patent GB2603013.0 (Pending) · UK IPO · Filed February 5, 2026
# IETF draft-williams-intent-token-00 · intentbound.com
#
# Build apps safely. Human intent declared before the first line of code.
# Works with Claude Code routines, Lovable, Bolt, Replit, Emergent,
# Multica Autopilot, OpenCode, Codex, Hermes, OpenClaw.

import json
import yaml
import os
import sys
import time
import argparse
from datetime import datetime, timezone


class IBABlockedError(Exception):
    """Raised when an app builder action is blocked by the IBA gate."""
    pass


class IBATerminatedError(Exception):
    """Raised when the app build session is terminated by the IBA gate."""
    pass


HOLLOW_LEVELS = {
    "light": ["production_deploy", "production-deployment"],
    "medium": ["production_deploy", "production-deployment",
               "authentication", "auth_system", "database",
               "user_data", "user_tracking"],
    "deep":   ["production_deploy", "production-deployment",
               "authentication", "auth_system", "database",
               "user_data", "user_tracking", "external_api",
               "payment", "secrets", "credentials"],
}


class IBAAppBuilderGuard:
    """
    IBA enforcement layer for prompt-based app builders.
    Reads .iba.yaml, validates every build action against declared scope,
    blocks unauthorized components, terminates on production/payment actions.
    Writes immutable audit chain to app-audit.jsonl.

    Compatible with Claude Code routines, Lovable, Bolt, Replit,
    Emergent, Multica Autopilot, OpenCode, Codex, Hermes, OpenClaw.
    """

    def __init__(self, config_path=".iba.yaml", audit_path="app-audit.jsonl"):
        self.config_path = config_path
        self.audit_path = audit_path
        self.terminated = False
        self.session_id = f"appbuild-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
        self.action_count = 0
        self.block_count = 0
        self.components_built = []

        self.config = self._load_config()
        self.scope        = [s.lower() for s in self.config.get("scope", [])]
        self.denied       = [d.lower() for d in self.config.get("denied", [])]
        self.default_posture = self.config.get("default_posture", "DENY_ALL")
        self.kill_threshold  = self.config.get("kill_threshold", None)
        self.hard_expiry     = self.config.get("temporal_scope", {}).get("hard_expiry", None)
        self.hollowing       = self.config.get("hollowing", {})

        self._log_event("SESSION_START", "IBA App Builder Guard initialised", "ALLOW")
        self._print_header()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            print(f"⚠️  No {self.config_path} found — creating default DENY_ALL config")
            default = {
                "intent": {"description": "No app build intent declared — DENY_ALL posture active"},
                "scope": [],
                "denied": [],
                "default_posture": "DENY_ALL",
            }
            with open(self.config_path, "w") as f:
                yaml.dump(default, f)
            return default
        with open(self.config_path) as f:
            return yaml.safe_load(f)

    def _print_header(self):
        intent = self.config.get("intent", {})
        desc = intent.get("description", "No intent declared") if isinstance(intent, dict) else str(intent)
        print("\n" + "═" * 64)
        print("  IBA APP BUILDER GUARD · Intent Bound Authorization")
        print("  Patent GB2603013.0 Pending · intentbound.com")
        print("═" * 64)
        print(f"  Session   : {self.session_id}")
        print(f"  Intent    : {desc[:55]}...")
        print(f"  Posture   : {self.default_posture}")
        print(f"  Scope     : {', '.join(self.scope) if self.scope else 'NONE'}")
        print(f"  Denied    : {', '.join(self.denied) if self.denied else 'NONE'}")
        if self.hard_expiry:
            print(f"  Expires   : {self.hard_expiry}")
        if self.kill_threshold:
            print(f"  Kill      : {self.kill_threshold}")
        print("═" * 64 + "\n")

    def _is_expired(self):
        if not self.hard_expiry:
            return False
        try:
            expiry = datetime.fromisoformat(str(self.hard_expiry))
            if expiry.tzinfo is None:
                expiry = expiry.replace(tzinfo=timezone.utc)
            return datetime.now(timezone.utc) > expiry
        except Exception:
            return False

    def _match_scope(self, action: str) -> bool:
        return any(s in action.lower() for s in self.scope)

    def _match_denied(self, action: str) -> bool:
        return any(d in action.lower() for d in self.denied)

    def _match_kill_threshold(self, action: str) -> bool:
        if not self.kill_threshold:
            return False
        thresholds = [t.strip().lower() for t in str(self.kill_threshold).split("|")]
        return any(t in action.lower() for t in thresholds)

    def _log_event(self, event_type: str, action: str, verdict: str, reason: str = ""):
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": self.session_id,
            "event_type": event_type,
            "action": action[:200],
            "verdict": verdict,
            "reason": reason,
        }
        with open(self.audit_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def check_action(self, action: str) -> bool:
        """
        Gate check. Call before every app builder action.
        Returns True if permitted.
        Raises IBABlockedError if blocked.
        Raises IBATerminatedError if kill threshold triggered.
        """
        if self.terminated:
            raise IBATerminatedError("App build session terminated. Reset certificate to continue.")

        self.action_count += 1
        start = time.perf_counter()

        # 1. Expiry
        if self._is_expired():
            self._log_event("BLOCK", action, "BLOCK", "Certificate expired")
            self.block_count += 1
            print(f"  ✗ BLOCKED  [{action[:62]}]\n    → Certificate expired")
            raise IBABlockedError(f"Certificate expired: {action}")

        # 2. Kill threshold
        if self._match_kill_threshold(action):
            self._log_event("TERMINATE", action, "TERMINATE", "Kill threshold triggered")
            self.terminated = True
            print(f"  ✗ TERMINATE [{action[:60]}]\n    → Kill threshold — build session ended")
            self._log_event("SESSION_END", "Kill threshold", "TERMINATE")
            raise IBATerminatedError(f"Kill threshold triggered: {action}")

        # 3. Denied list
        if self._match_denied(action):
            self._log_event("BLOCK", action, "BLOCK", "Component in denied list")
            self.block_count += 1
            print(f"  ✗ BLOCKED  [{action[:62]}]\n    → Component in denied list")
            raise IBABlockedError(f"Denied: {action}")

        # 4. Scope check
        if self.scope and not self._match_scope(action):
            if self.default_posture == "DENY_ALL":
                self._log_event("BLOCK", action, "BLOCK", "Outside declared app scope — DENY_ALL")
                self.block_count += 1
                print(f"  ✗ BLOCKED  [{action[:62]}]\n    → Outside declared app scope (DENY_ALL)")
                raise IBABlockedError(f"Out of scope: {action}")

        # 5. ALLOW
        elapsed_ms = (time.perf_counter() - start) * 1000
        self._log_event("ALLOW", action, "ALLOW", f"Within app scope ({elapsed_ms:.3f}ms)")
        print(f"  ✓ ALLOWED  [{action[:62]}]  ({elapsed_ms:.3f}ms)")
        self.components_built.append(action)
        return True

    def hollow(self, prompt: str, level: str = "medium") -> str:
        """Redact high-risk component requests from the build prompt."""
        blocked = HOLLOW_LEVELS.get(level, HOLLOW_LEVELS["medium"])
        hollowed = prompt
        redacted = []
        for component in blocked:
            if component.lower() in prompt.lower():
                hollowed = hollowed.replace(component, f"[REDACTED:{component.upper()}]")
                redacted.append(component)
        if redacted:
            print(f"  ◎ HOLLOWED [{level}] — blocked: {', '.join(redacted)}")
            self._log_event("HOLLOW", f"Prompt hollowing: {level}", "ALLOW",
                           f"Blocked components: {', '.join(redacted)}")
        return hollowed

    def summary(self):
        print("\n" + "═" * 64)
        print("  IBA APP BUILDER GUARD · SESSION SUMMARY")
        print("═" * 64)
        print(f"  Session      : {self.session_id}")
        print(f"  Actions      : {self.action_count}")
        print(f"  Blocked      : {self.block_count}")
        print(f"  Allowed      : {self.action_count - self.block_count}")
        print(f"  Components   : {len(self.components_built)}")
        print(f"  Status       : {'TERMINATED' if self.terminated else 'COMPLETE'}")
        print(f"  Audit log    : {self.audit_path}")
        print("═" * 64 + "\n")

    def print_audit_log(self):
        print("\n── APP BUILD AUDIT CHAIN ────────────────────────────────────")
        if not os.path.exists(self.audit_path):
            print("  No audit log found.")
            return
        with open(self.audit_path) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    verdict = entry['verdict']
                    symbol = "✓" if verdict == "ALLOW" else "✗"
                    print(f"  {symbol} {entry['timestamp'][:19]}  {verdict:<10}  {entry['action'][:50]}")
                except Exception:
                    pass
        print("─────────────────────────────────────────────────────────────\n")


# ── CLI & Demonstration ───────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='IBA App Builder Guard')
    parser.add_argument('prompt', nargs='?', help='App build prompt')
    parser.add_argument('--hollow', choices=['light', 'medium', 'deep'],
                        default=None, help='Apply safe hollowing to prompt')
    parser.add_argument('--config', default='.iba.yaml', help='IBA config file')
    parser.add_argument('--demo', action='store_true', help='Run demonstration')
    args = parser.parse_args()

    guard = IBAAppBuilderGuard(config_path=args.config)

    if args.prompt:
        prompt = args.prompt
        if args.hollow:
            prompt = guard.hollow(prompt, args.hollow)
        print(f"\n  Prompt: {prompt}\n")

    if args.demo or not args.prompt:
        scenarios = [
            # ALLOW — within scope
            ("Generate todo list UI component", True),
            ("Build frontend dashboard with mock data", True),
            ("Create prototype landing page", True),

            # BLOCK — denied list
            ("Add user authentication system", False),
            ("Connect PostgreSQL database", False),
            ("Integrate Stripe payment processing", False),

            # TERMINATE — kill threshold
            ("Deploy application to production-deployment server", False),
        ]

        print("── Running App Builder Gate Checks ──────────────────────────\n")

        for action, _ in scenarios:
            try:
                guard.check_action(action)
            except IBATerminatedError as e:
                print(f"\n  BUILD SESSION TERMINATED: {e}")
                break
            except IBABlockedError:
                pass

    guard.summary()
    guard.print_audit_log()


if __name__ == "__main__":
    main()
