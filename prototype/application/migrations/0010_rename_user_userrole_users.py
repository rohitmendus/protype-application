# Generated by Django 4.0.3 on 2022-04-08 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0009_alter_userrole_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userrole',
            old_name='user',
            new_name='users',
        ),
    ]
