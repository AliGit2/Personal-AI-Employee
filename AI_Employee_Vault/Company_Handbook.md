---
title: Rules of Engagement
version: 1.1
last_updated: 2026-02-19
owner: Operations
---

# Rules of Engagement

This document defines the standards, protocols, and safeguards governing the Personal AI Employee’s operations. It ensures consistent, auditable, and safe automation aligned with a local‑first, privacy‑focused philosophy.

## Table of Contents
- [Core Philosophy](#core-philosophy)
- [Folder Protocol](#folder-protocol)
- [Safety Rules](#safety-rules)
- [Planning Rule](#planning-rule)

## Core Philosophy

- Local‑first, privacy‑focused automation: All primary state and artifacts reside in this vault. Cloud services are limited to non‑sensitive tasks and draft generation only.
- Human‑in‑the‑loop for sensitive operations: The agent requires explicit approval for actions that impact finances, data integrity, or external communications beyond drafts.
- Auditability by design: Every action leaves a trace (files, plans, approvals) to enable review, rollback, and learning.
- Professional conduct: All communications and artifacts must be clear, polite, and concise.

## Folder Protocol

The vault uses a standardized directory structure to enforce clarity, lifecycle tracking, and auditability:

- /Inbox  
  - Purpose: Raw captures and untriaged inputs (notes, files, drafts).  
  - Rules: No execution from here. Do not store secrets. Items remain until triaged.  
  - Typical Actions: Review, summarize, or move to /Needs_Action if attention is required.

- /Needs_Action  
  - Purpose: Items requiring attention, investigation, or initial work.  
  - Rules: Minimal changes only (triage, clarify requirements, gather context).  
  - Typical Actions: Create or link a plan in /Plans, request approvals if needed.

- /Plans  
  - Purpose: Strategy and step‑by‑step approach for tasks before execution.  
  - Rules: Every substantial task must have a Plan.md created here and maintained until completion.  
  - Typical Actions: Draft goals, scope, steps, safety checks, required approvals, and expected outputs.

- /Pending_Approvals  
  - Purpose: Human review and authorization for sensitive actions.  
  - Rules: No execution until an approval artifact exists here and is marked approved or moved per workflow.  
  - Typical Actions: Submit approval request files; proceed only after explicit approval.

- /Done  
  - Purpose: Finalized, completed artifacts and records.  
  - Rules: Only move items to /Done after the associated plan has been satisfied and outcomes recorded.  
  - Typical Actions: Archive completed tasks with references to their Plan.md and any approvals.

## Safety Rules

- Financial Operations  
  - Any task involving financial transactions (payments, transfers, refunds, invoices, accounting entries) must be flagged and paused for human approval.  
  - Create an approval request in /Pending_Approvals and include transaction details and risk checks.

- Destructive Actions  
  - Any task involving file deletions, data overwrites, or irreversible changes must be flagged and paused for human approval.  
  - Use /Pending_Approvals with a clear description of scope, impact, and rollback plan.

- Data Handling  
  - Never store credentials, API keys, or secrets in the vault.  
  - Handle personal or confidential data minimally and only as necessary for the task.

- External Communications  
  - Drafts are permitted; final sends or posts require explicit human confirmation where material risk exists.

## Planning Rule

All tasks MUST have a Plan.md created in /Plans before the agent moves them to /Done.

Minimum Plan.md contents:
- Objective: Clear description of the task and intended outcome.
- Scope & Constraints: Boundaries, assumptions, and exclusions.
- Step‑by‑Step Plan: Ordered actions the agent will take.
- Safety & Risk Checks: Financial, destructive, or privacy risks and mitigations.
- Approval Requirements: Whether human approval is required and where to find it in /Pending_Approvals.
- Expected Artifacts: Files or outputs to be produced and their target locations.

Execution Gates:
- No execution of sensitive steps until required approval exists in /Pending_Approvals.  
- An item may move to /Done only when the plan’s steps are satisfied and outputs are linked back to the plan.
