# Generated by Django 3.2.8 on 2021-11-03 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0005_auto_20211103_2135'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='no_of_visits',
        ),
    ]
