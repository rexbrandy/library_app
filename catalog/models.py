import re
from django.db import models
from django.urls import reverse
import uuid

class Language(models.Model):
    language_code = models.CharField(max_length=6, help_text='Enter language code e.g. ("en" for "English")')
    name = models.CharField(max_length=64, help_text='Enter language name e.g. English')

    def __str__(self):
        return f'({self.language_code}) {self.name}'

class Author(models.Model):
    first_name = models.CharField(max_length=100, help_text='Enter Author first name.')
    last_name = models.CharField(max_length=100, help_text='Enter Author last name.')
    date_of_birth = models.DateField(null=True, blank=True, help_text='Enter Author date of birth.')

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Genre(models.Model):
    name = models.CharField(max_length=100, help_text='Enter genre name.')

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200, help_text='Enter book title.')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(
        max_length=1000, 
        help_text='Enter a description of the book.'
    )
    genre = models.ManyToManyField(
        Genre, 
        help_text='Select a Genre for this book.'
    )
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ' '.join(genre.name for genre in self.genre.all()[:3])


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    due_back = models.DateField(null=True, blank=True, help_text='Date due to be returned')
    
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

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title})'

    def display_book_title(self):
        return self.book.title