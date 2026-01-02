import os
from datetime import datetime
from pathlib import Path
from src.Miijin.MiijinDatabase import miijin_postgres, postgres_config

def get_log_dir() -> Path:
    base = os.environ.get("XDG_STATE_HOME")
    if base:
        return Path(base) / "miijin"
    return Path.home() / ".local" / "state" / "miijin"

LOG_DIR = get_log_dir()
LOG_DIR.mkdir(parents=True, exist_ok=True)

def invalid_scan_log_path() -> Path:
    today = datetime.now().strftime("%Y-%m-%d")
    return LOG_DIR / f"invalid_scans_{today}.log"

def db_error_log_path() -> Path:
    today = datetime.now().strftime("%Y-%m-%d")
    return LOG_DIR / f"db_errors_{today}.log"

class MiijinLunchCLI:
    def __init__(self):
        self.server = postgres_config.server
        self.database = postgres_config.database
        self.username = postgres_config.username
        self.password = postgres_config.password

        self.miijin_db = miijin_postgres.MiijinDatabase(
            self.server, self.database, self.username, self.password
        )

    def run(self):
        print("Scan/enter a Student/Employee ID and press Enter.")
        last_userid = None

        while True:
            try:
                raw = input("Student/Employee ID: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting.")
                break

            if raw.lower() in ("quit", "scipio"):
                print("Program closing.")
                break

            if not raw:
                continue

            if not raw.isdigit():
                print("Invalid input: please enter a numeric ID.")
                with open(invalid_scan_log_path(), "a") as f:
                    f.write(f"{datetime.now().isoformat()} | {raw}\n")
                continue

            userid = int(raw)
            last_userid = userid
            print(f"Last User ID Scanned: {last_userid}")

            try:
                self.miijin_db.perform_insert(userid)
            except Exception as e:
                print(f"Insert failed: {e}\n")
                with open(db_error_log_path(), "a") as f:
                    f.write(f"{datetime.now().isoformat()} | userid={userid} | error={e}\n")

def main():
    MiijinLunchCLI().run()

if __name__ == "__main__":
    main()
