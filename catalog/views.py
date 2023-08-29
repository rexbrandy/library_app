import datetime
from multiprocessing import context
import re

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import modelformset_factory
from django.utils import timezone as django_timezone

from .forms import RenewBookForm, LoanForm, ReturnBookForm
from .models import Book, BookInstance, Author, Loan
from django.contrib.auth.models import User


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
# USER VIEWS
#
class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = User

@login_required
def user_detail(request):
    user = request.user
    loans = Loan.objects.filter(user=user).filter(returned_date__isnull=True)
    returned_loans = Loan.objects.filter(user=user).filter(returned_date__isnull=False)

    has_past_loans = (True if Loan.objects.filter(user=user).filter(returned_date__isnull=False).count() > 0 else False)

    print(returned_loans)

    context = {
        'has_past_loans': has_past_loans,
        'loan_list': loans,
        'loan_list_returned': returned_loans
    }

    return render(request, 'catalog/user_detail.html', context=context)


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
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death', 'bio']

class AuthorUpdate(generic.edit.UpdateView):
    model = Author
    fields = '__all__'

class AuthorDelete(generic.edit.DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


##############
# LOAN VIEWS 
#

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

    def get_queryset(self):
        return (
            Loan.objects.filter(returned_date__isnull=True)
        )

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def loan_create(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)

        if form.is_valid():
            book_instance = form.cleaned_data['book'].get_available_copy()
            loaner = form.cleaned_data['user']

            loan = Loan(user=loaner, book_instance=book_instance)
            book_instance.set_on_loan()
            loan.save()

            return HttpResponseRedirect(reverse('all-loans'))
    else:
        form = LoanForm()

    return render(request, 'catalog/loan_form.html', context={'form': form})


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_loan(request, pk):
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

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def return_loan(request, pk):
    loan = get_object_or_404(Loan, pk=pk)

    if request.method == 'POST':
        form = ReturnBookForm(request.POST)

        if form.is_valid():
            loan.returned_date = form.cleaned_data['returned_date']
            loan.save()

            return HttpResponseRedirect(reverse('all-loans'))
    else:
        form=ReturnBookForm(initial={'returned_date': django_timezone.now()})

    context = {
        'form': form,
        'loan': loan
    }

    return render(request, 'catalog/loan_return.html', context=context)


#############
# AJAX VIEWS
#

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def add_book_instance_ajax(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        try: 
            book = Book.objects.get(pk=request.POST['book_id'])
            new_book_instance = BookInstance(book=book)
            new_book_instance.save()

            return JsonResponse({'new_book_id': new_book_instance.pk}, status=200)
        except Exception as e:
            return JsonResponse({'error': e.pk}, status=400)
    return JsonResponse({'error': 'unknown'}, status=400)