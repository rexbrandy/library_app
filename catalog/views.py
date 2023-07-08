from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Book, BookInstance, Author, Loan

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

# Book Views
class BookListView(generic.ListView):
    model = Book
    paginate_by = 1

class BookDetailView(generic.DetailView):
    model = Book


# Author Views
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = Loan
    template_name = 'catalog/borrowed_books.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            Loan.objects.filter(user=self.request.user)
            .filter(returned_date__isnull=True)
        )

class LoanedBooksByAllListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'

    model = Loan
    template_name = 'catalog/all_borrowed_books.html'
