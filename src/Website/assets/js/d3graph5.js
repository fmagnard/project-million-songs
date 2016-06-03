d3.csv("./data/genre_per_year_norm.csv", function(error, data) {
  if (error) throw error;
  
  var margin = {top: 20, right: 40, bottom: 30, left: 0},
    width = parseInt(d3.select('#d3div5').style('width'), 10)
    width = width - margin.left - margin.right,
    height = 700 - margin.top - margin.bottom;
    
	var datearray = [];
	    
	var format = d3.time.format("%Y");
	    
	var tip = d3.tip()
	  	.attr('class', 'd3-tip')
	  	.offset([0, 0])
	  	.html(function(d) {
			return getName(d);
	    })
	
	var x = d3.time.scale()
	    .range([0, width]);
	
	var y = d3.scale.linear()
	    .range([height-10, 0]);
	    
	var z = d3.scale.category20()
	
	var xAxis = d3.svg.axis()
	    .scale(x)
	    .orient("bottom")
	
	var yAxis = d3.svg.axis()
	    .scale(y);
	
	var stack = d3.layout.stack()
	    .offset("silhouette")
	    .values(function(d) { return d.values; })
	    .x(function(d) { return d.date; })
	    .y(function(d) { return d.value; });
	
	var nest = d3.nest()
	    .key(function(d) { return d.key; });
	
	var area = d3.svg.area()
	    .interpolate("cardinal")
	    .x(function(d) { return x(d.date); })
	    .y0(function(d) { return y(d.y0); })
	    .y1(function(d) { return y(d.y0 + d.y); });
	
	var chart5 = d3.select("#d3div5").append("svg")
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
	  .append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
	    
	chart5.call(tip);
	
	data.forEach(function(d) {
    d.date = format.parse(d.date);
    d.value = +d.value;
  });

  var layers = stack(nest.entries(data));

  x.domain(d3.extent(data, function(d) { return d.date; }));
  y.domain([0, d3.max(data, function(d) { return d.y0 + d.y; })]);
  
  chart5.selectAll(".layer")
      .data(layers)
    .enter().append("path")
      .attr("class", "layer")
      .attr("d", function(d) { return area(d.values); })
      .style("fill", function(d, i) { return z(i); });


  chart5.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  chart5.append("g")
      .attr("class", "y axis")
      .attr("transform", "translate(" + width + ", 0)")
      .call(yAxis.orient("right"))
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 30)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Genre ratio (over 100%)");
  
  chart5.selectAll(".layer")
    .on('mouseover', tip.show)
	.on('mouseout', tip.hide);
  
});

function getName(d){
	var outputString = '';
	outputString += d.key;
	return outputString;
}