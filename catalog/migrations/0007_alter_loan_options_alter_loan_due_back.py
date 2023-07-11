# Generated by Django 4.2.3 on 2023-07-08 13:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_loan_delete_loans'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='loan',
            options={'permissions': (('can_mark_returned', 'Set loan as returned'),)},
        ),
        migrations.AlterField(
            model_name='loan',
            name='due_back',
            field=models.DateField(default=datetime.datetime(2023, 8, 7, 15, 12, 2, 770384), help_text='Date due to be returned'),
        ),
    ]