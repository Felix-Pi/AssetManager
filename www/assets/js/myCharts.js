colors = {
    pink: 'rgb(207,43,89)',
    red: 'rgb(248,117,109)',
    orange: 'rgb(255,159,64)',
    yellow: 'rgb(255, 205, 86)',
    lightgreen: 'rgb(0,208,127)',
    green: 'rgb(0,152,77)',
    teal: 'rgb(75, 192, 192)',
    blue: 'rgb(54, 162, 235)',
    darkblue: 'rgb(77,89,128)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(201, 203, 207)'
};

window.randomScalingFactor = function () {
    return Math.random(1, 500)
};

function get_random_color(amount) {
    let bgcolors = [];
    var keys = Object.keys(colors);
    for (let i = 0; i < amount; ++i) {
        bgcolors.push(colors[keys[i % keys.length]]);
    }
    return bgcolors;
}

function chart_doughnut(id, title, data, labels, label_suffix, width, height) {
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

    let color = get_random_color(input.length);

    console.log('input', input)

    var datasets = []
    for (let i = 0; i < input.length; i++) {
        datasets.push({
            backgroundColor: color[i],
            borderColor: color[i],
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

function draw_stacked_recommendation_bar_chart(id, title, input, width, height) {
    var colors_ = [colors.red, colors.orange, colors.teal, colors.blue, colors.green];

    var datasets = [];
    var data = []
    var keys = Object.keys(input[0]);
    for (let j = 1; j < keys.length; j++) {
        data[j] = []
        for (let i = 0; i < input.length; i++) {
            console.log(input[i][keys[j]])
            data[j].push(input[i][keys[j]])
        }

        datasets.push({
            label: keys[j],
            data: data[j],
            backgroundColor: colors_[j - 1]
        })
    }

    var barChartData = {
        labels: ['now', '-1m', '-2m', '-3m', '-4m'],
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

    console.log(data_line, data_label)

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
