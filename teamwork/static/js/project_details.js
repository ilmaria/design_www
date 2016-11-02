function editMembers() {
  
}

function removeMember(username) {
  $.ajax({
    url: 'edit_project_members',
    method: 'post',
    data: {
      csrfmiddlewaretoken: CSRF_TOKEN,
      'remove': [username]
    }
  })
  .done(function (params) {
    console.log(params)
  })
  .fail(function(params) {
    console.log(params)
  })
}