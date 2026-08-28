"""Turn DJ Mik-E owner update emails into reviewable GitHub issues.

This script is intentionally conservative: it creates GitHub issues only.
It does not edit website files, commit changes, push to GitHub, or deploy.

Prerequisites:
- Hermes Google Workspace OAuth authorized for Gmail read/modify.
- GitHub CLI authenticated with access to jimmyaibot10-glitch/dj-mike-booking-site.
- Optional Gmail labels created:
  DJMIKE_SITE_UPDATES, DJMIKE_PROCESSED, DJMIKE_NEEDS_REVIEW
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = "jimmyaibot10-glitch/dj-mike-booking-site"
DEFAULT_QUERY = '({subject:"SITE UPDATE:" OR subject:"MEDIA UPDATE:" OR subject:"URGENT SITE UPDATE:"} OR label:DJMIKE_SITE_UPDATES) -label:DJMIKE_PROCESSED'
DEFAULT_MAX_MESSAGES = 10

HERMES_HOME = Path(os.environ.get("HERMES_HOME", r"C:\Users\chris\AppData\Local\hermes"))
GOOGLE_API = HERMES_HOME / "skills" / "productivity" / "google-workspace" / "scripts" / "google_api.py"
PYTHON = Path(r"C:\Users\chris\AppData\Roaming\uv\python\cpython-3.11.15-windows-x86_64-none\python.exe")


def run_command(command: list[str], *, check: bool = True) -> str:
    """Run a command and return stdout with clear errors."""
    result = subprocess.run(command, text=True, capture_output=True)
    if check and result.returncode != 0:
        raise RuntimeError(
            f"Command failed ({result.returncode}): {' '.join(command)}\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result.stdout.strip()


def google_api(*args: str) -> object:
    """Call the Hermes Google API helper and parse JSON output."""
    if not GOOGLE_API.exists():
        raise FileNotFoundError(f"Google API helper not found: {GOOGLE_API}")

    python_exe = str(PYTHON if PYTHON.exists() else Path(sys.executable))
    output = run_command([python_exe, str(GOOGLE_API), *args])
    if not output:
        return None
    return json.loads(output)


def get_label_id(labels: list[dict], label_name: str) -> str | None:
    """Return a Gmail label id by display name."""
    for label in labels:
        if label.get("name") == label_name or label.get("id") == label_name:
            return label.get("id")
    return None


def build_issue_body(message: dict) -> str:
    """Create a GitHub issue body from a Gmail message."""
    body = message.get("body") or message.get("snippet") or ""
    return f"""Owner website update request received by email.

## Source

- From: {message.get('from', 'Unknown')}
- To: {message.get('to', 'Unknown')}
- Date: {message.get('date', 'Unknown')}
- Gmail message id: `{message.get('id', 'Unknown')}`
- Gmail thread id: `{message.get('threadId', 'Unknown')}`

## Email subject

{message.get('subject', '(no subject)')}

## Requested change / email body

```text
{body.strip()[:6000]}
```

## Review checklist

- [ ] Verify request came from DJ Mik-E or an approved contact.
- [ ] Clarify any missing wording, dates, pricing, or media details.
- [ ] Confirm no private information should be published.
- [ ] Curate and optimize any attached media before committing.
- [ ] Implement approved website changes.
- [ ] Verify local files and live Vercel deployment.
"""


def ensure_github_labels() -> None:
    """Create workflow labels if they do not already exist."""
    label_specs = {
        "owner-request": ("Website owner requested change", "6f42c1"),
        "needs-review": ("Needs Chris review before implementation", "fbca04"),
    }
    existing_output = run_command(["gh", "label", "list", "--repo", REPO, "--limit", "100"])
    existing_names = {line.split("\t", 1)[0] for line in existing_output.splitlines() if line.strip()}

    for label_name, (description, color) in label_specs.items():
        if label_name in existing_names:
            continue
        run_command(
            [
                "gh",
                "label",
                "create",
                label_name,
                "--repo",
                REPO,
                "--description",
                description,
                "--color",
                color,
            ]
        )


def create_github_issue(message: dict, *, dry_run: bool) -> str:
    """Create a GitHub issue for one message and return the issue URL."""
    subject = message.get("subject") or "Owner website update"
    title = f"Owner update: {subject}"[:250]
    body = build_issue_body(message)

    if dry_run:
        print(f"DRY RUN: would create issue: {title}")
        return "dry-run"

    ensure_github_labels()
    return run_command(
        [
            "gh",
            "issue",
            "create",
            "--repo",
            REPO,
            "--title",
            title,
            "--body",
            body,
            "--label",
            "owner-request,needs-review",
        ]
    )


def process_messages(query: str, max_messages: int, dry_run: bool) -> int:
    """Search Gmail and create one GitHub issue per matching message."""
    labels = google_api("gmail", "labels")
    processed_label = get_label_id(labels or [], "DJMIKE_PROCESSED")
    needs_review_label = get_label_id(labels or [], "DJMIKE_NEEDS_REVIEW")

    messages = google_api("gmail", "search", query, "--max", str(max_messages)) or []
    if not messages:
        print("No matching owner update emails found.")
        return 0

    created = 0
    for summary in messages:
        message_id = summary["id"]
        message = google_api("gmail", "get", message_id)
        issue_url = create_github_issue(message, dry_run=dry_run)
        print(f"Created issue for Gmail message {message_id}: {issue_url}")
        created += 1

        if dry_run:
            continue

        labels_to_add = [label for label in [processed_label, needs_review_label] if label]
        if labels_to_add:
            google_api("gmail", "modify", message_id, "--add-labels", ",".join(labels_to_add), "--remove-labels", "UNREAD")
        else:
            google_api("gmail", "modify", message_id, "--remove-labels", "UNREAD")
            print("Warning: DJMIKE_PROCESSED / DJMIKE_NEEDS_REVIEW labels were not found.")

    return created


def main() -> int:
    parser = argparse.ArgumentParser(description="Create GitHub issues from DJ Mik-E owner update emails.")
    parser.add_argument("--query", default=DEFAULT_QUERY, help="Gmail search query")
    parser.add_argument("--max", type=int, default=DEFAULT_MAX_MESSAGES, help="Maximum messages to process")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without creating issues or modifying Gmail")
    args = parser.parse_args()

    count = process_messages(args.query, args.max, args.dry_run)
    print(f"Processed {count} message(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
