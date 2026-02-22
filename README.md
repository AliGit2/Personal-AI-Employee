# Personal AI Employee
An autonomous agent architecture built using Claude Code and Obsidian to manage personal affairs and business operations as a Digital FTE

## Bronze Tier: Implemented

- Obsidian vault initialized: [AI_Employee_Vault](file:///f:/Github/Personal-AI-Employee/AI_Employee_Vault)
  - Includes Dashboard.md and Company_Handbook.md
  - Folders: /Inbox, /Needs_Action, /Done
- Watcher: Filesystem Drop Watcher
  - Scripts at repo root: watcher.py, processor.py, requirements.txt
- Full Automation: processor.py now automatically updates Dashboard.md counts and System_Log.md tables.
- Claude interaction: Use built-in filesystem tools to read/write the vault

## Run Watcher (Windows)

1. Ensure Python 3.10+ is installed
2. Install dependency:

   pip install -r requirements.txt

3. Start the watcher pointing to the vault Inbox:

   python watcher.py --vault ".\\AI_Employee_Vault" --drop ".\\AI_Employee_Vault\\Inbox"

Drop files into the configured Drop folder. Copies and metadata appear in AI_Employee_Vault\\Needs_Action.

## Validate

Run verification that also checks automatic Dashboard and System Log updates:

   python tests\\processor_auto_update_test.py

Expected: {"ok": true, ...}

## Next

- Expand watchers (Gmail, WhatsApp) for Silver tier
- Integrate MCP servers for actions
