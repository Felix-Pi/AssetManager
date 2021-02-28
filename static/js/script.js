var colors = ['rgb(255, 99, 132)',
    'rgb(255, 159, 64)',
    'rgb(255, 205, 86)',
    'rgb(75, 192, 192)',
    'rgb(54, 162, 235)',
    'rgb(153, 102, 255)',
    'rgb(201, 203, 207)'
];

window.randomScalingFactor = function () {
    return Math.random(1, 500)
};

function get_random_color(amount) {
    let bgcolors = [];
    for (let i = 0; i < amount; ++i) bgcolors.push(colors[i % colors.length]);
    return bgcolors;
}

function chart_doughnut(id, title, data, labels) {
    var config = {
        type: 'doughnut',
        data: {
            datasets: [{
                data: data,
                backgroundColor: get_random_color(data.length),
                label: 'Dataset 1'
            }],
            labels: labels
        },
        options: {
            parsing: {
                xAxisKey: 'value',
                yAxisKey: 'symbol'
            },
            responsive: true,
            title: {
                display: true,
                text: title
            },
            animation: {
                animateScale: true,
                animateRotate: true
            },
            legend: {
                position: "right"
            },
            plugins: {
                datalabels: {
                    display: true,
                    align: 'bottom',
                    backgroundColor: '#ccc',
                    borderRadius: 3,
                    font: {
                        size: 18,
                    }
                },
            }

        }
    };

    var ctx = document.getElementById(id).getContext('2d');
    window.id = new Chart(ctx, config);
}


function chart_linechart(id, data, labels) {
    data[0] = [
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor()
    ]
    data[1] = [
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor(),
        randomScalingFactor()
    ]


    var lineChartData = {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [{
            label: 'My First dataset',
            borderColor: colors[0],
            backgroundColor: colors[0],
            fill: false,
            data: data[0],
            yAxisID: 'y-axis-1',
        }, {
            label: 'My Second dataset',
            borderColor: colors[1],
            backgroundColor: colors[1],
            fill: false,
            data: data[1],
            yAxisID: 'y-axis-2'
        }]
    };


    var config = {
        type: 'line',
        data: lineChartData,
        options: {
            responsive: true,
            hoverMode: 'index',
            stacked: false,
            title: {
                display: true,
                text: 'Chart.js Line Chart - Multi Axis'
            },
            scales: {
                yAxes: [{
                    type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
                    display: true,
                    position: 'left',
                    id: 'y-axis-1',
                }, {
                    type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
                    display: true,
                    position: 'right',
                    id: 'y-axis-2',

                    // grid line settings
                    gridLines: {
                        drawOnChartArea: false, // only want the grid lines for one axis to show up
                    },
                }],
            }
        }
    }
    var ctx = document.getElementById(id).getContext('2d');
    window.myLine = new Chart(ctx, config);


}




function test() {

}
$(document).ready(function () {






});
