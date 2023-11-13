import unittest
from users_functions import register_verification, query_commit, get_user_id, login_verification, restore_verification
from tasks_functions import read_tasks, add_task, delete_task, update_task, update_status
from data import query_read_rows


##################################### REGISTER TESTS ######################################

class TestLoginVerification(unittest.TestCase):
    def test_invalid_email_register_verification(self):
        # Check if register fails due to invalid email format
        # Check if the correct error message is returned
        invalid_emails = ['test@exa', 'test@example.', 'testexample.com', 'test@@example.com', '@example.com']
        for email in invalid_emails:
            result = register_verification(email, 'Password1', 'Alon', 'Test')
            self.assertFalse(result[0])
            self.assertEqual(result[1], "Please provide a properly formatted email.")


    def test_registered_email_verification(self):
        # Check if register fails due to already registered email
        # Check if the correct error message is returned
        registered_emails = ['user1@example.com', 'user2@example.com', 'user3@example.com']
        for email in registered_emails:
            result = register_verification(email, 'Password1', 'Alon', 'Test')
            self.assertFalse(result[0])
            self.assertEqual(result[1], "This email is already registered.")

    
    def test_invalid_name_register_verification(self):
        # Check if register fails due to invalid first name or last name
        # Check if the correct error message is returned
        invalid_names = ['2432', 'ad324', '', '$#@$#@']
        for name in invalid_names:
            result = register_verification('test1@example.com', 'Password1', name, 'Test')
            self.assertFalse(result[0])
            self.assertEqual(result[1], "Please use only alphabet letters for first and last name.")

            result = register_verification('test1@example.com', 'Password1', 'Alon', name)
            self.assertFalse(result[0])
            self.assertEqual(result[1], "Please use only alphabet letters for first and last name.")
        

    def test_invalid_password_register_verification(self):
        # Check if register fails due to invalid password
        # Check if the correct error message is returned
        invalid_length_passwords = ['passw', '342', 'fdfkndfngfdfd']
        for password in invalid_length_passwords:
            result = register_verification('test1@example.com', password, 'Alon', 'Test')
            self.assertFalse(result[0])
            self.assertEqual(result[1], "Password must contain 6-12 characters.")
        
        invalid_minimum_char_req_passwords = ["password1", "Password", "PASSWORD1"]
        for password in invalid_minimum_char_req_passwords:
            result = register_verification('test1@example.com', password, 'Alon', 'Test')
            self.assertFalse(result[0])
            self.assertEqual(result[1], "Password must contain atleast 1 uppercase letter, 1 lowercase letter and 1 number.")
    

    def test_and_set_up_register_account(self):
        # Set up and Check if register succeed with valid values
        result = register_verification('test@example.com', 'Password1', 'Alon', 'Test')
        self.assertTrue(result[0])

##################################### RESTORE TESTS ######################################

    def test_invalid_email_restore_verification(self):
        # Check if restore fails due to invalid email format
        # Check if the correct error message is returned
        invalid_emails = ['test@exa', 'test@example.', 'testexample.com', 'test@@example.com', '@example.com']
        for email in invalid_emails:
            result = restore_verification(email, 'Password1', 'Alon', 'Test')
            self.assertFalse(result[0])
            self.assertEqual(result[1], "Please provide a properly formatted email.")


    def test_unregistered_email_restore_verification(self):
        # Check if restore fails due to a not registered email
        # Check if the correct error message is returned
        unregistered_emails = ['blabla1@example.com', 'blabla2@example.com', 'blabla3@example.com']
        for email in unregistered_emails:
            result = restore_verification(email, 'Password1', 'Alon', 'Test')
            self.assertFalse(result[0])
            self.assertEqual(result[1], "Error: This email is not registered.")


    def test_incorrect_user_values_restore_verification(self):
        # Check if restore fails due to incorrect user values
        # Check if the correct error message is returned
        incorrect_user_values = [['user1@example.com', 'Password1', 'Alon', 'Test'], 
                                 ['user2@example.com', 'Password1', 'Tal', 'Test'], 
                                 ['user3@example.com', 'Password1', 'Alon', 'Alon']]
        for values in incorrect_user_values:
            result = restore_verification(*values)
            self.assertFalse(result[0])
            self.assertEqual(result[1], "Error: The user info you provided is incorrect.")
        

    def test_invalid_password_restore_verification(self):
        # Check if restore fails due to invalid password
        # Check if the correct error message is returned
        invalid_length_passwords = ['passw', '342', 'fdfkndfngfdfd']
        for password in invalid_length_passwords:
            result = restore_verification('user1@example.com', password, 'John', 'Doe')
            self.assertFalse(result[0])
            self.assertEqual(result[1], "New password must contain 6-12 characters.")
        
        invalid_minimum_char_req_passwords = ["password1", "Password", "PASSWORD1"]
        for password in invalid_minimum_char_req_passwords:
            result = restore_verification('user1@example.com', password, 'John', 'Doe')
            self.assertFalse(result[0])
            self.assertEqual(result[1], "New password must contain atleast 1 uppercase letter, 1 lowercase letter and 1 number.")


    def test_and_set_up_restore_account(self):
        # Check if restore succeed with valid values
        result = restore_verification('user1@example.com', 'Password2', 'John', 'Doe')
        self.assertTrue(result[0])
        result = restore_verification('user1@example.com', 'Password1', 'John', 'Doe')
        self.assertTrue(result[0])

