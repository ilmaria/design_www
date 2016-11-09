$('#user-search').typeahead({
  source: searchUsers,
  afterSelect: addToSelectedUsers
})

function searchUsers(query, process) {
  $.ajax({
    url: '/search_users',
    method: 'post',
    data: {
      csrfmiddlewaretoken: CSRF_TOKEN,
      query: query
    }
  })
  .done(function (result) {
    console.log(result)
    process(result)
  })
  .fail(function(error) {
    console.log(error)
  })
}

function addToSelectedUsers(username) {
  var userForm = $('#add-user-form')
  userForm.find('.user-to-add').text(username)
  userForm.find('#users-to-add').val([username])
}

function addMember() {
  $('#add-user-form').submit()
}

function removeMember(username) {
  var badge = $("[data-member='" + username + "']")
  
  editMembers({
    remove: [username],
    error: function(error) {
      badge.fadeIn('fast')
    }
  })
  
  badge.fadeOut('fast')
}

function editMembers(options) {
  $.ajax({
    url: 'edit_project_members',
    method: 'post',
    data: {
      csrfmiddlewaretoken: CSRF_TOKEN,
      remove: options.remove,
      add: options.add,
    },
    error: options.error,
    success: function (result) {
      console.log(result)
    } 
  })
}
