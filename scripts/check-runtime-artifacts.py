"""Reject tracked local database files; never inspect row contents."""
import subprocess
from pathlib import PurePosixPath

names = subprocess.check_output(["git", "ls-files", "-z"]).decode().split("\0")
extensions = (".db", ".sqlite", ".sqlite3")
bad = [name for name in names if any(PurePosixPath(name).name.endswith(ext + sidecar) for ext in extensions for sidecar in ("", "-journal", "-wal", "-shm"))]
if bad:
    raise SystemExit("Tracked runtime databases: " + ", ".join(bad))
print("PASS: no tracked runtime databases or SQLite sidecars")
