# Generated by Django 4.2.3 on 2023-07-08 11:34

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0003_alter_bookinstance_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loans',
            name='book',
            field=models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='catalog.bookinstance'),
        ),
        migrations.AlterField(
            model_name='loans',
            name='due_back',
            field=models.DateField(default=datetime.datetime(2023, 8, 7, 13, 34, 11, 63390), help_text='Date due to be returned'),
        ),
        migrations.AlterField(
            model_name='loans',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
    ]
