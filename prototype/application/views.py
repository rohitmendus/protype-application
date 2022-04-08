from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth import password_validation
from django.core.validators import validate_email, RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.views import View
from .models import *
from .forms import *
from .mixins import AdminRequiredMixin
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
import mimetypes, os, openpyxl, json

#Admin User
#username: admin
#password: 12345
class LoginView(View):
	template = "login.html"
	def get(self, request):
		form = AuthenticationForm()
		return render(request, self.template, {'form': form})

	def post(self, request):
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			user = form.get_user()
			if user.roles.filter(role='Admin').exists():
				login(request, user)
				return redirect('/users')
			else:
				messages.error(request, 'User is not an admin!')
				return redirect('/login')
		else:
			messages.error(request, 'Incorrect username or password!.')
			return redirect('/login')

class LogOutView(View):
	def get(self, request):
		logout(request)
		return redirect("/login")

#UsersView
#self.get() - Renders the template and sents users' details
#self.post() - Creates new users(request sent through ajax)
class UsersView(AdminRequiredMixin, View):
	login_url = "/login/"
	template = 'users.html'
	def get(self, request):
		users_obj = ProfileUser.objects.all()
		users = []
		for i in users_obj:
			if i.health:
				health="Fine"
			else:
				health="Not fine"
			if i.department == None:
				dept = ""
			else:
				dept = i.department.name
			user_obj = User.objects.get(id=i.user_id)
			user = {'username': user_obj.username, 'name': i.name, 'email': user_obj.email,
				'mobile': i.mobile, 'age': i.age, 'sex': i.sex, 'salutation': i.salutation,
				'health': health, 'id': user_obj.id, 'dept': dept}
			users.append(user)
		form2 = ProfileForm()
		form1 = CreateUserForm()
		print(request.user.roles.filter(role="Admin").exists())
		context = {'users': users, 'depts': Department.objects.values_list('name', flat=True),
			'form1': form1, 'form2': form2}
		return render(request, self.template, context)

	def post(self, request):
		form1 = CreateUserForm(request.POST)
		form2 = ProfileForm(request.POST)
		if form1.is_valid() and form2.is_valid():
			user = form1.save()
			profile = form2.save(commit=False)
			profile.user = user
			profile.save()
		else:
			errors = {**json.loads(form1.errors.as_json()), **json.loads(form2.errors.as_json())}
			data = {'errors': errors, 'success': False}
			return JsonResponse(data)

		#Sents updated data to js to render it
		users_obj = ProfileUser.objects.all()
		users = []
		for i in users_obj:
			if i.health:
				health="Fine"
			else:
				health="Not fine"
			if i.department == None:
				dept = ""
			else:
				dept = i.department.name
			user_obj_1 = User.objects.get(id=i.user_id)
			user_1 = {'username': user_obj_1.username, 'name': i.name, 'email': user_obj_1.email,
				'mobile': i.mobile, 'age': i.age, 'sex': i.sex, 'salutation': i.salutation,
				'health': health, 'id': user_obj_1.id, 'dept': dept}
			users.append(user_1)
		data = {'users': users, 'success': True}
		return JsonResponse(data)

#UsersDelete
#self.get() - Deletes the user(request sent through ajax)
class UsersDelete(AdminRequiredMixin, View):
	login_url = "/login/"
	def get(self, request, id):
		#Deleting user
		user = User.objects.get(id=id)
		user.delete()
		#Sents updated data to js to render it
		users_obj = ProfileUser.objects.all()
		users = []
		for i in users_obj:
			if i.health:
				health="Fine"
			else:
				health="Not fine"
			if i.department == None:
				dept = ""
			else:
				dept = i.department.name
			user_obj = User.objects.get(id=i.user_id)
			user_1 = {'username': user_obj.username, 'name': i.name, 'email': user_obj.email,
				'mobile': i.mobile, 'age': i.age, 'sex': i.sex, 'salutation': i.salutation,
				'health': health, 'id': user_obj.id, 'dept': dept}
			users.append(user_1)
		data = {'users': users}
		return JsonResponse(data)

