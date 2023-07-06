from django.shortcuts import render, HttpResponse
from .models import Book, BookInstance, Author, Genre

def index(request):
    num_books = Book.objects.all().count()
    num_copies = BookInstance.objects.all().count()
    num_avail = BookInstance.objects.filter(status__exact='a').count()

    num_authors = Author.objects.all().count()

    context = {
        'num_books': num_books,
        'num_copies': num_copies,
        'num_avail': num_avail,
        'num_authors': num_authors,
    }

    return render(request, 'index.html', context=context)