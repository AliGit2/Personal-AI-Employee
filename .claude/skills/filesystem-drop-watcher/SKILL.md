---
name: filesystem-drop-watcher
description: Monitors a Drop folder and files into Obsidian Needs_Action. Invoke for local file intake workflows.
---

# Filesystem Drop Watcher

Monitors a directory for new files and moves them into your Obsidian vault's Needs_Action with a metadata markdown.

## When To Use

- Ingest local files into the AI_Employee_Vault
- Trigger Claude processing via Needs_Action entries
- Run continuously on Windows via PowerShell

## Setup

1. Ensure Python 3.10+ is available on PATH
2. Optional: install watchdog
3. Set your Drop folder path and vault path

## Start (Windows)

Run scripts/start-watcher.ps1

## Manual Run

python scripts\watcher.py --vault "..\..\..\AI_Employee_Vault" --drop "C:\Drop"

## Verification

Run scripts\tests\smoke_test_processor.py

## Output Convention

- File copy: Needs_Action\FILE_<original_name>
- Metadata: Needs_Action\FILE_<original_name>.md with YAML front matter and status: pending

