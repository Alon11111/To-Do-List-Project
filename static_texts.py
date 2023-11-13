# Static unchanging texts

DB_NAME = "to_do_list.sqlite"

LOGIN_USER_MESSAGE_BANK = ["Please provide a properly formatted email.",
                           "Error: This email is not registered.",
                           "Error: Password incorrect."]

REGISTER_USER_MESSAGE_BANK = ["Please provide a properly formatted email.",
                              "This email is already registered.",
                              "Please use only alphabet letters for first and last name.",
                              "Password must contain 6-12 characters.",
                              "Password must contain atleast 1 uppercase letter, 1 lowercase letter and 1 number."]

RESTORE_USER_MESSAGE_BANK = ["Please provide a properly formatted email.",
                             "Error: This email is not registered.",
                              "Error: The user info you provided is incorrect.",
                              "New password must contain 6-12 characters.",
                              "New password must contain atleast 1 uppercase letter, 1 lowercase letter and 1 number."]

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

PASSWORD_REGEX = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{6,12}$'

DATE_REGEX = r'^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'