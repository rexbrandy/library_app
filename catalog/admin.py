from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language, Loan

admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Loan)

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('display_book_title', 'status')
    list_filter = ('status',)

    fieldsets = (
        (None, {
            'fields': ('book', 'id')
        }),
        ('Availability', {
            'fields': ('status',)
        })
    )

class BookInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre', 'summary', 'language')

    inlines = [BookInstanceInline]

class BookInline(admin.TabularInline):
    model = Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth')

    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death', 'bio' ]

    inlines = [BookInline]
