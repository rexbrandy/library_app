import datetime

from urllib import response
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone as django_timezone

from django.contrib.auth.models import User
from catalog.models import Loan, Author, Book, BookInstance, Genre, Language

class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_authors = 13

        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name = f'Mary {author_id}',
                last_name = f'Jane {author_id}',
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



class LoanedBooksByUserListViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='G00d_Pass')
        test_user2 = User.objects.create_user(username='testuser2', password='G00d_Pass')

        test_user1.save()
        test_user2.save()

        test_author = Author.objects.create(first_name='John', last_name='Smith')
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
                due_back = due_back
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my-loans'))
        self.assertRedirects(response, '/accounts/login/?next=/my_loans/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='G00d_Pass')
        response = self.client.get(reverse('my-loans'))

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/borrowed_books.html')
    