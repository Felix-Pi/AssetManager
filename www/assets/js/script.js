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
            responsive: true,
            title: {
                display: false,
            },
            animation: {
                animateScale: true,
                animateRotate: true
            },
            legend: {
                display: false,
            },
        }
    };


    $(id + ' .card-header').text(title);
    $(id + ' .card-body').html('<canvas id="' + id + '_canvas"></canvas>');

    var ctx = document.getElementById(id + '_canvas').getContext('2d');
    window.id = new Chart(ctx, config);


}


function chart_linechart(id, title, data, labels) {
    console.log('chart_linechart id', id)
    console.log('chart_linechart data', data)
    console.log('chart_linechart labels', labels)


    unit = $(id + " .unit").val()
    console.log(unit)

    data_final = []
    labels_final = []

    for (let i = 0; i < 3; i++) {
        label = labels[i]

        console.log(label)
        console.log(Date.parse(label))

        if (i % 5 == 0) {
            data_final.push(data[i])
            labels_final.push(labels[i])
        }
    }

    console.log(data.length)

    color = get_random_color(data.length);
    var lineChartData = {
        labels: labels_final,
        datasets: [{
            label: title,
            borderColor: colors[0],
            backgroundColor: colors[0],
            fill: false,
            data: data_final,
            yAxisID: 'y-axis-1',
            cubicInterpolationMode: 'monotone'

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
                display: false,
            },
            legend: {
                display: false,
            },
            scales: {
                yAxes: [{
                    display: true,
                    position: 'left',
                    id: 'y-axis-1',
                }],
            }
        }
    }

    $(id + ' .card-header').text(title);
    $(id + ' .card-body').html('<canvas id="' + id + '_canvas"></canvas>');

    var ctx = document.getElementById(id + '_canvas').getContext('2d');
    window.myLine = new Chart(ctx, config);


}



