/**
 * This function initializes and renders the calendar.
 * @param {string} element - The selector for element that is used as the
 *  calendar container.
 * @param {Function} template - Precompiled template function that takes
 *  a data object as a parameter.
 * @param {Object[]} events - List of event objects for calendar events.
 */
function initCalendar(element, template, events) {
  $(element).each(function() {
    var calendar = $(this).clndr({
      template: template,
      events: events,
      daysOfTheWeek: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
      weekOffset: 1,   // week starts with Monday as it should
      forceSixRows: true,
      clickEvents: {
        click: onClickDay
      }
    })
  })
}

function onClickDay(day) {
  if (day.events.length) {
    var eventListModal = $('#event-list-modal')
    var eventList = eventListModal.find('.modal-body .event-list')
    var template = eventList.find('.event-item').first().clone()
    eventList.empty()

    day.events.forEach(function(event) {
      var eventHtml = template.clone()
      eventHtml.find('.event-name').text(
        moment(event.date).format('hh:mm')  + ' - ' + event.name)

      if (event.location) {
        eventHtml.find('.event-location').text(event.location)
      } else {
        eventHtml.find('.event-location').remove()
      }

      eventHtml.appendTo(eventList)
    })

    eventListModal.modal('show')
  }
}
