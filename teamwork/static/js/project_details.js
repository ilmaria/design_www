/**
 * Initialize search suggestions for searching users.
 */
$('#user-search').typeahead({
  source: searchUsers,
  afterSelect: function addUserToMembers(username) {
    addUserToForm(username, '#add-user-form', '#member-user-list',
      '#user-search', '#users-to-add')
  }
})

$('#assignees-input').typeahead({
  source: searchUsers,
  afterSelect: function addUserToTask(username) {
    addUserToForm(username, '#add-task-form', '#assignee-user-list',
      '#assignees-input', '#assignees-hidden')
  }
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
 * @param {string} form - Css selector for the form where the
 * usernames are added.
 * @param {string} userList - Selector for list element to store users.
 * @param {string} visibleInput - Selector for the visible input element.
 * @param {string} hiddenInput - Selector for the hidden input element.
 */
function addUserToForm(username, form, userList, visibleInput, hiddenInput) {
  var userForm = $(form)
  var userList = $(userList)

  var userItem = userList.children().first().clone()
  userItem.find('.added-user').text(username)
  userItem.data('username', username)
  userItem.removeClass('hidden')
  userList.append(userItem)

  var usernameList = userList.children().map(function() {
    return $(this).data('username')
  }).get()

  var userListInput = userForm.find(hiddenInput)
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
  $(visibleInput).val('')
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

/**
 * Submit form to delete a task.
 * @param {string} taskName - Name of the task to delete.
 */
function deleteTask(taskName) {
  // delete_task is the form element
  var input = $(delete_task).find('input[name="task_name"]')
  input.val(taskName)
  delete_task.submit()
}
