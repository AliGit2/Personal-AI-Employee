from pathlib import Path
import tempfile
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from processor import process_file, ensure_vault_structure


def main():
    with tempfile.TemporaryDirectory() as tmp:
        vault = Path(tmp) / "vault"
        ensure_vault_structure(str(vault))
        source = Path(tmp) / "sample.txt"
        source.write_text("hello", encoding="utf-8")
        result = process_file(str(source), str(vault))
        copied = Path(result["copied_path"])
        meta = Path(result["metadata_path"])
        ok = copied.exists() and meta.exists()
        print(json.dumps({"ok": ok, "copied_exists": copied.exists(), "meta_exists": meta.exists()}))


if __name__ == "__main__":
    main()
