# Generated by Django 3.1.6 on 2021-06-13 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='description',
            field=models.TextField(blank=True, max_length=10000),
        ),
    ]
