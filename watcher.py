import argparse
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from processor import process_file, ensure_vault_structure


class DropHandler(FileSystemEventHandler):
    def __init__(self, vault_path: str):
        self.vault_path = vault_path
        ensure_vault_structure(self.vault_path)

    def on_created(self, event):
        if event.is_directory:
            return
        process_file(str(event.src_path), self.vault_path)


def run(drop_path: str, vault_path: str):
    handler = DropHandler(vault_path)
    observer = Observer()
    Path(drop_path).mkdir(parents=True, exist_ok=True)
    observer.schedule(handler, drop_path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", required=True)
    parser.add_argument("--drop", required=True)
    args = parser.parse_args()
    run(args.drop, args.vault)


if __name__ == "__main__":
    main()
