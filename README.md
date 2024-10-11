# password-manager-app
A simple password manager app with a easy to follow GUI.

## How to run this project

**Prerequisites**
- Python 3.x installed on your machine

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Dilpreet-singh-13/password-manager-app.git
   cd Expense-tracker
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Unix or MacOS use `source venv/bin/activate`
   ```

3. Install Dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Set Up the Database
   
   This project supports multiple databases such as PostgreSQL, MySQL, or SQLite.
   You can configure it according to your preferred database.
   **Using PostgreSQL (Default Setup)**
   - Make sure you have PostgreSQL installed and running.
   - Create a database for the project:
     ```bash
     psql -U your_postgres_username
     CREATE DATABASE your_db_name;
     ```

6. Configure Environment Variables
   The project uses environment variables to store sensitive information such as database credentials.
   Create a `.env` file in the root directory of the project and add the following:
   ```bash
   DB_USERNAME=your_postgres_username
   DB_PASSWORD=your_postgres_password
   DB_HOST=localhost
   DB_NAME=your_db_name
   ```

### Running the Application
   Finally, run the application:
  ```bash
  python app.py
  
  ```

## Features
- **Multiple Users:** Allows multiple users
- **Functionality:** Ability to add, edit, delete, view passwords
- **Simple GUI**
