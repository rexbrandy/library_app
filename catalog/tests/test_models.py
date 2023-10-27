from cgi import test
from dataclasses import field
import datetime
from django.test import TestCase

from django.contrib.auth.models import User
from catalog.models import Author, Book, BookInstance, Loan, Language, Genre

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name='Mary', last_name='Jane')

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_date_of_birth(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_birth').verbose_name
        self.assertEqual(field_label, 'Born')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        self.assertEqual(author.get_absolute_url(), '/author/1')

class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = Author.objects.create(first_name='Mary', last_name='Jane')
        cls.language = Language.objects.create(name='English')
        cls.genre1 = Genre.objects.create(name='Fantasy')
        cls.genre2 = Genre.objects.create(name='Adventure')
        test_book = Book.objects.create(
            title='Book Title',
            summary='My book summary',
            author=cls.author,
            language=cls.language,
        )

        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)

    def test_title_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')
        
    def test_title_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_summary_help_text(self):
        book = Book.objects.get(id=1)
        help_text = book._meta.get_field('summary').help_text
        self.assertEqual(help_text, 'Enter a description of the book')

    def test_summary_help_text(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('summary').max_length
        self.assertEqual(max_length, 1000)

    def test_get_absolute_url(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.get_absolute_url(), '/book/1')

    def test_display_genre(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.display_genre(), 'Fantasy Adventure')

    def test_bookinstance_creates_default(self):
        book = Book.objects.get(id=1)
        self.assertTrue(len(book.bookinstance_set.all()) == 1)

class BookInstanceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = Author.objects.create(first_name='Mary', last_name='Jane')
        cls.genre = Genre.objects.create(name='Fantasy')
        test_book = Book.objects.create(
            title='Book Title',
            summary='My book summary',
            author=cls.author,
        )

        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)

        BookInstance.objects.create(
            book=test_book,
            status='m'
        )

    def test_status_help_text(self):
        book_instance = BookInstance.objects.last()
        help_text = book_instance._meta.get_field('status').help_text
        self.assertEqual(help_text, 'Book Availability')

    def test_status_choices(self):
        book_instance = BookInstance.objects.last()
        choices = book_instance._meta.get_field('status').choices
        self.assertEqual(choices, (
            ('m', 'Maintence'),
            ('o', 'On loan'),
            ('a', 'Available'),
            ('r', 'Reserved'),
        ))

    def test_set_default_status(self):
        book_instance = BookInstance.objects.last()
        self.assertTrue(book_instance.status == 'm')

    def test_set_on_loan(self):
        book_instance = BookInstance.objects.last()
        book_instance.set_on_loan()
        self.assertTrue(book_instance.status == 'o')

class LoanModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = Author.objects.create(first_name='Mary', last_name='Jane')
        cls.genre = Genre.objects.create(name='Fantasy')
        test_book = Book.objects.create(
            title='Book Title',
            summary='My book summary',
            author=cls.author,
        )
        test_user = User.objects.create_user(
            username='testuser1', 
            password='G00d_Pass'
        )

        test_book_instance = BookInstance.objects.last()

        Loan.objects.create(
            book_instance = test_book_instance,
            user = test_user,
        )

    def test_date_is_now(self):
        loan = Loan.objects.get(id=1)
        self.assertEqual(loan.date, datetime.date.today())

    def test_date_help_text(self):
        loan = Loan.objects.get(id=1)
        date = loan._meta.get_field('date').help_text
        self.assertEqual(date, 'Date borrowed')

    def test_due_back_date(self):
        loan = Loan.objects.get(id=1)
        self.assertEqual(loan.due_back, datetime.date.today()+ + datetime.timedelta(30))

    def test_due_back_help_text(self):
        loan = Loan.objects.get(id=1)
        due_back = loan._meta.get_field('due_back').help_text
        self.assertEqual(due_back, 'Date due to be returned')

    def test_returned_date_help_text(self):
        loan = Loan.objects.get(id=1)
        date = loan._meta.get_field('returned_date').help_text
        self.assertEqual(date, 'Date book was returned')


