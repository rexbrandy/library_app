import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from catalog.models import Loan, Book, BookInstance
from django.contrib.auth.models import User

class RenewBookForm(forms.ModelForm):
    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past.'))
        
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        return data
    
    class Meta:
        model = Loan
        fields = ['due_back']
        labels = {'due_back': _('Renewal date')}
        help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 1)')}


class LoanForms_TEST(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    book = forms.ModelChoiceField(queryset=Book.objects.filter(
        pk__in=BookInstance.objects.filter(status__exact='a').distinct().values_list('book'))
    )


    