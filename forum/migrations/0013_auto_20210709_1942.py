# Generated by Django 3.1.6 on 2021-07-10 00:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0012_auto_20210709_1938'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignment',
            old_name='grouping',
            new_name='module',
        ),
    ]