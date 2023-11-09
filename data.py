import sqlite3
import os
from static_texts import DB_NAME

def setup(filename=DB_NAME):
    if not os.path.exists(DB_NAME):
        with sqlite3.connect(filename) as conn:
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, email TEXT NOT NULL UNIQUE, password TEXT, first_name TEXT, last_name TEXT);"
            )
            cur.execute(
                "CREATE TABLE IF NOT EXISTS tasks(task_id INTEGER PRIMARY KEY, user_id INTEGER, status TEXT DEFAULT 'In-Progress', description TEXT, date TEXT, FOREIGN KEY (user_id) REFERENCES users(user_id));"
            )
            conn.commit()

def query_commit(sql, filename=DB_NAME):
    with sqlite3.connect(filename) as conn:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        return "commited"


def query_read_rows(sql, filename=DB_NAME):
    with sqlite3.connect(filename) as conn:
        cur=conn.cursor()
        cur.execute(sql)
        return {"rows": cur.fetchall()}


def query_read_row_names(sql, filename=DB_NAME):
    with sqlite3.connect(filename) as conn:
        cur=conn.cursor()
        cur.execute(sql)
        row_names = []
        try:
            for row in cur.description:
                row_names.append(row[0])
        except:
            print("no description of row names")
        return {"keys": row_names}


def get_task_dicts(user_id=""):
    sql = f"SELECT * FROM tasks WHERE user_id='{user_id}'"
    keys = query_read_row_names(sql)["keys"]
    tasks = query_read_rows(sql)["rows"]
    dicts_list = []
    for task in tasks:
        values = list(task)
        dict_row = dict(zip(keys, values))
        dicts_list.append(dict_row)
    return dicts_list