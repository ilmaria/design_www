function initPiechart(loggedTimes) {
  google.charts.load("current", {packages:["corechart"]})
  google.charts.setOnLoadCallback(function() {
    drawChart(loggedTimes)
  })
}

function drawChart(loggedTimes) {
  var headers = ['User', 'Total logged time']
  // add headers to the beginning of loggedTimes array
  loggedTimes.unshift(headers)
  var data = google.visualization.arrayToDataTable(loggedTimes)

  // format logged hours to have 'h' as unit
  var formatter = new google.visualization.NumberFormat({
    suffix: 'h',
    fractionDigits: 1
  })
  formatter.format(data, 1)

  var options = {
    title: 'Total logged times',
    pieHole: 0.4,
  }

  var chart = new google.visualization
    .PieChart(document.querySelector('#piechart'))

  chart.draw(data, options)
}
