# Generated by Django 3.2.8 on 2021-11-03 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0004_remove_user_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='visits',
        ),
        migrations.AddField(
            model_name='user',
            name='no_of_visits',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
