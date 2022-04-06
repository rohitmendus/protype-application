// Renders the updated user data to the table
function render_user_data_to_table(response){
	$('#table-body').empty();
	var counter = 1
	for (let user of response.users){
		let element = `<tr>
			<th scope="row">${counter}</th>
			<td>${user.salutation}</td>
	        <td class="name-table">${user.name}</td>
	        <td>${user.username}</td>
	        <td>${user.email}</td>
	        <td>${user.mobile}</td>
	        <td>${user.age}</td>
	        <td>${user.sex}</td>
	        <td>${user.health}</td>
	        <td class="dept-table">${user.dept}</td>
	        <td><a href="/user-edit/" class="edit-users" data-id="${user.id}"><i class="bi bi-pencil-square"></i></a></td>
	        <td><a href="/user-delete/${user.id}" class="delete-users"><i class="bi bi-trash-fill"></i></a></td>
		</tr>`
		$('#table-body').append($(element));
		counter++;
	};
}

// Renders the updated programme data to the table
function render_programme_data_to_table(response) {
	$('#table-body-programme').empty();
	var counter = 1
	for (let programme of response.programmes){
		let element = `<tr>
	      <th scope="row">${counter}</th>
	      <td class="name-table">${programme.name}</td>
	      <td>${programme.description}</td>
	      <td class="dept-table">${programme.dept}</td>
	      <td><a class="edit-programmes" href="/programme-edit/" data-id="${programme.id}"><i class="bi bi-pencil-square"></i></a></td>
	      <td><a href="/programme-delete/${programme.id}" class="delete-programmes"><i class="bi bi-trash-fill"></i></a></td>
	    </tr>`
		$('#table-body-programme').append($(element));
		counter++;
	};
}

