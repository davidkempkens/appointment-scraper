import src.database as db


def main():
    db.reset_db()
    db.init_db()


if __name__ == "__main__":
    main()
