from collections import deque
import datetime
import numbers
from urllib import response

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone as django_timezone

from django.contrib.auth.models import User
from catalog.models import Loan, Author, Book, BookInstance, Genre, Language

class IndexViewTest(TestCase):
    def test_view_url_exists(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


class SearchViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_author = Author.objects.create(first_name='Mary', last_name='Jane')
        Book.objects.create(
            title='Book Title',
            summary='My book summary',
            author=test_author,
        )

    def test_view_url_exists(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)

    def test_accessible_by_name(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)

    def test_book_search(self):
        response = self.client.post('/search/', 
            data={'search': 'Book Title'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['search_results']) > 0)

    def test_view_uses_correct_template(self):
        response = self.client.get('/search/')
        self.assertTemplateUsed(response, 'catalog/search.html')

    def test_author_search(self):
        pass

class AccountViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='testuser1', password='G00d_Pass')
        test_author = Author.objects.create(
            first_name = 'Mary',
            last_name = 'Jane',
            country = 'Australia',
            date_of_birth = datetime.datetime.now(),
            date_of_death = datetime.datetime.now(),
        )

        test_book = Book.objects.create(
            title='Book Title',
            summary='My book summary',
            author=test_author,
        )
        
        test_book_instance = BookInstance.objects.create(book=test_book)
        test_returned_book_instance = BookInstance.objects.create(book=test_book)

        Loan.objects.create(
            book_instance = test_book_instance,
            user = test_user
        )

        Loan.objects.create(
            book_instance = test_returned_book_instance,
            user = test_user,
            due_back = django_timezone.now() - datetime.timedelta(30), 
            returned_date = django_timezone.now() - datetime.timedelta(1)
        )

    def test_view_url_exists(self):
        login = self.client.login(username='testuser1', password='G00d_Pass')
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 200)

    def test_accessible_by_name(self):
        login = self.client.login(username='testuser1', password='G00d_Pass')
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='G00d_Pass')
        response = self.client.get(reverse('account'))

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/user_detail.html')

    def test_accessible_by_name(self):
        login = self.client.login(username='testuser1', password='G00d_Pass')
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/accounts/login/?next=/account/')

    def test_loaned_books_appear(self):
        login = self.client.login(username='testuser1', password='G00d_Pass')
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['loan_list']) > 0)

    def test_returned_books_appear(self):
        login = self.client.login(username='testuser1', password='G00d_Pass')
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['loan_list_returned']) > 0)


class BookListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_books = 13

        test_author = Author.objects.create(
            first_name = 'Mary',
            last_name = 'Jane',
        )

        test_book = Book.objects.create(
            title='Book Title',
            summary='My book summary',
            author=test_author,
        )

        for i in number_of_books:
            Book.objects.create(
                title=f'Book {i}',
                summary=f'Test Book Number {i}',
                author=test_author
            )
        
    def test_view_url_exists(self):
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)

    def test_accessible_by_name(self):
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/books/')
        self.assertTemplateUsed(response, 'catalog/book_list.html')

    def test_view_pagination_is_ten(self):
        response = self.client.get('/books/')
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['book_list']), 10)
        
    def test_view_correct_number_displaying(self):
        response = self.client.get('/books/'+'?page=2')
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['book_list']), 3)
        

class BookDetailViewTest(TestCase):
    pass

class BookCreateViewTest(TestCase):
    pass

class BookDeleteViewTest(TestCase):
    pass

class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_authors = 13

        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name = f'Mary {author_id}',
                last_name = f'Jane {author_id}',
                country = 'Australia',
                date_of_birth = datetime.datetime.now(),
                date_of_death = datetime.datetime.now(),
            )
    
    def test_view_url_exists(self):
        response = self.client.get('/authors/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/authors/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_list.html')

    def test_view_pagination_is_ten(self):
        response = self.client.get('/authors/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['author_list']), 10)

    def test_view_lists_all_authors(self):
        response = self.client.get(reverse('authors')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['author_list']), 3)


# OLD
class LoanedBooksByUserListViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='G00d_Pass')
        test_user2 = User.objects.create_user(username='testuser2', password='G00d_Pass')

        test_user1.save()
        test_user2.save()

        test_author = Author.objects.create(
            first_name = 'Mary',
            last_name = 'Jane',
            country = 'Australia',
            date_of_birth = datetime.datetime.now(),
            date_of_death = datetime.datetime.now(),
        )

        test_genre = Genre.objects.create(name='Fantasy')
        test_language = Language.objects.create(name='English')
        test_book = Book.objects.create(
            title='Book Title',
            summary='My book summary',
            author=test_author,
            language=test_language,
        )

        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book) # Direct assignment of many-to-many types not allowed.
        test_book.save()

        number_of_copies = 30
        
        for book_copy in range(number_of_copies):
            book_instance = BookInstance.objects.create(
                book=test_book,
                status='m'
            )
            book_instance.save()

            borrower = test_user1 if book_copy % 2 else test_user2
            due_back = django_timezone.now() + datetime.timedelta(30)

            Loan.objects.create(
                user = borrower,
                book_instance = book_instance,
                due_back = due_back,

            )
        

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my-loans'))
        self.assertRedirects(response, '/accounts/login/?next=/loan/all_loans/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='G00d_Pass')
        response = self.client.get(reverse('my-loans'))

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/borrowed_books.html')
