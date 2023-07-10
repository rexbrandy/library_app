import datetime

from django.test import TestCase
from django.utils import timezone as django_timezone

from catalog.forms import RenewBookForm

class RenewBookFormTest(TestCase):
    def test_renew_form_date_field_label(self):
        form = RenewBookForm()
        self.assertTrue(
            form.fields['due_back'].label is None 
            or form.fields['due_back'].label == 'Renewal date'
        )

    def test_renew_form_help_text(self):
        form = RenewBookForm()
        self.assertEqual(
            form.fields['due_back'].help_text,
            'Enter a date between now and 4 weeks (default 1)'
        )

    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'due_back': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=5)
        form = RenewBookForm(data={'due_back': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form = RenewBookForm(data={'due_back': date})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_max(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4)
        form = RenewBookForm(data={'due_back': date})
        self.assertTrue(form.is_valid())
    



