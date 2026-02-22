from pathlib import Path
from datetime import datetime
import shutil
import os
import re


def ensure_vault_structure(vault_path: str) -> None:
    vp = Path(vault_path)
    (vp / "Inbox").mkdir(parents=True, exist_ok=True)
    (vp / "Needs_Action").mkdir(parents=True, exist_ok=True)
    (vp / "Done").mkdir(parents=True, exist_ok=True)


def _update_dashboard_needs_action(vault_path: str) -> None:
    dashboard = Path(vault_path) / "Dashboard.md"
    if not dashboard.exists():
        return
    text = dashboard.read_text(encoding="utf-8")
    lines = text.splitlines()
    # Find the table header for Task Statistics
    try:
        header_idx = next(
            i for i, ln in enumerate(lines)
            if ln.strip().startswith("| Area") and "Count" in ln
        )
    except StopIteration:
        return
    # Find end of table block (first non '|' line after header and alignment)
    i = header_idx + 1
    # Skip alignment line
    if i < len(lines) and lines[i].strip().startswith("|"):
        i += 1
    end = i
    while end < len(lines) and lines[end].strip().startswith("|"):
        end += 1
    # Iterate rows to find Needs_Action row
    for row_idx in range(i, end):
        row = lines[row_idx]
        if not row.strip().startswith("|"):
            continue
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if not cells:
            continue
        if cells[0] == "Needs_Action" and len(cells) >= 2:
            # Increment count
            try:
                count = int(re.sub(r"[^\d]", "", cells[1])) if cells[1] else 0
            except ValueError:
                count = 0
            new_count = count + 1
            # Rebuild row preserving left cell label, simple spacing for count
            lines[row_idx] = f"| Needs_Action       | {new_count:5d} |"
            dashboard.write_text("\n".join(lines), encoding="utf-8")
            return
    # If not found, append a new Needs_Action row at end of table
    insert_idx = end
    lines.insert(insert_idx, "| Needs_Action       |     1 |")
    dashboard.write_text("\n".join(lines), encoding="utf-8")


def _append_system_log(vault_path: str, filename: str) -> None:
    log_path = Path(vault_path) / "System_Log.md"
    ts = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    row = f"| {ts} | File Detected | {filename} |"
    if not log_path.exists():
        # Create a new log with the established headers
        content = [
            "# System Log",
            "",
            "## Activity Log",
            "",
            "| Timestamp | Action | Details |",
            "|-----------|--------|---------|",
            row,
            "",
        ]
        log_path.write_text("\n".join(content), encoding="utf-8")
        return
    text = log_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    # Locate the established header and alignment lines
    try:
        hdr_idx = next(
            i for i, ln in enumerate(lines)
            if ln.strip() == "| Timestamp | Action | Details |"
        )
        align_ok = hdr_idx + 1 < len(lines) and lines[hdr_idx + 1].strip() == "|-----------|--------|---------|"
        if not align_ok:
            raise StopIteration
    except StopIteration:
        # Fallback: append a new table at the end to maintain consistency
        lines.extend([
            "",
            "## Activity Log",
            "",
            "| Timestamp | Action | Details |",
            "|-----------|--------|---------|",
            row,
            "",
        ])
        log_path.write_text("\n".join(lines), encoding="utf-8")
        return
    # Find the end of the table block (contiguous '|' lines after alignment)
    end = hdr_idx + 2
    while end < len(lines) and lines[end].strip().startswith("|"):
        end += 1
    # Insert the new row at the end of the table block
    lines.insert(end, row)
    log_path.write_text("\n".join(lines), encoding="utf-8")


def process_file(source_path: str, vault_path: str) -> dict:
    ensure_vault_structure(vault_path)
    src = Path(source_path)
    needs_action = Path(vault_path) / "Needs_Action"
    dest = needs_action / f"FILE_{src.name}"
    shutil.copy2(src, dest)
    meta_path = dest.with_suffix(".md")
    size = src.stat().st_size if src.exists() else 0
    created = datetime.utcnow().isoformat() + "Z"
    front_matter = [
        "---",
        "type: file_drop",
        f"original_name: {src.name}",
        f"size: {size}",
        f"created: {created}",
        "status: pending",
        "---",
        "",
        "New file dropped for processing.",
        "",
    ]
    meta_path.write_text("\n".join(front_matter), encoding="utf-8")
    # Auto-updates for Bronze Tier
    _update_dashboard_needs_action(vault_path)
    _append_system_log(vault_path, src.name)
    return {
        "copied_path": str(dest),
        "metadata_path": str(meta_path),
        "size": size,
        "created": created,
    }


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", required=True)
    parser.add_argument("--file", required=True)
    args = parser.parse_args()
    result = process_file(args.file, args.vault)
    print(result)


if __name__ == "__main__":
    main()
