from pathlib import Path
import tempfile
from datetime import datetime
import json
import sys

# Import processor from repo root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from processor import process_file  # type: ignore


DASHBOARD_BASE = """---
title: Status Center
owner: Local Agent
last_updated: 2026-02-19
---

# Status Center

## Task Statistics

| Area               | Count |
|--------------------|------:|
| Needs_Action       |     0 |
| Completed Plans    |     0 |
| Pending_Approvals  |     0 |
| Done               |     0 |
"""

SYSTEM_LOG_BASE = """# System Log

## Activity Log

| Timestamp | Action | Details |
|-----------|--------|---------|
| 2026-02-19 | System Initialized | Vault structure created with Inbox, Needs_Action, Done, Logs, and Plans folders |
"""


def main():
    with tempfile.TemporaryDirectory() as tmp:
        vault = Path(tmp) / "AI_Employee_Vault"
        (vault / "Inbox").mkdir(parents=True, exist_ok=True)
        (vault / "Needs_Action").mkdir(parents=True, exist_ok=True)
        (vault / "Done").mkdir(parents=True, exist_ok=True)
        (vault / "Dashboard.md").write_text(DASHBOARD_BASE, encoding="utf-8")
        (vault / "System_Log.md").write_text(SYSTEM_LOG_BASE, encoding="utf-8")

        # Create a source file
        source = Path(tmp) / "sample.txt"
        source.write_text("hello world", encoding="utf-8")

        # Process the file
        result = process_file(str(source), str(vault))

        # Validate Dashboard increment
        dashboard = (vault / "Dashboard.md").read_text(encoding="utf-8")
        needs_action_row = [ln for ln in dashboard.splitlines() if ln.strip().startswith("| Needs_Action")][0]
        count_str = needs_action_row.split("|")[2].strip()
        try:
            count = int(count_str)
        except Exception:
            count = None

        # Validate System Log appended
        slog = (vault / "System_Log.md").read_text(encoding="utf-8")
        appended = any("File Detected" in ln and "sample.txt" in ln for ln in slog.splitlines())

        print(json.dumps({
            "copied_exists": Path(result["copied_path"]).exists(),
            "metadata_exists": Path(result["metadata_path"]).exists(),
            "needs_action_count": count,
            "log_appended": appended
        }))


if __name__ == "__main__":
    main()
