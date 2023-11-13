import re
from data import get_task_dicts , query_commit, query_read_rows
from datetime import datetime
from static_texts import DATE_REGEX


# Read functions

def read_tasks(user_id="", task=[]):
    if user_id == "":
        return False
    sql = f"SELECT * FROM users WHERE user_id='{user_id}'"
    if len(query_read_rows(sql)["rows"])==0:
        return False
    
    today = datetime.now().date()
    update_expired_status(user_id, today)
    
    if len(task) < 1:
        task = get_task_dicts(user_id)
    
    sorted_tasks = sorted(task, key=lambda i: (
        i["status"] != "In-Progress",
        i["status"] != "Finished",
        i["status"] != "Expired",
        i["date"]
))
    return sorted_tasks

def update_expired_status(user_id, today):
    sql = f"""
    UPDATE tasks 
    SET status="Expired"
    WHERE date < "{today}" AND status != 'Finished' AND user_id="{user_id}";
    """
    query_commit(sql)


# Add functions

def add_task(user_id, data):
    if user_id == "":
        return False
    sql = f"SELECT * FROM users WHERE user_id='{user_id}'"
    if len(query_read_rows(sql)["rows"])==0:
        return False

    if (len(data["description"]) <= 2) or (len(data["description"]) >= 76):
        return False
    
    if not re.fullmatch(DATE_REGEX, data["date"]):
        return False

    sql = f"""
    INSERT INTO tasks (user_id, description, date) VALUES
    ("{user_id}", "{data["description"]}", "{data["date"]}")
    """
    query_commit(sql)

    today = datetime.now().date()
    update_expired_status(user_id, today)


# Delete functions

def delete_task(data):
    if data["task_id"] == "":
        return False
    sql = f"SELECT * FROM tasks WHERE task_id='{data['task_id']}'"
    if len(query_read_rows(sql)["rows"])==0:
        return False

    sql = f"""
    DELETE FROM tasks 
    WHERE task_id="{data["task_id"]}"
    """
    query_commit(sql)


# Update functions

def date_to_today(data):
    status = query_read_rows(f"SELECT status FROM tasks WHERE task_id='{data['task_id']}'")["rows"]
    if status[0][0] == "Expired":
        today = datetime.now().date()
        data["date"] = today

def update_status(data):
    if data["task_id"] == "":
        return False
    sql = f"SELECT * FROM tasks WHERE task_id='{data['task_id']}'"
    if len(query_read_rows(sql)["rows"])==0:
        return False

    date_to_today(data)
    sql = f"""
    UPDATE tasks 
    SET status="{data["status"]}", date="{data["date"]}"
    WHERE task_id="{data["task_id"]}"
    """
    query_commit(sql)


def update_task(data):
    if data["task_id"] == "":
        return False
    sql = f"SELECT * FROM tasks WHERE task_id='{data['task_id']}'"
    if len(query_read_rows(sql)["rows"])==0:
        return False

    if (len(data["description"]) <= 2) or (len(data["description"]) >= 76):
        return False

    if not re.fullmatch(DATE_REGEX, data["date"]):
        return False

    sql = f"""
    UPDATE tasks 
    SET description="{data["description"]}", date="{data["date"]}" 
    WHERE task_id="{data["task_id"]}"
    """
    query_commit(sql)
