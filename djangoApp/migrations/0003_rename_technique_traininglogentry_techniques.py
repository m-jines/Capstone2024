# Generated by Django 4.2.2 on 2023-06-30 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangoApp', '0002_rename_date_traininglogentry_date_added_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='traininglogentry',
            old_name='technique',
            new_name='techniques',
        ),
    ]
