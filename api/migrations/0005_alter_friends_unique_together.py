# Generated by Django 5.1 on 2025-01-15 00:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_friends_options_friends_from_user_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='friends',
            unique_together=set(),
        ),
    ]
