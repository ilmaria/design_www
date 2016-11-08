$('#user-search').typeahead({
  source: searchUsers
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

function removeMember(username) {
  var badge = $("[data-member='" + username + "']")
  
  $.ajax({
    url: 'edit_project_members',
    method: 'post',
    data: {
      csrfmiddlewaretoken: CSRF_TOKEN,
      remove: [username]
    }
  })
  .done(function (result) {
    console.log(result)
  })
  .fail(function(error) {
    badge.fadeIn('fast')
    console.log(error)
  })

  badge.fadeOut('fast')
}
