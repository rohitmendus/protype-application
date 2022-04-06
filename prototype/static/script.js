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
	        <td><a href="/user-edit/${user.id}" class="edit-users"><i class="bi bi-pencil-square"></i></a></td>
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
		data = $(this).serialize();
		$.ajax({
			url: url,
			type: 'post',
			data: data,
			success: function(response){
				$('#messageLabel').empty();
				$('#message-modal .modal-body').empty();
				if (response.success) {
					$('#messageLabel').text('Success!');
					$('#message-modal .modal-body').text("User has been saved successfully!");
					$('#add-users-form').trigger("reset");
					render_user_data_to_table(response);
				} else {
					$('#messageLabel').text('Error!');
					for (let error in response.errors){
						message = '<p>' + response.errors[error][0]['message'] + '</p>'
						$('#message-modal .modal-body').append($(message));
					}
				}
				$('#message-modal').modal('show');
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
					$('#messageLabel').empty();
					$('#message-modal .modal-body').empty();
					$('#messageLabel').text('Success!');
					$('#message-modal .modal-body').text("User has been deleted successfully!");
					$('#message-modal').modal('show');
					render_user_data_to_table(response);
				},
				error: function(){
					$('#messageLabel').empty();
					$('#message-modal .modal-body').empty();
					$('#messageLabel').text('Error!');
					$('#message-modal .modal-body').text("An error occured please try again later!");
					$('#message-modal').modal('show');
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
		$.ajax({
			url: url,
			type: 'get',
			success: function(response){
				$('#edit-user-modal').modal('show');
				$('#edit-user-form').attr('action', url);
				$('#edit-user-modal .modal-body').empty();
				$('#edit-user-modal .modal-body').append(response);
			}
		});
	});

	// Fetches data from the user edit form and sends the updated data to db for updating
	// On success renders the updated data to the table
	$('#edit-user-form').submit(function(e) {
		e.preventDefault()
		const url = $(this).attr('action');
		data = $(this).serialize();
		$.ajax({
			url: url,
			type: 'post',
			data: data,
			success: function(response){
				$('#messageLabel').empty();
				$('#message-modal .modal-body').empty();
				if (response.success) {
					$('#messageLabel').text('Success!');
					$('#message-modal .modal-body').text("User has been updated successfully!");
					render_user_data_to_table(response);
				} else {
					$('#messageLabel').text('Error!');
					for (let error in response.errors){
						message = '<p>' + response.errors[error][0]['message'] + '</p>'
						$('#message-modal .modal-body').append($(message));
					}
				}
				$('#edit-user-modal .modal-body').empty();
				$('#edit-user-modal').modal('hide');
				$('#message-modal').modal('show');
			}
		});
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
		const data = $(this).serialize()
		$.ajax({
			url: url,
			type: 'post',
			data: data,
			success: function(response){
				$('#messageLabel').empty();
				$('#message-modal .modal-body').empty();
				if (response.success) {
					$('#messageLabel').text('Success!');
					$('#message-modal .modal-body').text("Programme has been saved successfully!");
					$('#add-users-form').trigger("reset");
					render_programme_data_to_table(response);
				} else {
					$('#messageLabel').text('Error!');
					for (let error in response.errors){
						message = '<p>' + response.errors[error][0]['message'] + '</p>'
						$('#message-modal .modal-body').append($(message));
					}
				}
				$('#message-modal').modal('show');
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
					$('#messageLabel').empty();
					$('#message-modal .modal-body').empty();
					$('#messageLabel').text('Success!');
					$('#message-modal .modal-body').text("Programme has been deleted successfully!");
					$('#message-modal').modal('show');
					render_programme_data_to_table(response);
				},
				error: function(){
					$('#messageLabel').empty();
					$('#message-modal .modal-body').empty();
					$('#messageLabel').text('Error!');
					$('#message-modal .modal-body').text("An error occured please try again later!");
					$('#message-modal').modal('show');
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
		$.ajax({
			url: url,
			type: 'get',
			success: function(response){
				$('#edit-programme-modal').modal('show');
				$('#edit-programme-form').attr('action', url);
				$('#edit-user-modal .modal-body').empty();
				$('#edit-programme-modal .modal-body').append(response);
			}
		});
	});

	// Fetches data from the programme edit form and sends the updated data to db for updating
	// On success renders the updated data to the table
	$('#edit-programme-form').submit(function(e) {
		e.preventDefault()
		const url = $(this).attr('action');
		const data = $(this).serialize()
		$.ajax({
			url: url,
			type: 'post',
			data: data,
			success: function(response){
				$('#messageLabel').empty();
				$('#message-modal .modal-body').empty();
				if (response.success) {
					$('#messageLabel').text('Success!');
					$('#message-modal .modal-body').text("Programme has been updated successfully!");
					render_programme_data_to_table(response);
				} else {
					$('#messageLabel').text('Error!');
					for (let error in response.errors){
						message = '<p>' + response.errors[error][0]['message'] + '</p>'
						$('#message-modal .modal-body').append($(message));
					}
				}
				$('#edit-programme-modal .modal-body').empty();
				$('#edit-programme-modal').modal('hide');
				$('#message-modal').modal('show');
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
		const data = $(this).serialize();
		$.ajax({
			url: url,
			type: 'post',
			data: data,
			success: function(response){
				$('#messageLabel').empty();
				$('#message-modal .modal-body').empty();
				if (response.success) {
					$('#messageLabel').text('Success!');
					$('#message-modal .modal-body').text("Department has been saved successfully!");
					$('#add-departments-form').trigger('reset');
				} else {
					$('#messageLabel').text('Error!');
					for (let error in response.errors){
						message = '<p>' + response.errors[error][0]['message'] + '</p>'
						$('#message-modal .modal-body').append($(message));
					}
				}
				$('#message-modal').modal('show');
			}
		});
	});
});