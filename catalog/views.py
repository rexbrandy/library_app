import datetime
import re
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import modelformset_factory

from .forms import RenewBookForm
from .models import Book, BookInstance, Author, Loan
from catalog import forms

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

##############
# BOOK VIEWS
#
class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class BookCreate(generic.edit.CreateView):
    model = Book
    fields = '__all__'

class BookUpdate(generic.edit.UpdateView):
    model = Book
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        book_instances_qs = BookInstance.objects.all().filter(book=self.kwargs['pk'])
        BookInstanceFormset = modelformset_factory(BookInstance, extra=0, can_delete=True, fields=['status', 'id'])

        context['book_instance_formset'] = BookInstanceFormset(queryset=book_instances_qs)

        return context

    def post(self, request, **kwargs):
        BookInstanceFormset = modelformset_factory(BookInstance, extra=0, can_delete=True, fields=['status', 'id'])
        formset = BookInstanceFormset(request.POST)

        if formset.is_valid():
            for form in formset:
                print(form.is_valid())
                if form.is_valid():
                    form.save()
        
        return super(BookUpdate, self).post(request, **kwargs)

class BookDelete(generic.edit.DeleteView):
    model = Book
    success_url = reverse_lazy('books')


################
# AUTHOR VIEWS
#
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author

class AuthorCreate(generic.edit.CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth']

class AuthorUpdate(generic.edit.UpdateView):
    model = Author
    fields = '__all__'

class AuthorDelete(generic.edit.DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


##############
# LOAN VIEWS 
#
class LoanCreate(LoginRequiredMixin, generic.edit.CreateView):
    model = Loan
    fields = ['user', 'book_instance']

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
    paginate_by = 10

    template_name = 'catalog/all_borrowed_books.html'


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_loan_librarian(request, pk):
    loan = get_object_or_404(Loan, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            # if submitted form is valid we update the due date with the clean form data
            loan.due_back = form.cleaned_data['renewal_date']
            loan.save()

            return HttpResponseRedirect(reverse('all-loans'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=1)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'loan': loan
    }

    return render(request, 'catalog/book_renew_librarian.html', context=context)
    
