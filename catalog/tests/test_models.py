from django.test import TestCase

from catalog.models import Author

class AuthorModelTst(TestCase):
    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name='Mary', last_name='Jane')

    