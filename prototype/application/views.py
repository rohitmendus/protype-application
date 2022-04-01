from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import *
from django.contrib.auth.models import User

# Create your views here.
class UsersView(View):
	template = 'users.html'
	def get(self, request):
		users_obj = ProfileUser.objects.all()
		users = []
		for i in users_obj:
			if i.health:
				health="Fine"
			else:
				health="Not fine"
			user_obj = User.objects.get(id=i.user_id)
			user = {'username': user_obj.username, 'name': i.name, 'email': user_obj.email,
				'mobile': i.mobile, 'age': i.age, 'sex': i.sex, 'salutation': i.salutation,
				'health': health, 'id': user_obj.id}
			users.append(user)
		context = {'users': users}
		return render(request, self.template, context)

	def post(self, request):
		username = request.POST.get('username')
		name = request.POST.get('name')
		email = request.POST.get('email')
		mobile = request.POST.get('mobile')
		age = request.POST.get('age')
		sex = request.POST.get('sex')
		salutation = request.POST.get('salutation')
		if request.POST.get('health') == "True":
			health = True
		else:
			health = False
		password1 = request.POST.get('password1')
		user = User.objects.create_user(username=username, email=email, password=password1)
		user.save()	
		user_profile = ProfileUser(user=user, name=name, mobile=mobile, age=int(age), sex=sex, salutation=salutation, health=health)
		user_profile.save()


		users_obj = ProfileUser.objects.all()
		users = []
		for i in users_obj:
			if i.health:
				health="Fine"
			else:
				health="Not fine"
			user_obj = User.objects.get(id=i.user_id)
			user_1 = {'username': user_obj.username, 'name': i.name, 'email': user_obj.email,
				'mobile': i.mobile, 'age': i.age, 'sex': i.sex, 'salutation': i.salutation,
				'health': health, 'id': user_obj.id}
			users.append(user_1)
		data = {'users': users}
		return JsonResponse(data)

class UsersDelete(View):
	def get(self, request, id):
		user = User.objects.get(id=id)
		user.delete()

		users_obj = ProfileUser.objects.all()
		users = []
		for i in users_obj:
			if i.health:
				health="Fine"
			else:
				health="Not fine"
			user_obj = User.objects.get(id=i.user_id)
			user_1 = {'username': user_obj.username, 'name': i.name, 'email': user_obj.email,
				'mobile': i.mobile, 'age': i.age, 'sex': i.sex, 'salutation': i.salutation,
				'health': health, 'id': user_obj.id}
			users.append(user_1)
		data = {'users': users}
		return JsonResponse(data)

class UsersEdit(View):
	def get(self, request):
		id_1 = request.GET.get('id')
		user_obj = User.objects.get(id=id_1)
		profile_obj = ProfileUser.objects.get(user_id=id_1)
		data = {'username': user_obj.username, 'name': profile_obj.name, 'email': user_obj.email,
				'mobile': profile_obj.mobile, 'age': profile_obj.age, 'sex': profile_obj.sex, 'salutation': profile_obj.salutation,
				'health': str(profile_obj.health), 'id': user_obj.id}
		return JsonResponse(data)

	def post(self, request):
		id_1 = request.POST.get('id')
		username = request.POST.get('username')
		name = request.POST.get('name')
		email = request.POST.get('email')
		mobile = request.POST.get('mobile')
		age = request.POST.get('age')
		sex = request.POST.get('sex')
		salutation = request.POST.get('salutation')
		if request.POST.get('health') == "True":
			health = True
		else:
			health = False

		user_obj = User.objects.get(id=id_1)
		user_obj.username = username
		user_obj.email = email

		profile_obj = ProfileUser.objects.get(user_id=id_1)
		profile_obj.mobile = mobile
		profile_obj.age = int(age)
		profile_obj.sex = sex
		profile_obj.salutation = salutation
		profile_obj.health = health
		profile_obj.name = name

		user_obj.save()
		profile_obj.save()

		users_obj = ProfileUser.objects.all()
		users = []
		for i in users_obj:
			if i.health:
				health="Fine"
			else:
				health="Not fine"
			user_obj_1 = User.objects.get(id=i.user_id)
			user_1 = {'username': user_obj_1.username, 'name': i.name, 'email': user_obj_1.email,
				'mobile': i.mobile, 'age': i.age, 'sex': i.sex, 'salutation': i.salutation,
				'health': health, 'id': user_obj_1.id}
			users.append(user_1)
		data = {'users': users}
		return JsonResponse(data)