# Generated by Django 4.0.4 on 2022-05-17 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_delete_usertwo'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='UserForm',
        ),
    ]
