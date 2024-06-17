import pandas as pd
from jinja2 import Template

# Read the CSV file with a different delimiter
# Update 'delimiter' based on your file structure (e.g., ',' for comma, '\t' for tab, ' ' for space)
df = pd.read_csv('waveforms.csv', delimiter='\t', header=None)

# Convert the DataFrame to a JavaScript array
data_array = df.values.tolist()

# Define the template for the HTML file
template_str = """
<!DOCTYPE html>
<html>
<head>
  <title>Web Visualization Tool</title>
  <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
  <script src="https://d3js.org/d3.v6.min.js"></script>
  <script type="text/javascript">
    google.charts.load('current', {packages: ['corechart', 'bar']});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
      var data = google.visualization.arrayToDataTable([
        ['Index', 'Value'],
        {% for row in data %}
          [{{ loop.index0 }}, {{ row[0] }}],
        {% endfor %}
      ]);

      var lineOptions = {
        title: 'Waveform Line Chart',
        hAxis: {title: 'Index'},
        vAxis: {title: 'Value'},
        series: {1: {curveType: 'function'}}
      };

      var lineChart = new google.visualization.LineChart(document.getElementById('line_chart'));
      lineChart.draw(data, lineOptions);

      var barOptions = {
        title: 'Waveform Bar Chart',
        chartArea: {width: '50%'},
        hAxis: {title: 'Value'},
        vAxis: {title: 'Index'}
      };

      var barChart = new google.visualization.BarChart(document.getElementById('bar_chart'));
      barChart.draw(data, barOptions);
    }
  </script>
  <script>
    document.addEventListener("DOMContentLoaded", function() {
      var data = {{ data|tojson }};
      var width = 900;
      var height = 500;
      var margin = {top: 20, right: 20, bottom: 30, left: 40};

      var x = d3.scaleLinear().domain([0, data.length]).range([margin.left, width - margin.right]);
      var y = d3.scaleLinear().domain([0, d3.max(data, function(d) { return d[0]; })]).nice().range([height - margin.bottom, margin.top]);

      var svg = d3.select("#d3_chart").append("svg")
                  .attr("width", width)
                  .attr("height", height);

      svg.append("g")
         .attr("transform", "translate(0," + (height - margin.bottom) + ")")
         .call(d3.axisBottom(x).ticks(width / 80));

      svg.append("g")
         .attr("transform", "translate(" + margin.left + ",0)")
         .call(d3.axisLeft(y));

      svg.append("path")
         .datum(data)
         .attr("fill", "none")
         .attr("stroke", "steelblue")
         .attr("stroke-width", 1.5)
         .attr("d", d3.line()
                      .x(function(d, i) { return x(i); })
                      .y(function(d) { return y(d[0]); }));
    });
  </script>
</head>
<body>
  <h1>Web Visualization Tool</h1>
  <div id="line_chart" style="width: 900px; height: 500px;"></div>
  <div id="bar_chart" style="width: 900px; height: 500px;"></div>
  <div id="d3_chart" style="width: 900px; height: 500px;"></div>
</body>
</html>
"""

# Create a Jinja2 template from the string
template = Template(template_str)

# Render the template with the data
html_str = template.render(data=data_array)

# Write the HTML string to a file
with open('index.html', 'w') as f:
    f.write(html_str)

print("HTML file created successfully!")
