# LibSys

## Table of Contents

- [Installation](#Installation)
- [Documentation](#Documentation)


### College Project : Library Management System 

This Project is a part of my college project. The main aim of this project is to create a library management system. The system will be able to manage books, customers, reservations and the borrowing process. 

#### Technologies Used

- **Python and Django**:
  - Django: I used Django Rest Framework (DRF) to create the API that will be used to manage the library system.

- **JavaScript**:
  - Axios: Used to make HTTP requests from the client side to the API.

#### Project Finality

The project refers to the development of a bookstore management system, as part of the evaluation process for the Software Project course taught by Professor Dr. Baldoíno Fonseca dos Santos Neto at the Federal University of Alagoas (UFAL). The main objective of the project is to create a system that allows the management of books, customers, reservations and the borrowing process while put into practice the concepts learned during the course.

#### How it works

1. **Implementation of the API in Django**:
   - Creation of an API using Django Rest Framework.

2. **Implementation of the client side with JavaScript, HTML and CSS**:
   - The scripts are responsible for making requests to the API to manage the library system.
   - The client side is a simple HTML page with JavaScript scripts.
   - Axios is used to make HTTP requests to the API.

## Installation

### Prerequisites

Certify yourself to have the following installed on your local environment:
- [Python](https://www.python.org/) 
- [pip](https://pip.pypa.io/en/stable/installation/) 

### Step 1: Clone the Project Repository

Clone the `libsys` project repository to your local machine:
    

### Step 2: Configure the Django Environment

1. **Create a Virtual Environment**
    Create a new Python virtual environment in the project directory:
   ```bash
   python -m venv venv
   source venv/bin/activate  # on Windows use `venv\Scripts\activate`
   ```

2. **Install Required Dependencies**
   Install all required dependencies using pip, they are listed in the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` File**
    Create a new `.env` file in the `libsys` directory and add the following environment variables:
   ```env
   EMAIL_HOST=smtp.your-email-provider.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@provider.com
   EMAIL_HOST_PASSWORD=your-email-password
   EMAIL_USE_TLS=True
   ```

### Step 3: Run the Project

1. **Run the Django Server**

   If it is the first time you are running the project, you will need to create the database and run the migrations:
   ```bash
    python manage.py migrate
    ```

   Run the Django development server using the `manage.py` script:
   ```bash
   python manage.py runserver
   ```


3. **Access the Web Aplication**
   Access the web application opening any HTML file in the `webApp\public\views` directory with live server.

## Documentation

The documentation of the project can be accessed using swagger. To access the documentation, run the project and access the following URL in your browser:
```bash
http://127.0.0.1:8000/swagger/
```
This will open the Swagger documentation page with all the available endpoints and their descriptions.

