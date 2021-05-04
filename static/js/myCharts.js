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
    var colors = get_color_sheme(data);

    var config = {
        type: 'doughnut',
        data: {
            datasets: [{
                data: data.data,
                backgroundColor: colors,
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
                position: 'right'
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
            },
            myCustomOptions: {},
        },
    };


    return insert_chart(id, title, config, label_suffix, width, height);
}

function chart_half_doughnut(id, title, data, label_suffix, width, height) {
    let chart = chart_doughnut(id, title, data, label_suffix, width, height);

    chart.options.isHalfDoughnut = true;
    chart.options.circumference = Math.PI;
    chart.options.rotation = -Math.PI;
    chart.options.borderWidth = 0;
    chart.options.cutoutPercentage = 65;
    chart.update();

    return chart;
}

function chart_linechart(id, title, input, label_suffix, width = '', height = '') {
    var colors = get_color_sheme(input);
    var datasets = [{
        backgroundColor: colors,
        borderColor: colors,
        label: '',
        data: [],
        lineTension: 0,
        borderWidth: 2,
        fill: false
    }]
    var labels = []

    //in case of empty input
    if (input.length > 0) {
        labels = input[0].labels
        // title = input[0].title
    }


    for (let i = 0; i < input.length; i++) {
        datasets.push({
            backgroundColor: colors[i],
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
            labels: labels,
            datasets: datasets
        },
        options: {
            plugins: {},
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
                        display: false,
                        labelString: 'Date'
                    }
                }],
                yAxes: [{
                    beginAtZero: true,
                    display: true,
                    scaleLabel: {
                        display: false,
                        labelString: 'Value'
                    }
                }]
            },
            myCustomOptions: {},
        }

    };
    return insert_chart(id, title, config, label_suffix, width, height);
}

function bar_chart(id, title, input, label_suffix, width, height) {
    var colors = get_color_sheme(input);

    var barChartData = {
        labels: input.labels,
        datasets: [{
            label: 'Stocks',
            data: input.data,
            backgroundColor: colors,
        }],
    };
    var config = {
        type: 'bar',
        data: barChartData,
        options: {
            title: {
                display: false,
            },
            tooltips: {
                mode: 'index',
                intersect: false,
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
            },
            legend: {
                display: false,
            },
            responsive: true,
            scales: {
                xAxes: [{
                    stacked: true,
                    display: false,
                }],
                yAxes: [{
                    stacked: true,
                }]
            },
            myCustomOptions: {},
        }
    }
    return insert_chart(id, title, config, label_suffix, width, height);

}

function draw_stacked_recommendation_bar_chart(id, title, input, label_suffix = '', width, height) {
    var colors_ = [colors.red, colors.orange, colors.grey, colors.blue, colors.blue_light];
    input_data = input.data

    var datasets = [];
    var data = []
    var keys = Object.keys(input_data[0]);


    for (let j = 0; j < keys.length; j++) {
        data[j] = []
        for (let i = 0; i < input_data.length; i++) {
            data[j].push(input_data[i][keys[j]])
        }
        datasets.push({
            label: keys[j],
            data: data[j],
            backgroundColor: colors_[j]
        })
    }


    var barChartData = {
        //labels: ['now', '-1m', '-2m', '-3m', '-4m'],
        labels: input.labels,
        datasets: datasets
    };
    var config = {
        type: 'horizontalBar',
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
            scales: {
                xAxes: [{
                    stacked: true,
                }],
                yAxes: [{
                    stacked: true
                }]
            },
            myCustomOptions: {},
        }
    }
    return insert_chart(id, title, config, label_suffix, width, height)

}

function draw_candle_bar_chart(id, title, input, label_suffix = '') {
    if (input.length > 0) {

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
            },
            options: {
                myCustomOptions: {},
            }
        }

    }

    return insert_chart(id, title, config, label_suffix);
}

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

//if input.colored = true: multiple colors
//if input.colored = false: one colors
function get_color_sheme(input) {
    if (input.colored === true) {
        var colors = get_random_color(input.data.length);
    } else {
        var colors = chartcolors.blue_light;
    }
    return colors;
}

function change_chart_type(chart) {
    let types = ['bar', 'doughnut', 'pie'];
    let canvas_id = chart.canvas.id;
    let chart_id = canvas_id.replace('_canvas', '');
    let parent_id = chart.canvas.offsetParent;
    let label_suffix = $(parent_id).attr('label-suffix');
    let body_elem = $(parent_id).find('.card-body');
    let current_type = chart.config.type;
    let isHalfDoughnut = chart.options.isHalfDoughnut;

    let title = $(chart_id + ' .card-header span').text();
    let width = chart.config.options.myCustomOptions.width;
    let height = chart.config.options.myCustomOptions.height;

    let input = {'data': chart.data.datasets[0].data, 'labels': chart.data.labels, 'colored': true}

    body_elem.html("");
    chart.destroy();


    if (current_type === types[0]) {
        if (isHalfDoughnut) {
            new_chart = chart_half_doughnut(chart_id, title, input, label_suffix, width, height);

        } else {
            new_chart = chart_doughnut(chart_id, title, input, label_suffix, width, height);
        }

    }

    if (current_type === types[1]) {
        new_chart = bar_chart(chart_id, title, input, label_suffix, width, height);
    }

    if (current_type === types[3]) {
        //return pie_chart(chart_id, title, input, '') //ToDO
    }

    new_chart.options.isHalfDoughnut = isHalfDoughnut;

    return new_chart;
}

function get_instance_from_id(id) {
    Chart.helpers.each(Chart.instances, function (instance) {
        if (instance.canvas.id === id) {
            result = instance;
        }
    });

    return result;
}

function insert_chart(id, title, config, label_suffix = '', width = 'auto', height = 300) {
    let header_elem = $(id + ' .card-header')
    let settings_change_chart_elem = $(id + ' .settings .change_chart_type')

    $(id).attr('label-suffix', label_suffix);


    if (title.includes('~')) {
        let description = title.split('~')[1]
        title = title.split('~')[0]
        header_elem.find('.description').html(description);
    }
    header_elem.find('span').text(title);

    if (settings_change_chart_elem.length > 0) {
        settings_change_chart_elem.attr('chart-type', config.type)

        if (config.type === 'doughnut') { //ToDo: move somewhere else
            settings_change_chart_elem.find('i').removeClass('fa-chart-bar').addClass('fa-chart-pie');
        }
    }

    set_loader_inactive($(id + ' .card-body'))
    $(id + ' .card-body').prepend('<canvas id="' + id + '_canvas" width="' + width + '" height="' + height + '"></canvas>');


    config.options.myCustomOptions.width = width;
    config.options.myCustomOptions.height = height;


    var ctx = document.getElementById(id + '_canvas').getContext('2d');
    return new Chart(ctx, config);
}

function enable_xaxis_label(chart) {
    chart.config.options.scales.xAxes[0].display = false;
    chart.update();
}


function update_chart(chart, data, labels) { //ToDo

    console.log('data: ', data)
    if (chart.data.datasets.length === 0) {
        chart.data.datasets = [{data: []}];
    } else {
        chart.data.datasets = [chart.data.datasets[0]];
    }

    chart.data.datasets[0].data = data;
    chart.data.labels = labels;
    chart.update();
}