//---------------------------------------------------
// Functions to validate forms before submit
//---------------------------------------------------

function validateNewTimelog() {
  // check if: logDate AND (logHours OR logMinutes)
  return $('#log-date-input').val() !== '' &&
    (parseInt($('#log-time-input').val()) > 0 ||
      Number($('#log-time-input').val().split(':')[1]) > 0)
}

function validateDashboardTimelog(event) {
  var form = $(event.target)

  // check if: logDate AND (logHours OR logMinutes)
  return form.find('input[name=date]').val() !== '' &&
    (parseInt(form.find('input[name=time]').val()) > 0 ||
      Number(form.find('input[name=time]').val().split(':')[1]) > 0)
}

function validateNewEvent() {
  // check if: logDate AND (logHours OR logMinutes)
  return $('#event-date').val() !== '' &&
    $('#event-time').val() !== '' &&
    $('#event-name').val() !== ''
}

function validateEventEdit() {
  // check if: logDate AND (logHours OR logMinutes)
  return $('#edit-event-date').val() !== '' &&
    $('#edit-event-time').val() !== '' &&
    $('#edit-event-name').val() !== ''
}

function validateNewMembers() {
  // fail if trying to send an empty username
  return $('input#users-to-add').val() !== ''
}

function validateNewProject() {
  // fail if trying to send an empty project name
  return $('input#new-project-name').val() !== ''
}

function validateNewTask() {
  var estimate = $('input#time-estimate-input').val()
  var isEstimateValid = true

  if (estimate) {
    var time = estimate.split(':')
    var hours = Number(time[0])
    var minutes = time.length === 2 ? Number(time[1]) : 0

    if (isNaN(hours) || isNaN(minutes) || minutes > 59 || time.length > 2) {
      isEstimateValid = false
    }
  }

  return $('input#task-name-input').val() !== '' && isEstimateValid
}

function validateTaskEdit() {
  var estimate = $('#edit-time-estimate').val()
  var isEstimateValid = true

  if (estimate) {
    var time = estimate.split(':')
    var hours = Number(time[0])
    var minutes = time.length === 2 ? Number(time[1]) : 0

    if (isNaN(hours) || isNaN(minutes) || minutes > 59 || time.length > 2) {
      isEstimateValid = false
    }
  }

  return $('#edit-task-name').val() !== '' && isEstimateValid
}
