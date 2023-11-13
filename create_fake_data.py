import random
import datetime
from data import query_commit

def create_fake_users():
    sql = f"""
    INSERT INTO users (email, password, first_name, last_name) VALUES
    ('user1@example.com', 'Password1', 'John', 'Doe'),
    ('user2@example.com', 'Password2', 'Alice', 'Smith'),
    ('user3@example.com', 'Password3', 'Bob', 'Johnson'),
    ('user4@example.com', 'Password4', 'Emily', 'Brown'),
    ('user5@example.com', 'Password5', 'Michael', 'Davis')
    """
    query_commit(sql)

def create_fake_tasks(num=30):
    for i in range(num):
        user_id = random.randint(1, 5)  # number of users for tests (ids 1-5)
        descriptions = [
            "Walk the dog",
            "Buy groceries",
            "Do homework",
            "Workout",
            "Drive somewhere",
        ]
        description = random.choices(descriptions)[0]
        date = datetime.date(
            day=random.randint(1, 28),
            month=random.randint(1, 12),
            year=random.randint(2023, 2025),
        )
        sql = f"""
        INSERT INTO tasks (user_id, description, date) VALUES
        ("{user_id}", "{description}", "{date}")
        """
        query_commit(sql)

# create_fake_users()

# create_fake_tasks()