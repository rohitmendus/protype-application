from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
import mimetypes, os, openpyxl, json

#UsersView
#self.get() - Renders the template and sents users' details
#self.post() - Creates new users(request sent through ajax)
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
class UsersDelete(View):
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
class UsersEdit(View):
	def get(self, request, id):
		user_obj = User.objects.get(id=id)
		profile_obj = ProfileUser.objects.get(user_id=id)
		form1 = UpdateUserForm(instance=user_obj)
		form2 = ProfileForm(instance=profile_obj)
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
		if form1.is_valid() and form2.is_valid():
			form1.save()
			form2.save()
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
class ProgrammesView(View):
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
class ProgrammesDelete(View):
	def get(self, request, id):
		programme = Programme.objects.get(id=id)
		programme.delete()
		#Sents updated data to js to render it
		data = {'programmes': RenderProgrammeData()}
		return JsonResponse(data, safe=False)

#ProgrammesEdit
#self.get() - Gets programme data to fill the modal form(request sent through ajax)
#self.post() - Updates programme data(request sent through ajax)
class ProgrammesEdit(View):
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
class DepartmentsView(View):
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
class DownloadFileUser(View):
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
			if validation.__contains__('B2'):
				toRemove.append(validation)
		for rmValidation in toRemove:
			ws.data_validations.dataValidation.remove(rmValidation)

		#Removing user names from existing template
		for x in range(2, 102):
			ws['A'+str(x)].value=""

		#Adding new drop downs
		department_names = Department.objects.values_list('name', flat=True)
		dlist1 = ", ".join(department_names)
		dlist1 = '"' + dlist1 + '"'
		dv = openpyxl.worksheet.datavalidation.DataValidation(type="list", formula1=dlist1)
		ws.add_data_validation(dv)
		dv.add('B2:B100')

		#Adding user names
		users = ProfileUser.objects.values_list('name', 'department')
		counter = 2
		for user in users:
			ws['A'+str(counter)].value = user[0]
			if user[1] != None:
				ws['B'+str(counter)].value = Department.objects.get(id=user[1]).name
			counter += 1
		wb.save(filepath)

		#Sending the file as response
		path = open(filepath, 'rb')
		mime_type, _ = mimetypes.guess_type(filepath)
		response = HttpResponse(path, content_type=mime_type)
		response['Content-Disposition'] = "attachment; filename=%s" % filename
		return response

#Uploads the user and department mapping to the db from the uploaded excel file
class UploadUserDeptView(View):
	def post(self, request):
		file = request.FILES.get('user_dept_file')

		data = []
		wb = openpyxl.load_workbook(file)
		ws = wb.active
		count = ProfileUser.objects.all().count()
		for y in range(2, count+2):
			user_name = ws['A'+str(y)].value
			department_name = ws['B'+str(y)].value
			if user_name != None and department_name != None:	
				data_set = {'user_name':user_name, 'department_name': department_name}
				data.append(data_set)
		
		print(data)
		for i in data:
			user = ProfileUser.objects.get(name=i['user_name'])
			department = Department.objects.get(name=i['department_name'])
			if user != None and department != None:
				user.department = department
				user.save()
			else:
				return HttpResponse("An error occured!")
		return redirect("/departments")

#DownloadFileProgramme
#self.get() - Downloads the excel template for uploading programmes with department
class DownloadFileProgramme(View):
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
			if validation.__contains__('B2'):
				toRemove.append(validation)
		for rmValidation in toRemove:
			ws1.data_validations.dataValidation.remove(rmValidation)

		#Removing programme names from existing template
		for x in range(2, 102):
			ws1['A'+str(x)].value=""

		#Adding new drop downs
		department_names = Department.objects.values_list('name', flat=True)
		dlist1 = ", ".join(department_names)
		dlist1 = '"' + dlist1 + '"'
		dv = openpyxl.worksheet.datavalidation.DataValidation(type="list", formula1=dlist1)
		ws1.add_data_validation(dv)
		dv.add('B2:B100')

		#Adding programme names
		programmes = Programme.objects.values_list('name', 'department')
		counter = 2
		for pgm in programmes:
			ws1['A'+str(counter)].value = pgm[0]
			if pgm[1] != None:
				ws1['B'+str(counter)].value = Department.objects.get(id=pgm[1]).name
			counter += 1
		wb1.save(filepath)

		#Sending the file as response
		path = open(filepath, 'rb')
		mime_type, _ = mimetypes.guess_type(filepath)
		response = HttpResponse(path, content_type=mime_type)
		response['Content-Disposition'] = "attachment; filename=%s" % filename
		return response

#Uploads the programme and department mapping to the db from the uploaded excel file
class UploadProgrammeDeptView(View):
	def post(self, request):
		file = request.FILES.get('pgm_dept_file')

		data = []
		wb1 = openpyxl.load_workbook(file)
		ws1 = wb1.active
		count = Programme.objects.all().count()
		for y in range(2, count+2):
			pgm_name = ws1['A'+str(y)].value
			department_name = ws1['B'+str(y)].value
			if pgm_name != None and department_name != None:	
				data_set = {'pgm_name':pgm_name, 'department_name': department_name}
				data.append(data_set)
		
		for i in data:
			pgm = Programme.objects.get(name=i['pgm_name'])
			department = Department.objects.get(name=i['department_name'])
			if pgm != None and department != None:
				pgm.department = department
				pgm.save()
			else:
				return HttpResponse("An error occured!")
		return redirect("/departments")

