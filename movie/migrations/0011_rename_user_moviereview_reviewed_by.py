# Generated by Django 4.1.7 on 2023-04-26 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0010_alter_moviereview_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='moviereview',
            old_name='user',
            new_name='reviewed_by',
        ),
    ]
