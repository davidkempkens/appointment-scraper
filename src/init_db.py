import src.database as db


def main():
    print("Resetting the database")
    db.reset_db()
    print("Initializing the database")
    db.init_db()


if __name__ == "__main__":
    main()
