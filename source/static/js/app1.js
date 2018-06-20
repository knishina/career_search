d3.json("/data", function(error, response) {
    if (error) throw error;
    // Add data for entry1
    function render() {
        for (var i=0; i<response.length; i=i+2) {
            var a = d3.select(".entry1")
                .append("a")
                .attr("href", response[i].url)
                .attr("target", "_blank")
                .text(response[i].company);
                
                d3.select(".entry1")
                    .append("h5")
                    .text(`${response[i].title}`)
                d3.select(".entry1")
                    .append("h6")
                    .text(`${response[i].city}, CA`)
                d3.select(".entry1") 
                    .append("h6")
                    .text(`Commute Time: ${response[i].communte_dur_text}`)
                d3.select(".entry1")
                    .append("h6")
                    .html(`Percent Match: ${response[i].percent_match}%<br><br>`)
        }
        for (var i=1; i<response.length; i=i+2) {
            var a = d3.select(".entry2")
                .append("a")
                .attr("href", response[i].url)
                .attr("target", "_blank")
                .text(response[i].company);
                
                d3.select(".entry2")
                    .append("h5")
                    .text(`${response[i].title}`)
                d3.select(".entry2")
                    .append("h6")
                    .text(`${response[i].city}, CA`)
                d3.select(".entry2") 
                    .append("h6")
                    .text(`Commute Time: ${response[i].communte_dur_text}`)
                d3.select(".entry2")
                    .append("h6")
                    .html(`Percent Match: ${response[i].percent_match}%<br><br>`)
        }
        colors = ["#21AEBF", "#7FB3D5", "#138D75", "#E67E22", "#FF000F", "#8E44AD", "#F20B9A", "#FFDE26", "#00ECFF", "#0032FF"]
        for (var i=0; i<response.length; i++) {
            var a = d3.select(".entry3")
                .append("p")
                .text(response[i].company)
                .style("color", function() {
                    return colors[i]
                })
                .style("font-size", "10px")
                .style("padding", "0px")
        }
    }
    render()       
})