import re
from data import query_read_rows, query_commit
from static_texts import REGISTER_USER_MESSAGE_BANK, LOGIN_USER_MESSAGE_BANK, RESTORE_USER_MESSAGE_BANK, EMAIL_REGEX, PASSWORD_REGEX


# Session functions

def session_user_id_verification(session_user_id = ""):
    sql = f"SELECT * FROM users WHERE user_id='{session_user_id}'"
    if len(query_read_rows(sql)["rows"])==0:
        return False
    return True


# Login functions

def get_user_id(email=""):
    return (query_read_rows(f"SELECT user_id FROM users WHERE email='{email}'")["rows"])

def login_verification(email="", password=""):
    email = email.lower()

    if not re.fullmatch(EMAIL_REGEX, email):
        message = LOGIN_USER_MESSAGE_BANK[0]
        return [False, message]

    not_registered_test = get_user_id(email)
    if len(not_registered_test)==0:
        message = LOGIN_USER_MESSAGE_BANK[1]
        return [False, message]
    
    sql = f"SELECT * FROM users WHERE email='{email}' AND password='{password}'"
    wrong_password_test = query_read_rows(sql)["rows"]
    if len(wrong_password_test)==0:
        message = LOGIN_USER_MESSAGE_BANK[2]
        return [False, message]
    
    message = ""
    return [True, message]


# Register functions

def create_user(email="", password="", first_name="", last_name=""):
    sql = f"""INSERT INTO users (email, password, first_name, last_name) VALUES
    ('{email}', '{password}', '{first_name}', '{last_name}')"""
    query_commit(sql)

def register_verification(email="", password="", first_name="", last_name=""):
    email = email.lower()
    first_name = first_name.lower().capitalize()
    last_name = last_name.lower().capitalize()

    if not re.fullmatch(EMAIL_REGEX, email):
        message = REGISTER_USER_MESSAGE_BANK[0]
        return [False, message]

    used_email_test = get_user_id(email)
    if len(used_email_test)>0:
        message = REGISTER_USER_MESSAGE_BANK[1]
        return [False, message]
    
    if (not first_name.isalpha()) or (not last_name.isalpha()):
        message = REGISTER_USER_MESSAGE_BANK[2]
        return [False, message]
    
    if (len(password) < 6) or (len(password) > 12):
        message = REGISTER_USER_MESSAGE_BANK[3]
        return [False, message]
    
    if not re.fullmatch(PASSWORD_REGEX, password):
        message = REGISTER_USER_MESSAGE_BANK[4]
        return [False, message]

    create_user(email=email, password=password,
                    first_name=first_name, last_name=last_name)
    message = ""
    return [True, message]


# restore functions

def reset_user(email="", password=""):
    sql = f"""
    UPDATE users 
    SET password="{password}" 
    WHERE email="{email}"
    """
    query_commit(sql)

def restore_verification(email="", password="", first_name="", last_name=""):
    email = email.lower()
    first_name = first_name.lower().capitalize()
    last_name = last_name.lower().capitalize()

    if not re.fullmatch(EMAIL_REGEX, email):
        message = RESTORE_USER_MESSAGE_BANK[0]
        return [False, message]

    not_registered_test = get_user_id(email)
    if len(not_registered_test)==0:
        message = RESTORE_USER_MESSAGE_BANK[1]
        return [False, message]
    
    sql = f"SELECT * FROM users WHERE email='{email}' AND first_name='{first_name}' AND last_name='{last_name}'"
    wrong_user_info_test = query_read_rows(sql)["rows"]
    if len(wrong_user_info_test)==0:
        message = RESTORE_USER_MESSAGE_BANK[2]
        return [False, message]

    if (len(password) < 6) or (len(password) > 12):
        message = RESTORE_USER_MESSAGE_BANK[3]
        return [False, message]
    
    if not re.fullmatch(PASSWORD_REGEX, password):
        message = RESTORE_USER_MESSAGE_BANK[4]
        return [False, message]

    reset_user(email=email, password=password)
    message = ""
    return [True, message]


# Home functions

def get_first_name(user_id=""):
    return (query_read_rows(f"SELECT first_name FROM users WHERE user_id='{user_id}'")["rows"])