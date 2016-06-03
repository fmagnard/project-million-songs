d3.csv("./data/features_per_year.csv", function(error, data) {
  if (error) throw error;
  
  var margin = {top: 20, right: 50, bottom: 30, left: 30},
    width = parseInt(d3.select('#d3div6').style('width'), 10)
    width = width - margin.left - margin.right,
    height = 600 - margin.top - margin.bottom;

var parseDate = d3.time.format("%Y").parse;

var x = d3.time.scale()
    .range([0, width]);

var y = d3.scale.linear()
    .range([height, 0]);

var color = d3.scale.category10();

var featureNames = {
	artist_familiarity: 'artist_familiarity', 
	artist_hotness: 'artist artist_hotness',
	duration: 'artist duration',
	loudness: 'loudness',
	tempo: 'tempo'
};

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var line6 = d3.svg.line()
    .interpolate("basis")
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.scores); });

var chart6 = d3.select("#d3div6").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	  color.domain(d3.keys(data[0]).filter(function(key) {
	  	return key == "duration";
	  }));
	
	  data.forEach(function(d) {
	    d.date = parseDate(d.year);
	  });
	
	  var cities = color.domain().map(function(name) {
	    return {
	      name: name,
	      values: data.map(function(d) {
	        return {date: d.date, scores: +d[name]};
	      })
	    };
	  });
	
	  x.domain(d3.extent(data, function(d) { return d.date; }));
	
	  y.domain([
	    d3.min(cities, function(c) { return d3.min(c.values, function(v) { return v.scores; }); }),
	    d3.max(cities, function(c) { return d3.max(c.values, function(v) { return v.scores; }); })
	  ]);
	  //y.domain([0,1]);
	
	  chart6.append("g")
	      .attr("class", "x axis")
	      .attr("transform", "translate(0," + height + ")")
	      .call(xAxis);
	
	  chart6.append("g")
	      .attr("class", "y axis")
	      .call(yAxis)
	    .append("text")
	      .attr("transform", "rotate(-90)")
	      .attr("y", 6)
	      .attr("dy", ".71em")
	      .style("text-anchor", "end")
	      .text("average value");
	
	  var city = chart6.selectAll(".city")
	      .data(cities)
	    .enter().append("g")
	      .attr("class", "city");
	
	  city.append("path")
	      .attr("class", "line")
	      .attr("d", function(d) { return line6(d.values); })
	      .style("stroke", function(d) { return color(d.name); });
	
	  city.append("text")
	      .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
	      .attr("transform", function(d) { return "translate(" + x(d.value.date) + "," + y(d.value.scores) + ")"; })
	      .attr("x", 3)
	      .attr("dy", ".35em")
	      .text(function(d) { return d.name; });
	      
	      
	      
	  d3.select("[name=graph6feature]").on("change", function(){
	    featureNames = this.value;
	    
	     var lk = d3.select("[name=graph6feature]").value
	     console.log(lk)
	    
	    color.domain(d3.keys(data[0]).filter(function(key) {
		  	return key == featureNames;
		  }));
	
	  var cities = color.domain().map(function(name) {
	    return {
	      name: name,
	      values: data.map(function(d) {
	        return {date: d.date, scores: +d[name]};
	      })
	    };
	  });
	
	  y.domain([
	    d3.min(cities, function(c) { return d3.min(c.values, function(v) { return v.scores; }); }),
	    d3.max(cities, function(c) { return d3.max(c.values, function(v) { return v.scores; }); })
	  ]);
	  
	  var city = chart6.selectAll(".city")
	      .data(cities)
	      .attr("class", "city");
	
	  city.select("path")
	  		.transition()
	      .attr("class", "line")
	      .attr("d", function(d) { return line6(d.values); })
	      .style("stroke", function(d) { return color(d.name); });
	      
		chart6.select(".y.axis").transition().call(yAxis);
		
	city.select("text")
	      .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
	      .transition()
	      .attr("transform", function(d) { return "translate(" + x(d.value.date) + "," + y(d.value.scores) + ")"; })
	      .attr("x", 3)
	      .attr("dy", ".35em")
	      .text(function(d) { return d.name; });
	    
	  });
});