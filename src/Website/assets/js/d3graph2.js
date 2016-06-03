d3.csv("./data/thematic_per_year_norm.csv", function(error, data) {
  if (error) throw error;
  
  var margin = {top: 20, right: 60, bottom: 30, left: 30},
    width = parseInt(d3.select('#d3div2').style('width'), 10)
    width = width - margin.left - margin.right,
    height = 700 - margin.top - margin.bottom;
    
var parseDate = d3.time.format("%Y").parse;

var x = d3.time.scale()
    .range([0, width]);

var y = d3.scale.linear()
    .range([height, 0]);

var color = d3.scale.category10();

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var line = d3.svg.line()
    .interpolate("basis")
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.temperature); });

var chart2 = d3.select("#d3div2").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")

  color.domain(d3.keys(data[0]).filter(function(key) { return key !== "year"; }));

  data.forEach(function(d) {
    d.date = parseDate(d.year);
  });

  var cities = color.domain().map(function(name) {
    return {
      name: name,
      values: data.map(function(d) {
        return {date: d.date, temperature: +d[name]};
      })
    };
  });

  x.domain(d3.extent(data, function(d) { return d.date; }));

  y.domain([
    d3.min(cities, function(c) { return d3.min(c.values, function(v) { return v.temperature; }); }),
    d3.max(cities, function(c) { return d3.max(c.values, function(v) { return v.temperature; }); })
  ]);
  
  

  chart2.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  chart2.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Appearance of lexical field");

  var city = chart2.selectAll(".city")
      .data(cities)
    .enter().append("g")
      .attr("class", "city");

  city.append("path")
      .attr("class", "line")
      .attr("d", function(d) { return line(d.values); })
      .style("stroke", function(d) { return color(d.name); });

  city.append("text")
      .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
      .attr("transform", function(d) { return "translate(" + x(d.value.date) + "," + y(d.value.temperature) + ")"; })
      .attr("x", 3)
      .attr("dy", ".35em")
      .text(function(d) { return d.name; });
      
  var datas = [1950,1975];
	var objects = datas.slice(0, datas.length/2).map(
	 function(d,i) { return { value:d, average:datas[i+datas.length/2] }; } 
	);
	var bars = chart2.selectAll("g.bar")
	  .data(objects)
	 .enter().append("g")
	   .attr("class", "bar")
	   .attr("transform", function(d,i) { return "translate("+(i*10)+",0)"; });
	
	
	bars.append("rect")
	   .attr("x",function(d,i) { return (d.value-1900)*8.2; })
	   .attr("y", function(d,i) { return height - d.value; })
	   .attr("width", 8.2*25)
	   .attr("height", function(d,i) { return d.value; })
	   .attr("opacity",0.1);
	
	bars.append("text")
	   .attr("x",function(d,i) { return (d.value-1900)*8.2+8.2*25/2-20; })
	   .text("Vietnam War");
});