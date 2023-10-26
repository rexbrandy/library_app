from dataclasses import field
from django.test import TestCase

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
