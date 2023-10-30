# Django Library Application

This is a small Django library application designed to manage a library's collection of book, members and loan transactions.
It provides a user friendly interface for librarians to manage there library resources and allows members to browse the library's collection.

## Table of Contents

- [Features](#features)
- [Dependencies](#dependencies)
- [Installation](#installation)

## Features

- **Book Management**
    - Add, edit, and delete books.
    - Categorize books by genre and author.
    - Keep track of book copies and their availability.

- **Patron Management**
    - Manage library patrons.
    - View patron details and history.

- **Loan Transactions**
    - Issue and return books for patrons.
    - Track due dates and late returns.

- **User Authentication**
    - Different user roles (librarian, admin, and patron).
    - Authentication and authorization for secure access.

## Dependencies

- Python==3.9
- Django==4.2
- django-widget-tweaks==1.4.12


## Installation

To run this project clone the repo, install the requirements and run locally.
```shell
$ git clone https://github.com/rexbrandy/library_app.git
$ cd library_app
$ python -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py runserver
```
Your library application should now be running locally at http://127.0.0.1:8000/. Access the admin interface at http://127.0.0.1:8000/admin/.git 