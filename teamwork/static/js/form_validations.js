//---------------------------------------------------
// Functions to validate forms before submit
//---------------------------------------------------

function validateNewTimelog() {
  // check if: logDate AND (logHours OR logMinutes)
  return $('#logDate').val() !== '' && 
    ($('#logHours').val() !== '' || $('#logMinutes').val() !== '')
}

function validateNewMembers() {
  // fail if trying to send an empty username
  return $('input#users-to-add').val() !== ''
}

function validateNewProject() {
  // fail if trying to send an empty project name
  return $('input#new-project-name').val() !== ''
}

function validateNewEventName() {
  // fail if trying to send an empty event name
  return $('input#new-event-name').val() !== '' && 
  ($('#eventTime').val() !== '')
}