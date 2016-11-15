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
    // filter usernames if they are already in to-be-added list
    var usernames = result.filter(function(username) {
      var addedUsernames = $('.user-list').children().map(function() {
        return $(this).data('username')
      }).get()
      return addedUsernames.indexOf(username) === -1
    })
    process(usernames)
  })
  .fail(function(error) {
    console.log(error)
  })
}

function addToSelectedUsers(username) {
  var userForm = $('#add-user-form')
  var userList = $('.user-list')

  var userItem = userList.children().first().clone()
  userItem.find('.added-user').text(username)
  userItem.data('username', username)
  userItem.removeClass('hidden')
  userList.append(userItem)

  var usernameList = userList.children().map(function() {
    return $(this).data('username')
  }).get()

  var userListInput = userForm.find('input#users-to-add')
  userListInput.val(usernameList)

  // event listener for clicking 'x' to remove a username
  userItem.find('.remove-member').on('click', function() {
    var username = userItem.data('username')
    userItem.remove()
    var usernames = userListInput.val().split(',')
    var index = usernames.indexOf(username)

    if (index > -1) {
      usernames.splice(index, 1)
    }

    userListInput.val(usernames)
  })

  // empty search field
  $('#user-search').val('')
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

function logTime(){
  var logTimeForm = $('#logTimeForm')
  var logHours = $('#logHours')
  var logMinutes = $('#logMinutes')

  var logDateInput = $('#logDate').val()

}