$(document).ready(function(){
	// Fetches values of the user and sends the data to the db
	// On success renders the updated data
	$('#add-users-form').submit(function(e){
		e.preventDefault()
		const url = $(this).attr('action');
		const csrf_token = $('#add-users-form input[name="csrfmiddlewaretoken"]').val();
		const username = $('#username').val();
		const name = $('#name').val();
		const email = $('#email').val();
		const mobile = $('#mobile').val();
		const age = $('#age').val();
		const sex = $('#sex').val();
		const salutation = $('#salutation').val();
		const health = $('#health').val();
		const password1 = $('#password1').val();
		const password2 = $('#password2').val();
		const dept = $('#dept').val()
		// if (!(Number.isInteger(Number(mobile)) && mobile.length == 10)) {
		// 	alert("Mobile number is not valid!");
		// } else if (!(Number.isInteger(Number(age)) && Number(age) > 0)) {
		// 	alert("Age is not valid!")
		// } else if (password1 !== password2) {
		// 	alert("Passwords don't match!")
		// } else {
		var form1 = new FormData();
		form1.append('username', username);
		form1.append('email', email);
		form1.append('password1', password1);
		form1.append('password2', password2);
		var form2 = new FormData();
		form2.append('name', name);
		form2.append('mobile', mobile);
		form2.append('age', age);
		form2.append('sex', sex);
		form2.append('salutation', salutation);
		form2.append('health', health);
		form2.append('department', dept);
		data = {'form1': form1, 'form2': form2, 'csrfmiddlewaretoken': csrf_token}
		$.ajax({
			url: url,
			type: 'post',
			data: data,
			processData: false,
			success: function(response){
				alert("User has been saved successfully!");
				$('#add-users-form').trigger("reset");
				render_user_data_to_table(response);
			}
		});
	});

	// Event is triggered when the delete btn is clicked
	// Sends a get request to django to delete the user
	$(document).on('click', '.delete-users', function(e){
		e.preventDefault()
		if (confirm("Are you sure you want to delete this user?")) {
			const url = $(this).attr('href')
			$.ajax({
				url: url,
				type: 'get',
				success: function(response){
					alert("User has been deleted");
					render_user_data_to_table(response);
				}
			});
		};
	});

	// Event is triggered on click of the edit btn
	// A get request is sent to fetch the user's data
	// Opens a modal form for editing the users with the existing user data
	$(document).on('click', '.edit-users', function(e){
		e.preventDefault()
		const url = $(this).attr('href');
		const id = $(this).data('id');
		$.ajax({
			url: url,
			data: {'id': id},
			type: 'get',
			success: function(response){
				$('#edit-user-modal').modal('show');
				$('#edit-user-form').attr('action', url);
				$('#edit-user-form input[name="edit-id"]').val(response.id);
				$('#edit-user-form input[id="username-edit"]').val(response.username);
				$('#edit-user-form input[id="name-edit"]').val(response.name);
				$('#edit-user-form input[id="email-edit"]').val(response.email);
				$('#edit-user-form input[id="mobile-edit"]').val(response.mobile);
				$('#edit-user-form select[id="health-edit"]').val(response.health);
				$('#edit-user-form input[id="age-edit"]').val(response.age);
				$('#edit-user-form select[id="sex-edit"]').val(response.sex);
				$('#edit-user-form select[id="salutation-edit"]').val(response.salutation);
				$('#edit-user-form select[id="dept-edit"]').empty();
				for (let i of response.depts){
					let elem = `<option value="${i}">${i}</option>`;
					$('#edit-user-form select[id="dept-edit"]').append($(elem));
				}
				if (response.dept!=""){
					$('#edit-user-form select[id="dept-edit"]').val(response.dept);
				}
			}
		});
	});

	// Fetches data from the user edit form and sends the updated data to db for updating
	// On success renders the updated data to the table
	$('#edit-user-form').submit(function(e) {
		e.preventDefault()
		const url = $(this).attr('action');
		const id = $('#edit-user-form input[name="edit-id"]').val();
		const csrf_token = $('#edit-user-form input[name="csrfmiddlewaretoken"]').val();
		const username = $('#username-edit').val();
		const name = $('#name-edit').val();
		const email = $('#email-edit').val();
		const mobile = $('#mobile-edit').val();
		const age = $('#age-edit').val();
		const sex = $('#sex-edit').val();
		const salutation = $('#salutation-edit').val();
		const health = $('#health-edit').val();
		const dept = $('#dept-edit').val();
		if (!(Number.isInteger(Number(mobile)) && mobile.length == 10)) {
			alert("Mobile number is not valid!");
		} else if (!(Number.isInteger(Number(age)) && Number(age) > 0)) {
			alert("Age is not valid!")
		} else {
			$.ajax({
				url: url,
				type: 'post',
				data: {'csrfmiddlewaretoken': csrf_token, 'username': username, 'name': name,
					'email': email, 'mobile': mobile, 'age': age, 'sex': sex, 'salutation': salutation,
					'health': health, 'id': id, 'dept': dept},
				success: function(response){
					alert("Changes have been saved!");
					$('#edit-user-form').trigger("reset");
					$('#edit-user-modal').modal('hide');
					render_user_data_to_table(response);
				}
			});
		}
	});

	// Event is triggered when we type in search 
	// According to the value change renders the appropriate results according to the user's name
	$('#search').keyup(function() {
		var search_name = $(this).val().toLowerCase();
		$('#table-body .name-table').each(function(){
			let name = $(this).text().toLowerCase();
			if (!(name.includes(search_name))) {
				$(this).parent().hide();
			} else {
				$(this).parent().show();
			}
		});
	});

	// Fetches values of the programme and sends the data to the db
	// On success renders the updated data
	$('#add-programmes-form').submit(function(e){
		e.preventDefault()
		const url = $(this).attr('action');
		const csrf_token = $('#add-programmes-form input[name="csrfmiddlewaretoken"]').val();
		const name = $('#name').val();
		const description = $('#description').val();
		$.ajax({
			url: url,
			type: 'post',
			data: {'csrfmiddlewaretoken': csrf_token, 'name': name, 'description': description},
			success: function(response){
				alert("Programme has been saved successfully!");
				$('#add-programmes-form').trigger("reset");
				render_programme_data_to_table(response);
			}
		});
	});

	// Event is triggered when the delete btn is clicked
	// Sends a get request to django to delete the programme
	$(document).on('click', '.delete-programmes', function(e){
		e.preventDefault()
		if (confirm("Are you sure you want to delete this programme?")) {
			const url = $(this).attr('href')
			$.ajax({
				url: url,
				type: 'get',
				success: function(response){
					alert("Programme has been deleted");
					render_programme_data_to_table(response);
				}
			});
		};
	});

	// Event is triggered on click of the edit btn
	// A get request is sent to fetch the programme's data
	// Opens a modal form for editing the programmes with the existing user data
	$(document).on('click', '.edit-programmes', function(e){
		e.preventDefault()
		const url = $(this).attr('href');
		const id = $(this).data('id');
		$.ajax({
			url: url,
			data: {'id': id},
			type: 'get',
			success: function(response){
				$('#edit-programme-modal').modal('show');
				$('#edit-programme-form').attr('action', url);
				$('#edit-programme-form input[name="edit-programme-id"]').val(response.id);
				$('#edit-programme-form textarea[id="description-edit"]').text(response.description);
				$('#edit-programme-form input[id="name-edit"]').val(response.name);
				$('#edit-programme-form select[id="dept-edit"]').empty();
				for (let i of response.depts){
					let elem = `<option value="${i}">${i}</option>`;
					$('#edit-programme-form select[id="dept-edit"]').append($(elem));
				}
				if (response.dept!=""){
					$('#edit-programme-form select[id="dept-edit"]').val(response.dept);
				}
			}
		});
	});

	// Fetches data from the programme edit form and sends the updated data to db for updating
	// On success renders the updated data to the table
	$('#edit-programme-form').submit(function(e) {
		e.preventDefault()
		const url = $(this).attr('action');
		const id = $('#edit-programme-form input[name="edit-programme-id"]').val();
		const csrf_token = $('#edit-programme-form input[name="csrfmiddlewaretoken"]').val();
		const name = $('#name-edit').val();
		const description = $('#description-edit').val();
		const dept = $('#dept-edit').val();
		$.ajax({
			url: url,
			type: 'post',
			data: {'csrfmiddlewaretoken': csrf_token, 'name': name, 
				'description': description, 'id': id, 'dept': dept},
			success: function(response){
				alert("Changes have been saved!");
				$('#edit-programme-form').trigger("reset");
				$('#edit-programme-modal').modal('hide');
				render_programme_data_to_table(response);
			}
		});
	});

	// Event is triggered when we type in search 
	// According to the value change renders the appropriate results according to the programme's name
	$('#search-programme').keyup(function() {
		var search_name = $(this).val().toLowerCase();
		$('#table-body-programme .name-table').each(function(){
			let name = $(this).text().toLowerCase();
			if (!(name.includes(search_name))) {
				$(this).parent().hide();
			} else {
				$(this).parent().show();
			}
		});
	});

	// Event is triggered when there is change in value of dept-filter
	// Renders data accoriding to the user's or programme's department
	$('#dept-filter').change(function(){
		const dept = $(this).val();
		if (dept === "Select All"){
			$('table tbody tr').each(function(){
				$(this).show();
			});
		} else {
			$('table tbody .dept-table').each(function(){
				let name = $(this).text()
				if (name !== dept) {
					$(this).parent().hide();
				} else {
					$(this).parent().show();
				}
			});
		}
	});

	// Fetches values of the department and sends the data to the db
	$('#add-departments-form').submit(function(e){
		e.preventDefault()
		const url = $(this).attr('action');
		const csrf_token = $('#add-departments-form input[name="csrfmiddlewaretoken"]').val();
		const name = $('#name').val();
		const description = $('#description').val();
		$.ajax({
			url: url,
			type: 'post',
			data: {'csrfmiddlewaretoken': csrf_token, 'name': name, 'description': description},
			success: function(response){
				alert(response);
				$('#add-departments-form').trigger('reset');
			}
		});
	});
});