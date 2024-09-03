# Personal Budgeting API
This is a RESTful API for managing personal budgeting. It allows users to create accounts, define categories, set budgets, and record transactions. The API is built with Python using the Flask framework, and it uses MySQL as the database and JWT for authentication.

## Features
- User Management: Register and authenticate users with JWT-based token authentication.
- Category Management: Create and manage categories for organizing transactions.
- Budget Management: Define and manage budgets for different categories.
- Transaction Management: Add and track transactions under specific categories and budgets.

## Technology Stack
- Language: Python
- Framework: Flask
- Database: MySQL
- Authentication: JWT (JSON Web Tokens)

## Installation
Clone the repository:
```bash
git clone https://github.com/firmanasgani/personal-budgeting-api.git
cd personal-budgeting-api
```

Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

or 

```bash
pipenv install
```

Set up the database:

Create a MySQL database. 
Update the database configuration in the utils/connection.py file with your MySQL credentials.

Run the application:

```bash
flask run
```

License
This project is licensed under the MIT License. See the LICENSE file for details.
