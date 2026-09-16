#!/usr/bin/env python3
"""Fail if likely private or binary research files appear in a public release."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
BLOCKED_SUFFIXES = {".xlsx", ".xls", ".pdf", ".docx", ".png", ".jpg", ".jpeg", ".ndjson"}
BLOCKED_TOKENS = ("cookie", "session", "token", "password", "private", "working")
issues = []
for path in ROOT.rglob("*"):
    if not path.is_file() or ".git" in path.parts:
        continue
    relative = path.relative_to(ROOT)
    if relative.parts[:2] == ("data", "private"):
        continue
    name = path.name.lower()
    if path.suffix.lower() in BLOCKED_SUFFIXES:
        issues.append(f"Blocked binary or diagnostic file: {relative}")
    if any(token in name for token in BLOCKED_TOKENS):
        issues.append(f"Review potentially private filename: {relative}")
if issues:
    print("Public-release check failed:")
    print("\n".join(f"- {issue}" for issue in issues))
    sys.exit(1)
print("Public-release check passed.")
