colors = {
    lightgreen: 'rgb(0,208,127)',
    green: 'rgb(3,117,63)',
    teal: 'rgb(75, 192, 192)',
    grey: 'rgb(201, 203, 207)',
    red_dark: 'rgb(160,0,48)',
};

chartcolors = {
    yellow: 'rgb(243,169,60)',
    orange: 'rgb(239,130,80)',
    red: 'rgb(229,102,108)',
    pink: 'rgb(192,88,131)',
    purple: 'rgb(144,83,141)',
    purple_dark: 'rgb(91,78,134)',
    blue: 'rgb(46,69,112)',
    blue_dark: 'rgb(20,55,80)',
    blue_light: 'rgb(84,161,229)',
};
colors = Object.assign({}, colors, chartcolors);

window.randomScalingFactor = function () {
    return Math.random(1, 500)
};

function get_random_color(amount) {
    let bgcolors = [];
    var keys = Object.keys(chartcolors);
    for (let i = 0; i < amount; ++i) {
        bgcolors.push(chartcolors[keys[i % keys.length]]);
    }
    return bgcolors;
}

function chart_doughnut(id, title, data, label_suffix, width, height) {
    var config = {
        type: 'doughnut',
        data: {
            datasets: [{
                data: data.data,
                backgroundColor: get_random_color(data.data.length),
                label: 'Dataset 1'
            }],
            labels: data.labels
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            title: {
                display: false,
            },
            animation: {
                animateScale: false,
                animateRotate: true
            },
            legend: {
                display: false,
            },
            tooltips: {
                callbacks: {
                    label: function (item, data) {

                        let index = item.index;
                        let symbol = data.labels[index];
                        let value = data.datasets[0].data[index];
                        let parsed_value = parseFloat(value);
                        let formatted_value = parsed_value.toFixed(2);

                        return ' ' + symbol + ': ' + formatted_value + ' ' + label_suffix
                    }
                }
            }
        }
    };


    $(id + ' .card-header').text(title);
    $(id + ' .card-body').prepend('<canvas id="' + id + '_canvas" width="' + width + '" height="' + height + '"></canvas>');


    var ctx = document.getElementById(id + '_canvas').getContext('2d');
    return new Chart(ctx, config);
}

function chart_linechart(id, title, input, label_suffix) {
    Chart.controllers.LineWithLine = Chart.controllers.line.extend({
        draw: function (ease) {
            Chart.controllers.line.prototype.draw.call(this, ease);

            if (this.chart.tooltip._active && this.chart.tooltip._active.length) {
                var activePoint = this.chart.tooltip._active[0],
                    ctx = this.chart.ctx,
                    x = activePoint.tooltipPosition().x,
                    topY = this.chart.legend.bottom,
                    bottomY = this.chart.chartArea.bottom;

                // draw line
                ctx.save();
                ctx.beginPath();
                ctx.moveTo(x, topY);
                ctx.lineTo(x, bottomY);
                ctx.lineWidth = 1;
                ctx.strokeStyle = '#aba8a8';
                ctx.stroke();
                ctx.restore();
            }
        }
    });


    if (input.length > 1) {
        var color = get_random_color(input.length);
    } else {
        var color = [colors.blue];
    }

    var datasets = []
    for (let i = 0; i < input.length; i++) {
        datasets.push({
            backgroundColor: color[i],
            //borderColor: color[i],
            borderColor: chartcolors.blue_light,
            label: input[i].title,
            data: input[i].median,
            lineTension: 0,
            borderWidth: 2,
            fill: false
        })
    }


    var config = {
        type: 'LineWithLine',
        data: {
            labels: input[0].timestamps,
            datasets: datasets
        },
        options: {
            responsive: true,
            bezierCurve: false,
            title: {
                display: false,
            },
            elements: {
                point: {
                    radius: 0
                }
            },
            tooltips: {
                mode: 'index',
                intersect: false,
                callbacks: {
                    title: function (item, data) {
                        return item[0].xLabel
                    },
                    label: function (item, data) {
                        let symbol = data.datasets[0].label
                        //let value = item.yLabel.toFixed(2)
                        let value = item.yLabel.toLocaleString('en-US', {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 5
                        })


                        return symbol + ': ' + value + ' ' + label_suffix
                    }
                }
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            legend: {
                display: false,
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Date'
                    }
                }],
                yAxes: [{
                    beginAtZero: true,
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Value'
                    }
                }]
            }
        }

    };
    $(id + ' .card-header').text(input[0].title);
    $(id + ' .card-body').prepend('<canvas id="' + id + '_canvas"></canvas>');

    var ctx = document.getElementById(id + '_canvas').getContext('2d');
    return new Chart(ctx, config);
}