#UsersEdit
#self.get() - Gets user data to fill the modal form(request sent through ajax)
#self.post() - Updates user data(request sent through ajax)
class UsersEdit(AdminRequiredMixin, View):
	login_url = "/login/"
	def get(self, request, id):
		user_obj = User.objects.get(id=id)
		profile_obj = ProfileUser.objects.get(user_id=id)
		form1 = UpdateUserForm(instance=user_obj)
		form2 = ProfileForm(instance=profile_obj)
		user_roles = UserRole.objects.values_list('role', flat=True)
		user_roles_opts = ''
		for user_role in user_roles:
			if user_obj.roles.filter(role=user_role).exists():
				elem = f'<option value="{user_role}" selected>{user_role}</option>'
			else:
				elem = f'<option value="{user_role}">{user_role}</option>'
			user_roles_opts += elem
		data = f'''
			<div class="mb-3 col-6">
				<label for="username-edit" class="form-label">Username</label>
				{form1['username']}
			</div>
			<div class="mb-3 col-6">
				<label for="name-edit" class="form-label">Name</label>
				{form2['name']}
			</div>
			<div class="mb-3 col-6">
				<label for="email-edit" class="form-label">Email address</label>
				{form1['email']}
			</div>
			<div class="mb-3 col-6">
				<label for="mobile-edit" class="form-label">Mobile</label>
				{form2['mobile']}
			</div>
			<div class="mb-3 col-6">
				<label for="age-edit" class="form-label">Age</label>
				{form2['age']}
			</div>
			<div class="mb-3 col-6">
				<label for="sex-edit" class="form-label">Sex</label>
				{form2['sex']}
			</div>
			<div class="mb-3 col-12">
				<label for="salutation-edit" class="form-label">Salutation</label>
				{form2['salutation']}
			</div>
			<div class="mb-3 col-12">
				<label for="dept-edit" class="form-label">Department</label>
				{form2['department']}
			</div>
			<div class="mb-3 col-12">
				<label for="user-roles" class="form-label">User Role</label>
				<select name="user-roles" class="form-select" id="user-roles" multiple>
					{user_roles_opts}
				</select>
			</div>
			<div class="mb-3 col-6">
				{form2['health']}
				<label for="health-edit" class="form-check-label">Health</label>
			</div>
		'''

		return JsonResponse(data, safe=False)

	def post(self, request, id):
		user_obj = User.objects.get(id=id)
		profile_obj = ProfileUser.objects.get(user_id=id)
		form1 = UpdateUserForm(request.POST, instance=user_obj)
		form2 = ProfileForm(request.POST, instance=profile_obj)
		roles = request.POST.getlist('user-roles')
		if form1.is_valid() and form2.is_valid():
			form1.save()
			form2.save()
			for role_name in roles:
				role = UserRole.objects.get(role=role_name)
				role.users.add(user_obj)
		else:
			errors = {**json.loads(form1.errors.as_json()), **json.loads(form2.errors.as_json())}
			data = {'errors': errors, 'success': False}
			return JsonResponse(data)

		#Sents updated data to js to render it
		users_obj = ProfileUser.objects.all()
		users = []
		for i in users_obj:
			if i.health:
				health="Fine"
			else:
				health="Not fine"
			if i.department == None:
				dept = ""
			else:
				dept = i.department.name
			user_obj_1 = User.objects.get(id=i.user_id)
			user_1 = {'username': user_obj_1.username, 'name': i.name, 'email': user_obj_1.email,
				'mobile': i.mobile, 'age': i.age, 'sex': i.sex, 'salutation': i.salutation,
				'health': health, 'id': user_obj_1.id, 'dept': dept}
			users.append(user_1)
		data = {'users': users, 'success': True}
		return JsonResponse(data)

#Renders programme data
def RenderProgrammeData():
	pgms = []
	for pgm in Programme.objects.all():
		if pgm.department == None:
			dept = ""
		else:
			dept = pgm.department.name
		pgm_obj = {'id': pgm.id, 'name': pgm.name, 'description': pgm.description, 'dept': dept}
		pgms.append(pgm_obj)
	return pgms

#ProgrammesView
#self.get() - Renders the template and sents programmes' details
#self.post() - Creates new programmes(request sent through ajax)
class ProgrammesView(AdminRequiredMixin, View):
	login_url = "/login/"
	template = 'programmes.html'
	def get(self, request):
		form = ProgrammeForm()
		context = {'programmes': RenderProgrammeData(), 'depts': Department.objects.values_list('name', flat=True),
			'form': form}
		return render(request, self.template, context)

	def post(self, request):
		form = ProgrammeForm(request.POST)
		if form.is_valid():
			form.save()
		else:
			data = {'errors': form.errors.as_json(), 'success': False}
			return JsonResponse(data)
		#Sents updated data to js to render it
		data = {'programmes': RenderProgrammeData(), 'success': True}
		return JsonResponse(data, safe=False)

