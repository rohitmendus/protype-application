from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.
class Department(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=500)


class ProfileUser(models.Model):
	phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")
	sex_type = (
		(1, "Male"),
		(2, "Female"),
		(3, "Unspecified"),
	)
	salutations = (
		(1, "Dr"),
		(2, "Mr"),
		(3, "Ms"),
		(4, "Prof"),
		(5, "Rev"),
	)
	status_type = (
		(1, "Active"),
		(2, "Inactive"),
		(3, "Disabled"),
		(4, "Null"),
		(5, "Null"),
	)   

	name = models.CharField(max_length=200)
	mobile = models.CharField(validators = [phoneNumberRegex], max_length=10, unique = True)
	age = models.IntegerField()
	sex = models.CharField(choices=sex_type, max_length=15)
	salutation = models.CharField(choices=salutations, max_length=15)
	health = models.BooleanField(default=True)
	status = models.IntegerField(choices=status_type, default=1)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="users", blank=True, null=True)

class Programme(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=500)
	department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="programmes", blank=True, null=True)