function draw_bar_chart(id, title, input, width, height) {

    var barChartData = {
        labels: input.labels,
        datasets: [{
            label: 'Stocks',
            data: input.data,
            //backgroundColor: get_random_color(input.data.length)
            backgroundColor: colors.blue_light
        }],
    };
    config = {
        type: 'bar',
        data: barChartData,
        options: {
            title: {
                display: false,
            },
            tooltips: {
                mode: 'index',
                intersect: false
            },
            legend: {
                display: false,
            },
            responsive: true,
            scales: {
                xAxes: [{
                    stacked: true,
                }],
                yAxes: [{
                    stacked: true
                }]
            }
        }
    }
    $(id + ' .card-header').text(title);
    $(id + ' .card-body').prepend('<canvas id="' + id + '_canvas" width="' + width + '" height="' + height + '"></canvas>');


    var ctx = document.getElementById(id + '_canvas').getContext('2d');
    return new Chart(ctx, config);

}

function draw_stacked_recommendation_bar_chart(id, title, input, width, height) {
    var colors_ = [colors.red_dark, colors.orange, colors.teal, colors.blue, colors.green];
    input_data = input.data

    var datasets = [];
    var data = []
    var keys = Object.keys(input_data[0]);


    for (let j = 1; j < keys.length; j++) {
        data[j] = []
        for (let i = 0; i < input_data.length; i++) {
            data[j].push(input_data[i][keys[j]])
        }
        datasets.push({
            label: keys[j],
            data: data[j],
            backgroundColor: colors_[j - 1]
        })
    }


    var barChartData = {
        //labels: ['now', '-1m', '-2m', '-3m', '-4m'],
        labels: input.labels,
        datasets: datasets
    };
    config = {
        type: 'bar',
        data: barChartData,
        options: {
            title: {
                display: false,
                text: 'Chart.js Bar Chart - Stacked'
            },
            tooltips: {
                mode: 'index',
                intersect: false
            },
            legend: {
                display: false,
            },
            responsive: true,
            scales: {
                xAxes: [{
                    stacked: true,
                }],
                yAxes: [{
                    stacked: true
                }]
            }
        }
    }
    $(id + ' .card-header').text(title);
    $(id + ' .card-body').prepend('<canvas id="' + id + '_canvas" width="' + width + '" height="' + height + '"></canvas>');


    var ctx = document.getElementById(id + '_canvas').getContext('2d');
    return new Chart(ctx, config);

}

function draw_candle_bar_chart(id, title, input) {
    let data = []
    for (let i = 0; i < input[0].median.length; i++) {
        data.push({
                t: input[0].timestamps_raw[i] * 1000, //time
                o: input[0].open[i], //open
                h: input[0].high[i], //high
                l: input[0].low[i], //low
                c: input[0].close[i], //close
                m: input[0].median[i], //median
            }
        )
    }


    let data_line = []
    let data_label = []

    for (let i = 0; i < data.length; i++) {
        data_line.push(data[i].m)
        data_label.push(data[i].t)
    }


    var config = {
        type: 'candlestick',
        data: {
            labels: data_label,
            datasets: [{
                label: title,
                data: data
            }]
        }
    }


    $(id + ' .card-header').text(title);
    $(id + ' .card-body').prepend('<canvas id="' + id + '_canvas"></canvas>');

    var ctx = document.getElementById(id + '_canvas').getContext('2d');
    return new Chart(ctx, config);
}