##################################### LOGIN TESTS ######################################

    def test_invalid_email_login_verification(self):
        # Check if login fails due to invalid email format
        # Check if the correct error message is returned
        invalid_emails = ['test@exa', 'test@example.', 'testexample.com', 'test@@example.com', '@example.com']
        for email in invalid_emails:
            result = login_verification(email, 'Password1')
            self.assertFalse(result[0])
            self.assertEqual(result[1], "Please provide a properly formatted email.")


    def test_unregistered_email_login_verification(self):
        # Check if login fails due to a not registered email
        # Check if the correct error message is returned
        unregistered_emails = ['blabla1@example.com', 'blabla2@example.com', 'blabla3@example.com']
        for email in unregistered_emails:
            result = login_verification(email, 'Password1')
            self.assertFalse(result[0])
            self.assertEqual(result[1], "Error: This email is not registered.")


    def test_incorrect_user_values_login_verification(self):
        # Check if login fails due to incorrect user password value
        # Check if the correct error message is returned
        incorrect_user_password_value = [['user1@example.com', 'Password'], 
                                 ['user2@example.com', 'Password'], 
                                 ['user3@example.com', 'Password']]
        for values in incorrect_user_password_value:
            result = login_verification(*values)
            self.assertFalse(result[0])
            self.assertEqual(result[1], "Error: Password incorrect.")
        

    def test_and_set_up_login_account(self):
        # Check if login succeed with valid values
        result = login_verification('user1@example.com', 'Password1')
        self.assertTrue(result[0])


    def test_delete_registered_test_account(self):
        # Delete registered test account (manually)
        user_id = get_user_id("test@example.com")[0][0]
        sql = f"""
            DELETE FROM users 
            WHERE user_id="{user_id}"
            """
        query_commit(sql)

