# Generated by Django 3.2.8 on 2021-12-01 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gym_app', '0003_rename_users_userprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userclasses',
            old_name='user_id',
            new_name='user',
        ),
    ]
