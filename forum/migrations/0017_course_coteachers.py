# Generated by Django 3.1.6 on 2021-08-26 21:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0016_auto_20210826_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='coteachers',
            field=models.ManyToManyField(blank=True, related_name='course_of_coteacher', to=settings.AUTH_USER_MODEL),
        ),
    ]
