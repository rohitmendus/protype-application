# Generated by Django 4.0.3 on 2022-04-06 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_alter_profileuser_department_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileuser',
            name='salutation',
            field=models.CharField(choices=[('Dr', 'Dr'), ('Mr', 'Mr'), ('Ms', 'Ms'), ('Prof', 'Prof'), ('Rev', 'Rev')], max_length=15),
        ),
        migrations.AlterField(
            model_name='profileuser',
            name='sex',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Unspecified', 'Unspecified')], max_length=15),
        ),
    ]
