# Generated by Django 4.1.3 on 2022-12-06 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0013_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='account',
            new_name='author',
        ),
    ]