d3.csv("./data/features_scatterplot.csv", function(d) {
	return {
		duration : +d["duration"],
		artist_familiarity : +d["artist_familiarity"],
		artist_hotness : +d["artist_hotttnesss"],
		year : +d["year"]
	};
	},function(data) {
	
	
var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = parseInt(d3.select('#d3div3').style('width'), 10)
    width = width - margin.left - margin.right,
    height = 550 - margin.top - margin.bottom;
    
var aspect = width / height;
  
var x = d3.scale.linear()
    .range([0, width]);

var y = d3.scale.linear()
    .range([height, 0]);

var color = d3.scale.category10();

var axisNames = {
	duration: 'duration', 
	artist_familiarity: 'artist familiarity',
	artist_hotness: 'artist hotness',
	year: 'year',
};

var graph3xAXis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var graph3yAXis = d3.svg.axis()
    .scale(y)
    .orient("left");


var chart3 = d3.select("#d3div3").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  x.domain([1900, d3.max(data, function(d) { return d.year; })]).nice();
  y.domain(d3.extent(data, function(d) { return d.duration; })).nice();

  chart3.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(graph3xAXis)
    .append("text")
      .attr("class", "graph3label")
      .attr("x", width)
      .attr("y", -6)
      .style("text-anchor", "end")
      .text("year");

  chart3.append("g")
      .attr("class", "y axis")
      .call(graph3yAXis)
    .append("text")
      .attr("class", "graph3label")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("duration")

 var circles = chart3.selectAll(".dot")
      .data(data)
    .enter().append("circle")
      .attr("class", "dot")
      .attr("r", 3.5)
      .attr("cx", function(d) { return x(d.year); })
      .attr("cy", function(d) { return y(d.duration); })
      .style("fill", "blue");
      //.style("fill", function(d) { return color(d.species); });


  var legend = chart3.selectAll(".legend")
      .data(color.domain())
      .enter().append("g")
      .attr("class", "legend")
      .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });


  /*legend.append("rect")
      .attr("x", width - 18)
      .attr("width", 18)
      .attr("height", 18)
      .style("fill", color);


  legend.append("text")
      .attr("x", width - 24)
      .attr("y", 9)
      .attr("dy", ".35em")
      .style("text-anchor", "end")
      .text(function(d) { return d; });*/

  d3.select("[name=graph3xAX]").on("change", function(){
    graph3xAXy = this.value;
    console.log(graph3xAXy)
    if (graph3xAXy == "year"){
	    x.domain([1900, d3.max(data, function(d) { return d.year; })]).nice();
    }
    else{
	    x.domain(d3.extent(data, function(d) { return d[graph3xAXy]; })).nice();
    }
    
    chart3.select(".x.axis").transition().call(graph3xAXis);

    chart3.selectAll(".dot").transition().attr("cx", function(d) { 
        return x(d[graph3xAXy]);
    });
    chart3.selectAll(".x.axis").selectAll("text.graph3label").text(axisNames[graph3xAXy]);
  });

  d3.select("[name=graph3yAX]").on("change", function(){
    graph3yAXy = this.value;
    console.log(graph3yAXy)
    if (graph3yAXy == "year"){
	    y.domain([1900, d3.max(data, function(d) { return d.year; })]).nice();
    }
    else{
	    y.domain(d3.extent(data, function(d) { return d[graph3yAXy]; })).nice();
    }
    chart3.select(".y.axis").transition().call(graph3yAXis);
    chart3.selectAll(".dot").transition().attr("cy", function(d) { 
        return y(d[graph3yAXy]);
    });
    chart3.selectAll(".y.axis").selectAll("text.graph3label").text(axisNames[graph3yAXy]);
  });

});