# Generated by Django 4.0.3 on 2022-04-08 09:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application', '0007_userrole'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrole',
            name='description',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='userrole',
            name='user',
            field=models.ManyToManyField(blank=True, null=True, related_name='roles', to=settings.AUTH_USER_MODEL),
        ),
    ]
