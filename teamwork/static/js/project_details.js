/**
 * Initialize search suggestions for searching users.
 */
$('#user-search').typeahead({
  source: function(query, process) {
    searchUsers(query, projectMembers, '', process)
  },
  afterSelect: function addUserToMembers(username) {
    addUserToForm(username, '#add-user-form', '#member-user-list',
      '#user-search', '#users-to-add')
  }
})

$('#assignees-input').typeahead({
  source: function(query, process) {
    searchUsers(query, '', projectMembers, process)
  },
  afterSelect: function addUserToTask(username) {
    addUserToForm(username, '#add-task-form', '#assignee-user-list',
      '#assignees-input', '#assignees-hidden')
  }
})

$('#edit-assignees').typeahead({
  source: function(query, process) {
    searchUsers(query, '', projectMembers, process)
  },
  afterSelect: function addUserToTask(username) {
    addUserToForm(username, '#edit-task-form', '#edit-assignee-list',
      '#edit-assignees', '#edit-assignees-hidden')
  }
})

/**
 * Initialize date picker for logging times in project.
 */
$('#datePicker').datepicker({
  autoclose: true,
  format: 'dd/mm/yyyy',
  todayBtn: 'linked'
})
$('#datePicker').datepicker('update', new Date())

/**
 * This function is for searching new project members. It gets all
 * registered users that match the `query` from the server and then it
 * filters out the current project members. Remaining usernames are
 * processed with `process` callback that is given as parameter.
 * @param {string} query - Query for searching matching usernames.
 * @param {Function} process - Callback function for processing returned
 * usernames. (Used by the typeahead plugin.)
 */
function searchUsers(query, blacklist, whitelist, process) {
  $.ajax({
    url: '/search_users',
    method: 'post',
    data: {
      csrfmiddlewaretoken: CSRF_TOKEN,
      query: query,
      blacklist: blacklist,
      whitelist: whitelist
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

  $.ajax({
    url: 'edit_project_members',
    method: 'post',
    data: {
      csrfmiddlewaretoken: CSRF_TOKEN,
      'users-to-remove': username,
    }
  })

  badge.fadeOut('fast')
}

/**
 * Autofill selected task information to the edit task modal.
 * @param {string} taskStr - Task to edit.
 */
function editTaskModal(taskStr) {
  var task = taskStr.split(';')
  var name = task[0]

  var assignees = task[1].split(',').filter(function(username) {
    return username.length > 0
  })

  var estimate = task[2].split(':')
  estimate.pop()
  estimate = estimate.join(':')

  assignees.forEach(function(username) {
    addUserToForm(username, '#edit-task-form', '#edit-assignee-list',
      '#edit-assignees', '#edit-assignees-hidden')
  })

  $('#old-task-name').val(name)
  $('#edit-task-name').val(name)
  $('#remove-task-name').val(name)
  $('#edit-time-estimate').val(estimate)
}

function taskDoneToggle(taskId, event) {
  var progressBar = $('#task-progress-' + taskId)
  var taskDone = event.target.checked ? 1 : 0

  $.ajax({
    url: 'toggle_task_done',
    method: 'post',
    data: {
      csrfmiddlewaretoken: CSRF_TOKEN,
      'task-id': taskId,
      'task-done': taskDone
    }
  })

  if (taskDone) {
    progressBar
      .css('width', 100+'%')
      .attr('aria-valuenow', 100)
      .text('100%')
  } else {
    var original = progressBar.data('original-value')
    progressBar
      .css('width', original+'%')
      .attr('aria-valuenow', original)
      .text(original+'%')
  }
}

$(function() {
  // Trigger click twice to set the progress bar dynamically.
  $('.task-done').each(function() {
    $(this).trigger('click').trigger('click')
  })
})
