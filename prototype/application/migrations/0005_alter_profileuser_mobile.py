# Generated by Django 4.0.3 on 2022-04-06 12:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_alter_profileuser_salutation_alter_profileuser_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileuser',
            name='mobile',
            field=models.CharField(error_messages={'unique': 'The phone you entered has already been registered!'}, max_length=10, unique=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')]),
        ),
    ]
