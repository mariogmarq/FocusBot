import sqlite3

MIGRATION = 'CREATE TABLE IF NOT EXISTS users (' \
            'id INTEGER PRIMARY KEY,' \
            'time REAL NOT NULL,' \
            'max_strike REAL NOT NULL)'


def open_db(file_name: str) -> sqlite3.Connection:
    db = sqlite3.connect(file_name)
    c = db.cursor()
    c.execute(MIGRATION)
    db.commit()

    return db


class FocusDB:
    def __init__(self, file_name: str):
        self.db = open_db(file_name)
        self.cursor = self.db.cursor()

    def insert_user(self, user_id: int) -> None:
        statement = "INSERT INTO users (id, time, max_strike) VALUES ({}, 0.0, 0.0)".format(user_id)
        self.cursor.execute(statement)
        self.db.commit()

    def get_time(self, user_id: int) -> float:
        statement = "SELECT time FROM users WHERE id={}".format(user_id)
        self.cursor.execute(statement)
        row = self.cursor.fetchone()

        if row is None:
            self.insert_user(user_id=user_id)
            return 0

        return row[0]

    def get_max_strike(self, user_id: int) -> float:
        statement = "SELECT max_strike FROM users WHERE id={}".format(user_id)
        self.cursor.execute(statement)
        row = self.cursor.fetchone()

        if row is None:
            self.insert_user(user_id=user_id)
            return 0.0

        return row[0]

    def update_time(self, user_id: int, time_added: float) -> None:
        new_time = time_added + self.get_time(user_id=user_id)
        statement = "UPDATE users SET time={} WHERE id={}".format(new_time, user_id)
        self.cursor.execute(statement)
        statement = "UPDATE users SET max_strike={} WHERE id={}".format(time_added, user_id)
        if self.get_max_strike(user_id)*3600 < time_added:
            self.cursor.execute(statement)
        self.db.commit()

    def leaders(self) -> list:
        query = "SELECT * FROM users ORDER BY time ASC"
        self.cursor.execute(query)

        rv = []

        for i in range(3):
            row = self.cursor.fetchall()
            if row is None:
                break
            rv.append(row)

        return rv
