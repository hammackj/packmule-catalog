#!/usr/bin/env python3
"""Checks catalog.json and the review reports. Run from the repository root."""
import json
import re
import sys
from pathlib import Path

errors = []


def err(where, msg):
    errors.append(f"{where}: {msg}")


DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SHA = re.compile(r"^[0-9a-f]{64}$")
REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
VERDICTS = {"pass", "fail", "unsure", "error"}

try:
    catalog = json.loads(Path("catalog.json").read_text())
except Exception as e:  # noqa: BLE001
    sys.exit(f"catalog.json: {e}")

if catalog.get("version") != 1:
    err("catalog.json", "version must be 1")
addons = catalog.get("addons")
if not isinstance(addons, list) or not addons:
    sys.exit("catalog.json: no addons list")

ids = [e.get("id") for e in addons]
reports = set()
for e in addons:
    w = e.get("id") or "(entry without id)"
    if not re.fullmatch(r"[a-z0-9-]+", str(e.get("id", ""))):
        err(w, "id must be lowercase letters, digits and dashes")
    if ids.count(e.get("id")) > 1:
        err(w, "duplicate id")
    for k in ("name", "category", "description"):
        if not isinstance(e.get(k), str) or not e[k].strip():
            err(w, f"{k} is missing")
    if not REPO.match(str(e.get("repo", ""))):
        err(w, "repo must be owner/name")
    # "" picks the repo's unprefixed tags; anything else is a stream like "spoken/".
    if e.get("tagPrefix") not in (None, "") and not str(e["tagPrefix"]).endswith("/"):
        err(w, "tagPrefix must be empty or end with /")
    for k in ("flavors", "folders"):
        if not isinstance(e.get(k), list) or not e[k] or not all(isinstance(x, str) and x for x in e[k]):
            err(w, f"{k} must be a non-empty list of names")
    for r in e.get("requires", []):
        if r not in ids:
            err(w, f"requires unknown id {r}")
    v = e.get("verified")
    if v is not None:
        if not DATE.match(str(v.get("date", ""))):
            err(w, "verified.date must be YYYY-MM-DD")
        if not isinstance(v.get("ciBuilds", False), bool):
            err(w, "verified.ciBuilds must be true or false")
    for i, r in enumerate(e.get("reviews", [])):
        rw = f"{w} review {r.get('tag', i)}"
        if not r.get("tag"):
            err(rw, "tag is missing")
        if not r.get("sha256") or not all(SHA.match(h) for h in r["sha256"]):
            err(rw, "sha256 must list lowercase hex SHA-256 digests")
        if not DATE.match(str(r.get("date", ""))):
            err(rw, "date must be YYYY-MM-DD")
        for who in ("claude", "codex"):
            if r.get(who) not in VERDICTS:
                err(rw, f"{who} must be one of {sorted(VERDICTS)}")
        report = str(r.get("report", ""))
        if not report.startswith(f"reviews/{e.get('id')}/") or not Path(report).is_file():
            err(rw, f"report {report!r} is missing (expected under reviews/{e.get('id')}/)")
        reports.add(report)
        s = r.get("signoff")
        if s is not None and (not s.get("by") or not s.get("note") or not DATE.match(str(s.get("date", "")))):
            err(rw, "signoff needs by, date (YYYY-MM-DD) and note")

for f in sorted(Path("reviews").rglob("*.md")):
    if f.as_posix() not in reports:
        err(f.as_posix(), "report not referenced by catalog.json")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"OK: {len(addons)} addons, {len(reports)} reports")
