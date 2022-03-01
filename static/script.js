TESTER = document.getElementById('tester');

var data = [{
    type: "line",
    y: [88, 85, 86, 84, 85],
    x: ["2021-09-02", "2021-10-10", "2021-11-12", "2021-12-22", "2022-01-15" ]
    }];
    
var layout = {xaxis: {type: 'date'}, 
              margin: {l: 40, r:2},
              paper_bgcolor: 'rgba(0,0,0,0)',
              plot_bgcolor: 'rgba(0,0,0,0)' };

var config = {staticPlot: true}

Plotly.newPlot(TESTER, data, layout, config);

let userName = document.getElementById('userName')

// fetch('/weight-data/1')
// .then(res => res.json())
// .then(user => {
//     userName.innerHTML = user.user
// })

// console.log(user)