##################################### TASKS TESTS ######################################

    def test_invalid_user_id_task_read(self):
        # Check if reading fails due to invalid user id

        result = read_tasks('')
        self.assertFalse(result)

        result = read_tasks('999')
        self.assertFalse(result)

        result = read_tasks('tal')
        self.assertFalse(result)


    def test_task_read(self):
        # Check if reading succeed with valid values
        result = read_tasks('1')
        self.assertTrue(len(result) >= 1)


    def test_invalid_user_id_task_add(self):
        # Check if adding fails due to invalid user id
        data = {"description" : "Praise Alon's unit tests", "date" : "2025-01-01"}

        result = add_task('', data)
        self.assertFalse(result)

        result = add_task('999', data)
        self.assertFalse(result)

        result = add_task('tal', data)
        self.assertFalse(result)


    def test_invalid_description_task_add(self):
        # Check if adding fails due to invalid description
        invalid_task_description = [{"description" : "", "date" : "2025-01-01"}, 
                                    {"description" : "sd", "date" : "2025-01-01"}, 
                {"description" : "The characters in description requirements is, minimum '3' and the maximum is '75' or less.", "date" : "2025-01-01"}]
        for data in invalid_task_description:
            result = add_task("1", data)
            self.assertFalse(result)


    def test_invalid_date_task_add(self):
        # Check if adding fails due to invalid date
        invalid_task_date = [{"description" : "Praise Alons unit tests", "date" : "2025/01/01"}, 
                {"description" : "Praise Alons unit tests", "date" : "2025.01.01"}, 
                {"description" : "Praise Alons unit tests", "date" : ""}, 
                {"description" : "Praise Alons unit tests", "date" : "10th of October"}]
        for data in invalid_task_date:
            result = add_task("1", data)
            self.assertFalse(result)


    def test_add_task(self):
        # Check if adding succeed with valid values
        data = {"description" : "Praise Alons unit tests", "date" : "2025-01-01"}
        length_before = read_tasks('1')
        add_task('1', data)
        length_after = read_tasks('1')
        self.assertTrue(len(length_before) < len(length_after))


    def test_invalid_date_status_update(self):
        # Check if updating status fails due to invalid task id
        invalid_status_task_id = [{"task_id" : "", "status" : "Finished", "description" : "Alons tests", "date" : "2025-01-01"}, 
                {"task_id" : "999", "status" : "Finished", "description" : "Alons tests", "date" : "2025-01-01"}, 
                {"task_id" : "tal", "status" : "Finished", "description" : "Alons tests", "date" : "2025-01-01"}]
        for values in invalid_status_task_id:
            result = update_status(values)
            self.assertFalse(result)


    def test_invalid_description_task_update(self):
        # Check if updating status fails due to invalid description
        invalid_status_task_description = [{"task_id" : 1, "status" : "Finished", "description" : "", "date" : "2023-12-23"}, 
                                    {"task_id" : 1, "status" : "Finished", "description" : "sd", "date" : "2023-12-23"}, 
                {"task_id" : 1, "status" : "Finished", "description" : "The characters in description requirements is, minimum '3' and the maximum is '75' or less.", "date" : "2023-12-23"}]
        for values in invalid_status_task_description:
            result = update_status(values)
            self.assertFalse(result)


    def test_invalid_date_task_update(self):
        # Check if updating status fails due to invalid date
        invalid_status_task_date = [{"task_id" : 1, "description" : "Workout", "date" : "2025/01/01"}, 
                {"task_id" : 1, "status" : "Finished", "description" : "Workout", "date" : "2025.01.01"}, 
                {"task_id" : 1, "status" : "Finished", "description" : "Workout", "date" : ""}, 
                {"task_id" : 1, "status" : "Finished", "description" : "Workout", "date" : "10th of October"}]
        for values in invalid_status_task_date:
            result = update_status(values)
            self.assertFalse(result)


    def test_valid_date_task_update(self):
        # Check if updating status succeed with valid values
        sql = f"SELECT * FROM tasks WHERE task_id=1" # Values: 1, 4, 'In-Progress', 'Workout', '2023-12-23'
        data = query_read_rows(sql)["rows"][0]
        self.assertEqual(data, (1, 4, 'In-Progress', 'Workout', '2023-12-23'))

        valid_task_task_id = [{"task_id" : 1, "status" : "Finished", "description" : "Alons tests", "date" : "2025-12-23"}, 
                {"task_id" : 1, "status" : "In-Progress", "description" : "Workout", "date" : "2023-12-23"}]
        for values in valid_task_task_id:
            result = update_status(values)
            self.assertIsNone(result)


    def test_invalid_date_task_update(self):
        # Check if updating fails due to invalid task id
        invalid_task_task_id = [{"task_id" : "", "description" : "Alons tests", "date" : "2025-01-01"}, 
                {"task_id" : "999", "description" : "Alons tests", "date" : "2025-01-01"}, 
                {"task_id" : "tal", "description" : "Alons tests", "date" : "2025-01-01"}]
        for values in invalid_task_task_id:
            result = update_task(values)
            self.assertFalse(result)


    def test_invalid_description_task_update(self):
        # Check if updating fails due to invalid description
        invalid_task_description = [{"task_id" : 1, "description" : "", "date" : "2023-12-23"}, 
                                    {"task_id" : 1, "description" : "sd", "date" : "2023-12-23"}, 
                {"task_id" : 1, "description" : "The characters in description requirements is, minimum '3' and the maximum is '75' or less.", "date" : "2023-12-23"}]
        for values in invalid_task_description:
            result = update_task(values)
            self.assertFalse(result)


    def test_invalid_date_task_update(self):
        # Check if updating fails due to invalid date
        invalid_task_date = [{"task_id" : 1, "description" : "Workout", "date" : "2025/01/01"}, 
                {"task_id" : 1, "description" : "Workout", "date" : "2025.01.01"}, 
                {"task_id" : 1, "description" : "Workout", "date" : ""}, 
                {"task_id" : 1, "description" : "Workout", "date" : "10th of October"}]
        for values in invalid_task_date:
            result = update_task(values)
            self.assertFalse(result)


    def test_valid_date_task_update(self):
        # Check if updating succeed with valid values
        sql = f"SELECT * FROM tasks WHERE task_id=1" # Values: 1, 4, 'In-Progress', 'Workout', '2023-12-23'
        data = query_read_rows(sql)["rows"][0]
        self.assertEqual(data, (1, 4, 'In-Progress', 'Workout', '2023-12-23'))

        valid_task_task_id = [{"task_id" : 1, "description" : "Alons tests", "date" : "2025-12-23"}, 
                {"task_id" : 1, "description" : "Workout", "date" : "2023-12-23"}]
        for values in valid_task_task_id:
            result = update_task(values)
            self.assertIsNone(result)


    def test_task_delete(self):
        # Check if deleting succeed with valid values
        description = "Praise Alons unit tests"
        date = "2025-01-01"
        sql = f"SELECT task_id FROM tasks WHERE user_id=1 AND description='{description}' AND date='{date}'"
        data = {"task_id" : query_read_rows(sql)["rows"][0][0]}
        length_before = read_tasks(1)
        delete_task(data)
        length_after = read_tasks(1)
        self.assertTrue(len(length_before) > len(length_after))


if __name__ == '__main__':
    unittest.main()
