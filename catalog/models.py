from tkinter import FLAT
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone as django_timezone

import datetime
import uuid

class Language(models.Model):
    "Langauge code and language name according to ISO 639-1"
    language_code = models.CharField(max_length=6, help_text='Enter 2 letter language code e.g. ("en" for "English")')
    name = models.CharField(max_length=64, help_text='Enter language name e.g. English')

    def __str__(self):
        
        return f'({self.language_code}) {self.name}'

class Genre(models.Model):
    "Book genre"
    name = models.CharField(max_length=100, help_text='Enter genre name.')

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=100, help_text='Enter Author first name.')
    last_name = models.CharField(max_length=100, help_text='Enter Author last name.')
    country = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField('Born', null=True, blank=True, help_text='Enter Author date of birth.')
    date_of_death = models.DateField('Died', null=True, blank=True, help_text='Enter Author date of death.')

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    @property
    def number_of_books(self):
        return len(self.book_set.all())

    @property
    def dob_year(self):
        return self.date_of_birth.year

    @property
    def dod_year(self):
        return self.date_of_death.year

    @property
    def distinct_genres(self):
        pks = self.book_set.all().values_list('genre__pk', flat=True)
        return Genre.objects.filter(pk__in=pks).distinct()
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    title = models.CharField(max_length=200, help_text='Enter book title')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, help_text="Enter book author")
    summary = models.TextField(
        max_length=1000, 
        help_text='Enter a description of the book'
    )
    genre = models.ManyToManyField(
        Genre, 
        help_text='Select a Genre for this book'
    )
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, help_text="Select book language")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ' '.join(genre.name for genre in self.genre.all()[:3])

    def is_available(self):
        return bool(self.bookinstance_set.all().count() > 0)

    def copies_available(self):
        return self.bookinstance_set.filter(status__exact='a').count()


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)

    LOAN_STATUS = (
        ('m', 'Maintence'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book Availability'
    )

    def __str__(self):
        return f'{self.book.title} ({self.id}))'

    def display_book_title(self):
        return self.book.title
    
    def get_loan_status(self):
        return (
            ('m', 'Maintence'),
            ('o', 'On loan'),
            ('a', 'Available'),
            ('r', 'Reserved'),
        )

class Loan(models.Model):
    book_instance = models.OneToOneField(BookInstance, on_delete=models.RESTRICT)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    date = models.DateField(
        default=django_timezone.now,
        help_text='Date borrowed'
    )
    due_back = models.DateField(
        default= django_timezone.now() + datetime.timedelta(30), 
        help_text='Date due to be returned'
    )
    returned_date = models.DateField(null=True, blank=True, help_text='Date book was returned')

    @property
    def is_overdue(self):
        return bool(self.due_back and datetime.date.today() > self.due_back)
    
    def __str__(self):
        return f'{self.book_instance.book.title} - {self.user.username}'

    def set_returned_to_now(self):
        if not self.returned_date:
            self.returned_date = datetime.date.today()

    class Meta:
        permissions = (('can_mark_returned', 'Set loan as returned'),)