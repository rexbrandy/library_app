# Django Library Application
Basic Library application built using Django.

# TODO
- General
    - Add search functionality
    - Add a User page so that staff can click on a user profile and see all the borrowed books a user has.
    - Build  tests.
    - Author Country field might need to become a model choice like language.

- Author
    - Decide how Author section should be built: as seperate page or BookListView with view limited to Author

- Book
    - number of copies needs to be added to book list page.
    - Add loaner name to book instance section.
    - Book instance is added to bottom row but on reload is moved to the top.

- Loan
    - Build My Loans page (Maybe this should just be apart of the User page).
    - return functionality 
    - loan sorting and searching
    - Add loan return function
