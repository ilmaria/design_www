/**
 * This function initializes and renders the calendar.
 * @param {string} element - The selector for element that is used as the
 *  calendar container.
 * @param {Function} template - Precompiled template function that takes
 *  a data object as a parameter.
 * @param {Object[]} events - List of event objects for calendar events.
 */
function initCalendar(element, template, events) {
  var calendar = $(element).clndr({
    template: template,
    events: events,
    weekOffset: 1   // week starts with Monday as it should
  })
}
