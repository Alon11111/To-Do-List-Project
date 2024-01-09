# To-Do List Project

This project is a simple To-Do List application implemented using Flask (a Python web framework) and SQLite for data storage.

## Overview

The To-Do List Project provides functionalities for users to register, log in, add tasks, manage task status, and view tasks based on their status (In-Progress, Finished, or Expired).

### Features

- User authentication (register, login, and restore password)
- Task management (add, delete, update status and details)
- Task categorization based on status

## Getting Started

### Prerequisites

- Python 3.x
- Flask (`pip install flask`)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Alon11111/To-Do-List-Project.git
    cd To-Do-List-Project
    ```

2. Set up the virtual environment and install dependencies:

    ```bash
    python -m venv venv
    source venv/bin/activate (for Unix/macOS) or venv\Scripts\activate (for Windows)
    pip install -r requirements.txt
    ```

3. Run the application:

    ```bash
    python app.py
    ```

4. Access the application in your browser at `http://localhost:5000`.
### Usage

#### Routes

- `/`: Home page displays the To-Do List interface.
- `/login`: User login page.
- `/register`: User registration page.
- `/restore`: Password restoration page.
- `/log_out`: Log out route.

#### API Routes

- `/read_name`: Fetches the first name of the logged-in user.
- `/read_tasks`: Retrieves tasks for the logged-in user.
- `/add_task`: Adds a new task for the logged-in user.
- `/delete_task`: Deletes a task.
- `/update_status`: Updates task status.
- `/update_task`: Updates task details.

### Project Structure

- `app.py`: Contains Flask routes and API endpoints.
- `data.py`: Handles database setup and SQL queries.
- `tasks_functions.py`, `user_functions.py`, `static_texts.py`: Functions handling task/user operations and static texts.
- `home.js` and `home.html`: Frontend logic and UI for the To-Do List.

### Contributing

Feel free to fork the project, make changes, and create a pull request. Contributions are welcomed!
