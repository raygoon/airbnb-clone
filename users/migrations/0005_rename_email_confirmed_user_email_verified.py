# Generated by Django 3.2.8 on 2022-08-01 04:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_email_secret'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='email_confirmed',
            new_name='email_verified',
        ),
    ]