#ProgrammesDelete
#self.get() - Deletes the programme(request sent through ajax)
class ProgrammesDelete(AdminRequiredMixin, View):
	login_url = "/login/"
	def get(self, request, id):
		programme = Programme.objects.get(id=id)
		programme.delete()
		#Sents updated data to js to render it
		data = {'programmes': RenderProgrammeData()}
		return JsonResponse(data, safe=False)

#ProgrammesEdit
#self.get() - Gets programme data to fill the modal form(request sent through ajax)
#self.post() - Updates programme data(request sent through ajax)
class ProgrammesEdit(AdminRequiredMixin, View):
	login_url = "/login/"
	def get(self, request, id):
		pgm_obj = Programme.objects.get(id=id)
		form = ProgrammeForm(instance=pgm_obj)
		data = f'''
			<div class="mb-3 col-12">
			  <label for="name" class="form-label">Programme Name</label>
			  {form["name"]}
			</div>
			<div class="mb-3 col-12">
				<label for="dept-edit" class="form-label">Department</label>
				{form["department"]}
			</div>
			<div class="form-group mb-3">
			  <label for="description">Description</label>
			  {form["description"]}
			</div>
		'''
		return JsonResponse(data, safe=False)

	def post(self, request, id):
		pgm_obj = Programme.objects.get(id=id)
		form = ProgrammeForm(request.POST, instance=pgm_obj)
		if form.is_valid():
			form.save()
		else:
			data = {'errors': form.errors.as_json(), 'success': False}
			return JsonResponse(data)
		#Sents updated data to js to render it
		data = {'programmes': RenderProgrammeData(), 'success':True}
		return JsonResponse(data, safe=False)


#DepartmentsView
#self.get() - Renders the template
#self.post() - Creates new department(request sent through ajax)
class DepartmentsView(AdminRequiredMixin, View):
	login_url = "/login/"
	template = 'departments.html'
	def get(self, request):
		form = DepartmentForm()
		return render(request, self.template, {'form':form})

	def post(self, request):
		form = DepartmentForm(request.POST)
		if form.is_valid():
			form.save()
		else:
			data = {'errors': form.errors.as_json(), 'success': False}
			return JsonResponse(data)

		return JsonResponse({'success':True})

#DownloadFileUser
#self.get() - Downloads the excel template for uploading users with department
class DownloadFileUser(AdminRequiredMixin, View):
	login_url = "/login/"
	def get(self, request):
		# Getting file path
		filename= "user_department_template.xlsx"
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		filepath = BASE_DIR + '/templates/' + filename

		# Loading the excel file
		wb = openpyxl.load_workbook(filepath)
		ws = wb.active

		#Removing existing data downs if any
		toRemove = []
		for validation in ws.data_validations.dataValidation:
			if validation.__contains__('K2'):
				toRemove.append(validation)
		for rmValidation in toRemove:
			ws.data_validations.dataValidation.remove(rmValidation)

		#Adding new drop downs
		department_names = Department.objects.values_list('name', flat=True)
		dlist1 = ", ".join(department_names)
		dlist1 = '"' + dlist1 + '"'
		dv_dept = openpyxl.worksheet.datavalidation.DataValidation(type="list", formula1=dlist1, allow_blank=True)
		dv_sex = openpyxl.worksheet.datavalidation.DataValidation(type="list", formula1='"Male,Female,Unspecified"')
		dv_salutation = openpyxl.worksheet.datavalidation.DataValidation(type="list", formula1='"Dr,Mr,Ms,Prof,Rev"')
		dv_health = openpyxl.worksheet.datavalidation.DataValidation(type="list", formula1='"Fine,Not Fine"')
		ws.add_data_validation(dv_dept)
		dv_dept.add('K2:K100')
		ws.add_data_validation(dv_sex)
		dv_sex.add('F2:F100')
		ws.add_data_validation(dv_salutation)
		dv_salutation.add('G2:G100')
		ws.add_data_validation(dv_health)
		dv_health.add('H2:H100')

		wb.save(filepath)

		#Sending the file as response
		path = open(filepath, 'rb')
		mime_type, _ = mimetypes.guess_type(filepath)
		response = HttpResponse(path, content_type=mime_type)
		response['Content-Disposition'] = "attachment; filename=%s" % filename
		return response

