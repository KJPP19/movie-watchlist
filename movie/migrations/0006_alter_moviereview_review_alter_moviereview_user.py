# Generated by Django 4.1.7 on 2023-04-03 11:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movie', '0005_remove_moviereview_user_moviereview_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviereview',
            name='review',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='moviereview',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]