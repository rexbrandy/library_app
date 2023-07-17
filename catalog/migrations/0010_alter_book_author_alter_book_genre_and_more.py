# Generated by Django 4.2.3 on 2023-07-13 22:54

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_alter_author_date_of_birth_alter_loan_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(help_text='Enter book author', null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.author'),
        ),
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(help_text='Select a Genre for this book', to='catalog.genre'),
        ),
        migrations.AlterField(
            model_name='book',
            name='language',
            field=models.ForeignKey(help_text='Select book language', null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.language'),
        ),
        migrations.AlterField(
            model_name='book',
            name='summary',
            field=models.TextField(help_text='Enter a description of the book', max_length=1000),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(help_text='Enter book title', max_length=200),
        ),
        migrations.AlterField(
            model_name='loan',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, help_text='Date borrowed'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='due_back',
            field=models.DateField(default=datetime.datetime(2023, 8, 12, 22, 54, 41, 830008, tzinfo=datetime.timezone.utc), help_text='Date due to be returned'),
        ),
    ]
