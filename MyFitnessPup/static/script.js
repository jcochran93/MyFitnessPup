TESTER = document.getElementById('tester');

fetch('/weight')
.then(res => res.json())
.then(weightHistory => {
    
    var dates = Object.keys(weightHistory.weight);
    var pounds = Object.values(weightHistory.weight)
    
    var data = [{
        type: "line",
        y: pounds,
        x: dates
        }];

    var layout = {xaxis: {type: 'date'}, 
                xaxis: {
                    linecolor: 'black',
                    linewidth: 2,
                    mirror: true
                },
                yaxis: {
                    linecolor: 'black',
                    linewidth: 2,
                    mirror: true
                },
                margin: {b: 40,
                         t: 20,
                         l: 40,
                         r:40},
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)' };

    var config = {staticPlot: true}

    Plotly.newPlot(TESTER, data, layout, config);
})

/* Set date input for weight logging
    to today by default */

var defaultDate = document.querySelector('input[type="date"]');
let currentDate = new Date()
let today = currentDate.toISOString().slice(0, 10)

defaultDate.value = today
/* ----------- */

/*Set date for meal tracking to today by default */
let dateDisplay = document.querySelector('[data-date]')

dateDisplay.innerHTML = currentDate.toLocaleDateString()
/* ----------- */


/* Change Date when buttons are clicked */

let prevDay = document.querySelector('[data-prev-day]')

let nextDay = document.querySelector('[data-next-day]')

prevDay.addEventListener('click', evt => {

    currentDate.setDate(currentDate.getDate() -1);
    // dateDisplay.innerHTML = tomorrow.toISOString().slice(0, 10);
    dateDisplay.innerHTML = currentDate.toLocaleDateString();

    fetch('/date', {
        method: 'POST',
        headers: {
          'Accept': 'application/json, text/plain, */*',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({date: currentDate.toISOString()})
      }).then(res => res.json())
        .then(res => console.log(res));
    }
)

nextDay.addEventListener('click', evt => {
    
    currentDate.setDate(currentDate.getDate() +1);
    // dateDisplay.innerHTML = tomorrow.toISOString().slice(0, 10);
    dateDisplay.innerHTML = currentDate.toLocaleDateString()

    fetch('/date', {
        method: 'POST',
        headers: {
          'Accept': 'application/json, text/plain, */*',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({date: currentDate.toISOString()})
      }).then(res => res.json())
        .then(res => console.log(res));
    
    
    }
)
/* ----------- */
