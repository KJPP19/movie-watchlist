# Generated by Django 4.1.7 on 2023-04-03 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0003_moviereview'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviereview',
            name='review',
            field=models.TextField(null=True),
        ),
    ]