#Uploads the user and department mapping to the db from the uploaded excel file
class UploadUserDeptView(AdminRequiredMixin, View):
	login_url = "/login/"
	def post(self, request):
		file = request.FILES.get('user_dept_file')

		errors= []
		wb = openpyxl.load_workbook(file)
		ws = wb.active
		for x in range(2, 101):
			username = ws['A'+str(x)].value
			name = ws['B'+str(x)].value
			email = ws['C'+str(x)].value
			mobile = ws['D'+str(x)].value
			age = ws['E'+str(x)].value
			sex = ws['F'+str(x)].value
			salutation = ws['G'+str(x)].value
			dept_name = ws['K'+str(x)].value
			if ws['H'+str(x)].value == "Fine":
				health = True
			else:
				health = False
			password1 = str(ws['I'+str(x)].value)
			password2 = str(ws['J'+str(x)].value)
			error = []
			if None not in [username, name, email, mobile, age, sex, salutation, health, password1, password2]:
				if '' in [username, name, email, mobile, age, sex, salutation, health, password1, password2]:
					error.append('Some fields are empty')
				if password1 != password2:
					error.append('Passwords are not matching!')
				try:
					validate_email(email)
				except ValidationError as e:
					error.append("Email is not valid!")
				try:
					password_validation.validate_password(password1)
				except ValidationError as e:
					error.append('Password is not valid!')
				try:
					validator = RegexValidator(regex = r"^\+?1?\d{8,15}$")
					validator(mobile)
				except ValidationError as e:
					error.append('Phone number is not valid!')
				if ProfileUser.objects.filter(mobile=mobile).exists():
					error.append('The phone number you entered has already been registered!')
				if str(age).isnumeric() == False:
					error.append('The age is not valid!')
				if len(error) == 0:
					try:
						dept = Department.objects.get(name=dept_name)
					except:
						dept = None
					user = User.objects.create_user(username=username, email=email, password=password1)
					if dept != None:
						profile = ProfileUser.objects.create(name=name,mobile=mobile,age=age,
						sex=sex,salutation=salutation,health=health,department=dept, user=user)
					else:
						profile = ProfileUser.objects.create(name=name,mobile=mobile,age=age,
						sex=sex,salutation=salutation,health=health, user=user)
				else:
					errors.append(error)
		print(errors)
		return redirect("/departments")

#DownloadFileProgramme
#self.get() - Downloads the excel template for uploading programmes with department
class DownloadFileProgramme(AdminRequiredMixin, View):
	login_url = "/login/"
	def get(self, request):
		# Getting file path
		filename= "programme_dept_template.xlsx"
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		filepath = BASE_DIR + '/templates/' + filename

		# Loading the excel file
		wb1 = openpyxl.load_workbook(filepath)
		ws1 = wb1.active

		#Removing existing data downs if any
		toRemove = []
		for validation in ws1.data_validations.dataValidation:
			if validation.__contains__('C2'):
				toRemove.append(validation)
		for rmValidation in toRemove:
			ws1.data_validations.dataValidation.remove(rmValidation)

		#Adding new drop downs
		department_names = Department.objects.values_list('name', flat=True)
		dlist1 = ", ".join(department_names)
		dlist1 = '"' + dlist1 + '"'
		dv = openpyxl.worksheet.datavalidation.DataValidation(type="list", formula1=dlist1, allow_blank=True)
		ws1.add_data_validation(dv)
		dv.add('C2:C100')
		wb1.save(filepath)

		#Sending the file as response
		path = open(filepath, 'rb')
		mime_type, _ = mimetypes.guess_type(filepath)
		response = HttpResponse(path, content_type=mime_type)
		response['Content-Disposition'] = "attachment; filename=%s" % filename
		return response

#Uploads the programme and department mapping to the db from the uploaded excel file
class UploadProgrammeDeptView(AdminRequiredMixin, View):
	login_url = "/login/"
	def post(self, request):
		file = request.FILES.get('pgm_dept_file')

		errors = []
		wb1 = openpyxl.load_workbook(file)
		ws1 = wb1.active
		for x in range(2, 101):
			error = []
			name = ws1['A'+str(x)].value
			description = ws1['B'+str(x)].value
			dept_name = ws1['C'+str(x)].value
			if None not in [name, description]:
				if len(description) > 500:
					error.append('Max length has exceeded for description')
				if len(name) > 200:
					error.append('Max length has exceeded for programme name')
				if len(error) == 0:
					try:
						dept = Department.objects.get(name=dept_name)
					except:
						dept = None
					if dept != None:
						pgm = Programme.objects.create(name=name, description=description, department=dept)
					else:
						pgm = Programme.objects.create(name=name, description=description)
				else:
					errors.append(error)
		print(errors)
		return redirect("/departments")

