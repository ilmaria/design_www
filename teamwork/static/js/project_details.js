/**
 * Initialize search suggestions for searching users.
 */
$('#user-search').typeahead({
  source: searchUsers,
  afterSelect: addToSelectedUsers
})

/**
 * Initialize date picker for logging times in project. 
 */
$('#datePicker').datepicker({
  autoclose: true,
  format: 'dd/mm/yyyy',
  todayBtn: 'linked'
});

/**
 * This function is for searching new project members. It gets all
 * registered users that match the `query` from the server and then it
 * filters out the current project members. Remaining usernames are
 * processed with `process` callback that is given as parameter.
 * @param {string} query - Query for searching matching usernames.
 * @param {Function} process - Callback function for processing returned
 * usernames. (Used by the typeahead plugin.)
 */
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

/**
 * Adds `username` to the list of selected users that are to be added
 * to the project.
 * @param {string} username - Username to add to the project.
 */
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

/**
 * Submit form for adding new users.
 */
function addMember() {
  $('#add-user-form').submit()
}

/**
 * Remove member with given username from the project.
 * @param {string} username - Username to be removed from the project.
 */
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

/**
 * Ajax function for adding or removing users from the project.
 * @param {Object} options - An object with properties `remove` and `add`
 * that are arrays of usernames.
 */
function editMembers(options) {
  $.ajax({
    url: 'edit_project_members',
    method: 'post',
    data: {
      csrfmiddlewaretoken: CSRF_TOKEN,
      remove: options.remove,
      add: options.add,
    },
    error: options.error
  })
}
