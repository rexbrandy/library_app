from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),

    # Account 
    path('account/', views.user_detail, name='account'),
    path('accounts/register/', views.user_register, name='register'),

    # Books
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),   
    path('book/create', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete', views.BookDelete.as_view(), name='book-delete'),
    path('book/create_instance', views.add_book_instance_ajax, name='book-instance-create'),

    # Authors
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('author/create', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete', views.AuthorDelete.as_view(), name='author-delete'),

    # Loans
    path('loan/my_loans/', views.LoanedBooksByUserListView.as_view(), name='my-loans'),
    path('loan/<int:pk>/renew/', views.renew_loan, name='loan-renew'),
    path('loan/<int:pk>/return/', views.return_loan, name='loan-return'),
    path('loan/all_loans/', views.LoanedBooksByAllListView.as_view(), name='all-loans'),
    path('loan/create/', views.loan_create, name='loan-create'),

]