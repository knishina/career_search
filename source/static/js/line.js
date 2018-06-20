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

var svg2 = d3.select("#line")
    .append("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight);

var chartGroup2 = svg2.append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Get the data.    
d3.json("/data", function (error, response) {
    if (error) throw error;
    
    var line1p = [];
    var line2p = [];
    var line3p = [];
    var line4p = [];
    var line5p = [];
    var line6p = [];
    var line7p = [];
    var line8p = [];
    var line9p = [];
    var line10p = [];
    
    for (var i=0; i<24; i++) {
        line1p.push({
            x: response[0].x_axis_time_of_day[i],
            y: response[0].y_axis_travel_time_sec[i]
        });
        line2p.push({
            x: response[1].x_axis_time_of_day[i],
            y: response[1].y_axis_travel_time_sec[i]
        });
        line3p.push({
            x: response[2].x_axis_time_of_day[i],
            y: response[2].y_axis_travel_time_sec[i]
        });
        line4p.push({
            x: response[3].x_axis_time_of_day[i],
            y: response[3].y_axis_travel_time_sec[i]
        });
        line5p.push({
            x: response[4].x_axis_time_of_day[i],
            y: response[4].y_axis_travel_time_sec[i]
        });
        line6p.push({
            x: response[5].x_axis_time_of_day[i],
            y: response[5].y_axis_travel_time_sec[i]
        });
        line7p.push({
            x: response[6].x_axis_time_of_day[i],
            y: response[6].y_axis_travel_time_sec[i]
        });
        line8p.push({
            x: response[7].x_axis_time_of_day[i],
            y: response[7].y_axis_travel_time_sec[i]
        });
        line9p.push({
            x: response[8].x_axis_time_of_day[i],
            y: response[8].y_axis_travel_time_sec[i]
        });
        line10p.push({
            x: response[9].x_axis_time_of_day[i],
            y: response[9].y_axis_travel_time_sec[i]
        });
    };
    var max1 = d3.max(line1p, d => d.y);
    var max2 = d3.max(line2p, d => d.y);
    var max3 = d3.max(line3p, d => d.y);
    var max4 = d3.max(line4p, d => d.y);
    var max5 = d3.max(line5p, d => d.y);
    var max6 = d3.max(line6p, d => d.y);
    var max7 = d3.max(line7p, d => d.y);
    var max8 = d3.max(line8p, d => d.y);
    var max9 = d3.max(line9p, d => d.y);
    var max10 = d3.max(line10p, d => d.y);
    var max_ave = (max1+max2+max3+max4+max5+max6+max7+max8+max9+max10)/10;

    var xLinearScale = d3.scaleLinear()
        .domain([0, 24])
        .range([0, width]);
    var yLinearScale = d3.scaleLinear()
        .domain([0, max_ave+40])
        .range([height,0]);
    
    var bottomAxis = d3.axisBottom(xLinearScale);
    var leftAxis = d3.axisLeft(yLinearScale);

    chartGroup2.append("g")
        .attr("transform", `translate(0, ${height})`)
        .call(bottomAxis);
    chartGroup2.append("g")
        .call(leftAxis);

    // Set up the lines.
    var line1 = d3.line()
        .x(d => xLinearScale(d.x))
        .y(d => yLinearScale(d.y));
    var line2 = d3.line()
        .x(d => xLinearScale(d.x))
        .y(d => yLinearScale(d.y));
    var line3 = d3.line()
        .x(d => xLinearScale(d.x))
        .y(d => yLinearScale(d.y));
    var line4 = d3.line()
        .x(d => xLinearScale(d.x))
        .y(d => yLinearScale(d.y));
    var line5 = d3.line()
        .x(d => xLinearScale(d.x))
        .y(d => yLinearScale(d.y));
    var line6 = d3.line()
        .x(d => xLinearScale(d.x))
        .y(d => yLinearScale(d.y));
    var line7 = d3.line()
        .x(d => xLinearScale(d.x))
        .y(d => yLinearScale(d.y));
    var line8 = d3.line()
        .x(d => xLinearScale(d.x))
        .y(d => yLinearScale(d.y));
    var line9 = d3.line()
        .x(d => xLinearScale(d.x))
        .y(d => yLinearScale(d.y));
    var line10 = d3.line()
        .x(d => xLinearScale(d.x))
        .y(d => yLinearScale(d.y));

    chartGroup2.append("path")
        .attr("d", line1(line1p))
        .attr("fill", "none")
        .attr("stroke", "#21AEBF")
        .attr("stroke-width", 3);
    chartGroup2.append("path")
        .attr("d", line2(line2p))
        .attr("fill", "none")
        .attr("stroke", "#7FB3D5")
        .attr("stroke-width", 3);
    chartGroup2.append("path")
        .attr("d", line3(line3p))
        .attr("fill", "none")
        .attr("stroke", "#138D75")
        .attr("stroke-width", 3);
    chartGroup2.append("path")
        .attr("d", line4(line4p))
        .attr("fill", "none")
        .attr("stroke", "#E67E22")
        .attr("stroke-width", 3);
    chartGroup2.append("path")
        .attr("d", line5(line5p))
        .attr("fill", "none")
        .attr("stroke", "#FF000F")
        .attr("stroke-width", 3);
    chartGroup2.append("path")
        .attr("d", line6(line6p))
        .attr("fill", "none")
        .attr("stroke", "#8E44AD")
        .attr("stroke-width", 3);
    chartGroup2.append("path")
        .attr("d", line7(line7p))
        .attr("fill", "none")
        .attr("stroke", "#F20B9A")
        .attr("stroke-width", 3);
    chartGroup2.append("path")
        .attr("d", line8(line8p))
        .attr("fill", "none")
        .attr("stroke", "#FFDE26")
        .attr("stroke-width", 3);
    chartGroup2.append("path")
        .attr("d", line9(line9p))
        .attr("fill", "none")
        .attr("stroke", "#00ECFF")
        .attr("stroke-width", 3);
    chartGroup2.append("path")
        .attr("d", line10(line10p))
        .attr("fill", "none")
        .attr("stroke", "#0032FF")
        .attr("stroke-width", 3);

    
    // Set up the title and axes labels.
    chartGroup2.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0-margin.left + 40)
      .attr("x", 0-`${(height/2)}`)
      .attr("dy", "1em")
      .attr("class", "axisText")
      .text("Time of Commute (min)");

    chartGroup2.append("text")
      .attr("transform", `translate(${width/2}, ${height + 50})`)
      .attr("class", "axisText")
      .text("Time (24-hour clock)");
    
    chartGroup2.append("text")
      .attr("transform", `translate(${(width/2)}, ${-20})`)
      .attr("class", "axisText")
      .text("Commute Times Throughout the Day")
      .style("font-size", 20);
    
});

