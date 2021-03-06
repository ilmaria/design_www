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
    chartArea:{left:6,top:1,width:'85%',height:'85%'},
    legend:{textStyle: {color: '#34495e',fontSize: 18,fontName: 'Lato'}},
    tooltip:{textStyle: {color: '#34495e',fontSize: 18,fontName: 'Lato'}},
    colors: ['#1ABC9C', '#BDC3C7', '#7F8C8D', '#34495E', '#2C3E50', '#16A085'],
    pieHole: 0.4,
  }

  var chart = new google.visualization
    .PieChart(document.querySelector('#piechart'))

  chart.draw(data, options)
}
