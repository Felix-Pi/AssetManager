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

function drawCandleBarChart(id, title, input) {
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

$(document).ready(function () {

    $('.ui.accordion').accordion();

    $(document).on('click', '#update_data', function (e, f) {
        $.ajax({
            method: "GET",
            url: "/api/refresh/",
            success: function (data) {
                console.log(data)
            }
        });
    });

    $(document).on('click', '.card .settings button', function (e, f) {
        elem = $(this)

        elem.parent().find('.active').removeClass('active');
        elem.addClass('active');

    });
    $(document).on('click', '.card .settings button', function (e, f) {
        elem = $(this)

        elem.parent().find('.active').removeClass('active');
        elem.addClass('active');

    });

    $(document).on('click', '.card .more', function (e, f) {
        elem = $(this)
        console.log('elemmm', elem.parent().parent().find('.card-footer'))
        elem.parent().parent().parent().find('.card-footer').slideToggle()

    });
    /*
    toggle profit label
     */

    $('.profit_label').each(function () {
        elem = $(this)
        profit_val = parseFloat(elem.text())

        elem_text = elem.find('.label').find('span')

        suffix = ' €'

        if (profit_val < 0) {
            profit_val = profit_val * (-1)
            elem_text.text('  ' + profit_val)
        }

        elem_text.append(suffix)
    });

    const zeroPad = (num, places) => String(num).padStart(places, '0')
    $(document).on('click', '.profit_label', function () {
        $('.profit_label').each(function () {
            let elem = $(this)

            let counter = parseInt(elem.attr('counter'))
            let content = elem.attr('data-val').split('~')

            if (counter < 1) {
                suffix = ' €'
            } else {
                suffix = ' %'
            }

            if (counter === content.length - 1) {
                counter = 0
                suffix = ' €'
            } else {
                counter += 1
            }


            let content_val = parseFloat(content[counter])
            content_val = zeroPad(content_val, 2)


            if (content_val > 0) {
                var color = 'green'
                var icon = 'fas fa-caret-up'
            } else {
                var color = 'red'
                var icon = 'fas fa-caret-down'
                content_val = content_val * (-1)
            }

            let target_elem = elem.find('.label')


            target_elem.removeClass('.red .green')
            target_elem.addClass(color)


            elem.attr('counter', counter)
            target_elem.html('<i class="' + icon + '"></i> ' + content_val + suffix)

            profit_label_titles = ['profit total', 'profit total', ' profit today', 'profit today']
            $('#profit_label_title').text(profit_label_titles[counter])

        });
    });
});


