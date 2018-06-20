// THIS IS GOING TO BE THE BUBBLE GRAPH THAT SHOWS PERCENT MATCH V. COMMUTE TIME.

// Set up size of svg
var svgWidth = 600;
var svgHeight = 400;

var margin = {
    top: 50,
    right: 40,
    bottom: 60,
    left: 100
};

var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;

var svg1 = d3.select("#chart")
    .append("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight);

var chartGroup1 = svg1.append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Get the data.    
d3.json("/data", function (error, response) {
    if (error) throw error;
    // Make it a number.
    response.forEach(function(d) {
        d.commute_min = + (d.commute_dur_sec/60).toFixed(0);
        d.percent_match = + d.percent_match;
    });

    // Set up the scale and axis values.
    var xLinearScale = d3.scaleLinear()
        .domain([0, d3.max(response, d => d.commute_min + 5)])
        .range([0, width]);
    var yLinearScale = d3.scaleLinear()
        .domain([0, 100])
        .range([height,0]);
    
    var bottomAxis = d3.axisBottom(xLinearScale);
    var leftAxis = d3.axisLeft(yLinearScale);

    chartGroup1.append("g")
        .attr("transform", `translate(0, ${height})`)
        .call(bottomAxis);
    chartGroup1.append("g")
        .call(leftAxis);

    // Set up the circles.
    var circlesGroup = chartGroup1.selectAll("circle")
        .data(response)
        .enter()
        .append("a")
            .attr("xlink:href", function (d) {return `${d.url}`})
            .attr("xlink:show", "new")
        .append("circle")
        .attr("cx", d => xLinearScale(d.commute_min))
        .attr("cy", d => yLinearScale(d.percent_match))
        .attr("r", "15")
        .attr("fill", function() {
            for (var i=0; i<response.length; i++) {
                if (response[i].data_source == "Glassdoor") {
                    return ("#2980B9")
                }
                else {
                    return ("#85929E")
                }
            }
        })
        .attr("opacity", ".5");
    
    // Set up the tooltips and mouse over/out.
    var toolTip1 = d3.tip()
        .attr("class", "tooltip")
        .offset([80, -60])
        .html(function(d) {
            return (`Company: ${d.company}<br>Match: ${d.percent_match}%<br>Source: ${d.data_source}`)
        });
    
    chartGroup1.call(toolTip1);

    circlesGroup.on("mouseover", function (data) {
        toolTip1.show(data);
      })
      .on("mouseout", function (data, index) {
        toolTip1.hide(data);
      });

    
    // Set up the title and axes labels.
    chartGroup1.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0-margin.left + 40)
      .attr("x", 0-`${(height/2)}`)
      .attr("dy", "1em")
      .attr("class", "axisText")
      .text("Percent Match (%)");

    chartGroup1.append("text")
      .attr("transform", `translate(${width/2}, ${height + 50})`)
      .attr("class", "axisText")
      .text("Duration of Commute (min)");
    
    chartGroup1.append("text")
      .attr("transform", `translate(${(width/2)}, ${-20})`)
      .attr("class", "axisText")
      .text("Percent Match v. Commute Time")
      .style("font-size", 20)
})