from src.Miijin.MiijinDatabase import miijin_postgres, postgres_config

class MiijinLunchCLI:
    def __init__(self):
        # Our database configuration being pulled from postgres_config
        self.server = postgres_config.server
        self.database = postgres_config.database
        self.username = postgres_config.username
        self.password = postgres_config.password

        # Initiate the connection to our database
        self.miijin_db = miijin_postgres.MiijinDatabase(
            self.server, self.database, self.username, self.password
        )

    def run(self):
        print("Miijin Lunch (CLI)")
        print("Scan/enter a Student/Employee ID and press Enter.")
        print("Type 'scipio' to exit.\n")

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
                continue

            userid = int(raw)
            last_userid = userid

            print(f"Last User ID Scanned: {last_userid}")

            try:
                self.miijin_db.perform_insert(userid)
                print("Inserted.\n")
            except Exception as e:
                print(f"Insert failed: {e}\n")


def main():
    MiijinLunchCLI().run()


if __name__ == "__main__":
    main()
