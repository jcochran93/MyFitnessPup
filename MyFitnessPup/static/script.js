TESTER = document.getElementById('tester');

fetch('/weight')
.then(res => res.json())
.then(weightHistory => {
    
    var dates = Object.keys(weightHistory.weight);
    var pounds = Object.values(weightHistory.weight)
    console.log(dates);

    var data = [{
        type: "line",
        y: pounds,
        x: dates
        }];

    var layout = {xaxis: {type: 'date'}, 
                margin: {l: 40, r:2},
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)' };

    var config = {staticPlot: true}

    Plotly.newPlot(TESTER, data, layout, config);
})

var defaultDate = document.querySelector('input[type="date"]');
let today = new Date().toISOString().slice(0, 10)

defaultDate.value = today
