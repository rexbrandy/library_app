# Django Library Application

This is a small Library app built as a small exercise on Django. This project was mainly for the purposes of research and learning.

## Table of Contents

- [About](#about)
- [Getting Started](#getting-started)

## About
This is a small library application project.
In this app a User is able to join the library and view the books and authors available.
Staff members are able to add/edit books and authors, loan books to users and view all loans outstanding or otherwise.

Most of the code in this project comes from the [MDN Django tutorial](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Tutorial_local_library_website).

## Getting Started

To run this project clone the repo, install the requirements and run locally.
This project is not ready for deployment yet but soon I will update the repo and add deployment steps.

```shell
$ git clone https://github.com/rexbrandy/library_app.git
$ cd library_app
$ python -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
$ python manage.py migrate # create data models
$ python manage.py runserver
```

## TODO
- General
    - Build  tests.
    
- Loan
    - loan sorting and searching
    - User shouldnt allowed to loan same book twice

- Misc
    - Author Country field might need to become a model choice like language.
    - Fix table population scripts (Genre, Languages)
    - Add wishlist.
    - Fix `................/Users/yeliab/Projects/library_app/env/lib/python3.9/site-packages/django/views/generic/list.py:91: UnorderedObjectListWarning: Pagination may yield inconsistent results with an unordered object_list: <class 'catalog.models.Book'> QuerySet.`
