# Generated by Django 2.1.5 on 2020-09-03 04:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rango', '0007_userprofile_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='user_likes',
            field=models.ManyToManyField(blank=True, related_name='user_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
