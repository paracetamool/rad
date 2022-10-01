Chart.plugins.register({
    beforeDraw: function (chartInstance) {
        var ctx = chartInstance.chart.ctx;
        ctx.fillStyle = "white";
        ctx.fillRect(0, 0, chartInstance.chart.width, chartInstance.chart.height);
    }
});

var driver = {
    function: {
        charts: {
            hour_day: hourDayTrafficData,
            day_week: dayWeekTrafficData,
            day_month: dayMonthTrafficData,
            month_year: monthYearTrafficData,
            year: yearTrafficData,
        },
        run: function(link='all') {
            $('.chart-loading')
                .css('height', $('#charts canvas')[0].height + 40 + 'px')
                .addClass('active')
            if(link == 'all') for (var chart of Object.values(this.charts)) chart()
            else this.charts[link]()
            // console.log('run')
        },
    },
    datepicker: {
        options: {
            global: {
                defaultDate: new Date(), 
                toolbarPlacement: 'top',
                showTodayButton: true,
                showClear: true,
                showClose: true,
                locale: 'ru',
            },
            local: {
                hour_day: {
                    options: {minDate: '08/12/2019', maxDate: moment().endOf('day'), format: 'DD.MM.YYYY'}, 
                    mask: 'YYYY-MM-DD',
                },
                day_week: {
                    options: {minDate: moment('08/12/2019').startOf('isoWeek'), maxDate: moment().endOf('isoWeek'), calendarWeeks: true, format: 'DD.MM.YYYY, неделя W'}, 
                    mask: 'YYYY-[W]W',
                },
                day_month: {
                    options: {minDate: moment('08/12/2019').startOf('month'), maxDate: moment().endOf('month'), format: 'MMMM YYYY'}, 
                    mask: 'YYYY-MM',
                },
                month_year: {
                    options: {minDate: moment('08/12/2019').startOf('year'), maxDate: moment().endOf('year'), format: 'YYYY'}, 
                    mask: 'YYYY',
                },
            },
        },
        makeData: function () {
            if (!this.data) {
                this.data = {}
                for (var [dp, local] of Object.entries(this.options.local)) {
                    var options = Object.assign({}, this.options.global, local.options)
                    this.data[dp] = $(`#${dp} input`).datetimepicker(options)
                }
            }
        },
    },
    chart: {
        options: {
            global: {
                title: {
                    display: false,
                    fontSize: 14,
                    fontColor: '#000000',
                    padding: 15,
                    lineHeight: 0,
                },
                animation: {duration: 0},
                scales: {
                    xAxes: [{
                        ticks: {
                            fontStyle: 'bold',
                            fontColor: '#000000',
                        },
                    }],
                    yAxes: [{
                        ticks: {
                            min: 0,
                            fontStyle: 'bold',
                            fontColor: '#000000',
                            padding: 5,
                            callback: (value) => {
                                if (value % 1 === 0) {
                                    return value
                                }
                            },
                        },
                        gridLines: {
                            tickMarkLength: 4,
                        },
                    }],
                },
            },
            various: {
                type1: function() {
                    var options = driver.chart.options.global
                    options.title.text = 'Количество посещений сайта по часам'
                    options.legend = {display: true, position: 'bottom',}
                    options.tooltips = {
                        position: 'nearest',
                        mode: 'index',
                        filter: function (tooltipItem) {
                            return tooltipItem.yLabel != 0;
                        },
                        callbacks: {
                            footer: function(tooltipItems, data) {
                                var sum = 0;
                                tooltipItems.forEach(function(tooltipItem) {
                                    sum += data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
                                });
                                return 'Всего: ' + sum;
                            },
                        },
                    }
                    options.scales.xAxes[0].stacked = true
                    options.scales.yAxes[0].stacked = true
                    return options
                },
                type2: function() {
                    var options = driver.chart.options.global
                    options.title.text = 'Распределение'
                    options.legend = {display: false,}
                    options.tooltips = {
                        filter: (tooltipItem) => { return tooltipItem.xLabel != 0; },
                        callbacks: {
                            footer: (tooltipItems, data) => {
                                var sum = 0;
                                tooltipItems.forEach(function(tooltipItem) { sum += data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index] });
                                return 'Всего: ' + sum;
                            },
                        },
                    }
                    return options
                },
            },
            local: {
                hour_day: () => driver.chart.options.various.type1(),
                day_week: () => driver.chart.options.various.type1(),
                day_month: () => driver.chart.options.various.type1(),
                month_year: () => driver.chart.options.various.type1(),
                year: () => driver.chart.options.various.type2(),
            },
        },
        makeData: function () {
            if (!this.data) {
                this.data = {}
                for(var [chart, options] of Object.entries(this.options.local)){
                    this.data[chart] = new Chart($(`#${chart} canvas`), {type: 'bar',options: options()})
                }
            }
        },
    },
    table: {
        selector: '#users-list table',
        options: {
            processing: true,
            serverSide: true,
            ajax: {
                url: "/get_users_data/",
            },
            order: [
                [4, "desc"]
            ],
            pageLength: 10,
            lengthMenu: [
                [10, 25, 50, 100, -1],
                [10, 25, 50, 100, "Все"]
            ],
            scrollY: "300px",
            dom: "<'row'<'col-md-5'l><'col-md-3 select-org'><'custom-group'fB>>tip",
            buttons: [
                {
                    text: '<span class="fa fa-refresh" aria-hidden="true"></span>',
                    attr: {'class': 'btn-default refresh-icon',},
                    action: function ( e, dt, node, config ) {
                        dt.ajax.reload();
                    }
                },
            ],
            language: {
                url: "/static/DataTables/json/custom.json"
            },
            drawCallback: function (settings) {
                var $paginator = $(this).closest('.dataTables_wrapper').find('.dataTables_paginate'),
                    pg = (...arr) => {var o = ['opacity']; o.push(...arr); return $paginator.css(...o)}
                if(!(this.api().page.info().pages - 1) && !!+pg()) pg(0)
                if(!!(this.api().page.info().pages - 1) && !+pg()) pg(1)
            },
            initComplete: function(settings, json) {
                var $select = $('<select/>', {class: 'selectpicker', title: 'Выберите организацию', multiple: true,}),
                    column = this.api().columns(3)
                for(opt of json.adds.orgList) $select.append(`<option />${opt}`)
                $select.prependTo('#users-list .select-org')
                $select.selectpicker()
                $select.on('changed.bs.select', function() {column.search($(this).val()).draw()})
            },
        },
            makeData: function () {if (!this.data) this.data = $(this.selector).DataTable(this.options)},
    },
    activePanel: () => $('.tab-content .active').attr('id'),
    value: function (label = false) {
        dp = label ? label : this.activePanel()
        date = this.datepicker.data[dp].data().DateTimePicker.date()._d
        return moment(date).format(this.datepicker.options.local[dp].mask)
    },
}

function barStackedData(labels, keys, data, colors) {
    var datasets = [];
    data.forEach((item, i) => {
        datasets.push({
            label: keys[i],
            data: item,
            backgroundColor: colors[i],
            borderColor: colors[i],
        });
    });
    return {labels: labels, datasets: datasets};
};

function barData(labels, values, colors) {
    var datasets = [{
        label: '',
        data: values,
        backgroundColor: colors,
        borderColor: colors,
        hoverBorderWidth: 1,
        hoverBorderColor: '#000'
    }];
    return {labels: labels, datasets: datasets};
};

function init() {
    for (var obj of ['chart', 'datepicker', 'table']) driver[obj].makeData()
    driver.function.run()
    $('.nav.nav-tabs>li:first-child').addClass('active')
    $('.tab-content>div:first-child').addClass('active in')
    $('#year [name="datepicker"]').parent().remove()

    eventsInit = [
        ['input', '[name="user_type"]'],
        ['click', '[name="refresh_btn"]'],
        ['dp.change', '[name="datepicker"]'],
    ]
    for([type, selector] of eventsInit) {
        $(document).on(type, selector, function () {
            type = $(this).parents('.tab-pane').attr('id')
            driver.function.run(type)
        })
    }
    $(document).on('dp.show.update', '#day_week [name="datepicker"]', function () {
        var $s = $(this).next()
        $s.find('td.day.active').removeClass('active').parent().find('.cw').addClass('active')
        $s.find('td.disabled:nth-child(2)').removeClass('active').parent().find('.cw').addClass('disabled')
    })
}

// TODO: Схлопнуть функции. Перевести по возможности в json
function hourDayTrafficData() {
    var label = 'hour_day',
        data = {
            'select_type_date': label,
            'input_date': driver.value(label),
            'select_type_user': $(`#${label} [name="user_type"]`).val(),
        },
        chart = driver.chart.data[label]
    $.ajax({
        method: "GET",
        url: '/get_traffic_data/',
        data: data,
        dataType: 'json',
        success: (response) => {
            var x_values = response.labels,
            keys = [],
            y_values = [],
            colors = [];
            for (key in response.dict_stacked) {
                keys.push(key);
                y_values.push(response.dict_stacked[key][0]);
                colors.push(response.dict_stacked[key][1])
            };
            chart.data = barStackedData(x_values, keys, y_values, colors);
            chart.update();
            $('.chart-loading').removeClass('active');
        },
    });
};

function dayWeekTrafficData() {
    var label = 'day_week',
        data = {
            'select_type_date': label,
            'input_date': driver.value(label),
            'select_type_user': $(`#${label} [name="user_type"]`).val(),
        },
        chart = driver.chart.data[label]
    $.ajax({
        method: "GET",
        url: '/get_traffic_data/',
        data: data,
        dataType: 'json',
        success: (response) => {
            var x_values = response.labels,
            keys = [],
            y_values = [],
            colors = [];
            for (key in response.dict_stacked) {
                keys.push(key);
                y_values.push(response.dict_stacked[key][0]);
                colors.push(response.dict_stacked[key][1])
            };
            chart.data = barStackedData(x_values, keys, y_values, colors);
            chart.update();
            $('.chart-loading').removeClass('active');
        },
    });
};

function dayMonthTrafficData() {
    var label = 'day_month',
        data = {
            'select_type_date': label,
            'input_date': driver.value(label),
            'select_type_user': $(`#${label} [name="user_type"]`).val(),
        },
        chart = driver.chart.data[label]
    $.ajax({
        method: "GET",
        url: '/get_traffic_data/',
        data: data,
        dataType: 'json',
        success: (response) => {
            var x_values = response.labels,
            keys = [],
            y_values = [],
            colors = []
            for (key in response.dict_stacked) {
                keys.push(key);
                y_values.push(response.dict_stacked[key][0]);
                colors.push(response.dict_stacked[key][1])
            }
            chart.data = barStackedData(x_values, keys, y_values, colors)
            chart.update()
            $('.chart-loading').removeClass('active')
        },
    });
};

function monthYearTrafficData() {
    var label = 'month_year',
        data = {
            'select_type_date': label,
            'input_date': driver.value(label),
            'select_type_user': $(`#${label} [name="user_type"]`).val(),
        },
        chart = driver.chart.data[label]
    $.ajax({
        method: "GET",
        url: '/get_traffic_data/',
        data: data,
        dataType: 'json',
        success: (response) => {
            var x_values = response.labels,
            keys = [],
            y_values = [],
            colors = [];
            for (key in response.dict_stacked) {
                keys.push(key);
                y_values.push(response.dict_stacked[key][0]);
                colors.push(response.dict_stacked[key][1])
            };
            chart.data = barStackedData(x_values, keys, y_values, colors);
            chart.update();
            $('.chart-loading').removeClass('active')
        },
    });
};

function yearTrafficData() {
    var label = 'year',
        data = {
            'select_type_date': label,
            'select_type_user': $(`#${label} [name="user_type"]`).val(),
        },
        chart = driver.chart.data[label]
    $.ajax({
        method: "GET",
        url: '/get_traffic_data/',
        data: data,
        dataType: 'json',
        success: (response) => {
            var labels = [],
            data = [],
            colors = [];
            for (var key in response) {
                labels.push(key);
                data.push(response[key][0]);
                colors.push(response[key][1])
            };
            chart.data = barData(labels, data, colors);
            chart.update();
            $('.chart-loading').removeClass('active')
        },
    });
};

function getUsersData() {
    $('.ajax-loader.users-activity').show();
    $.ajax({
        method: "GET",
        url: '/get_users_data/',
        data: {
            'select_org': $('#users-list [name="users_org"]').val(),
        },
        dataType: 'json',
        success: (response) => {
            var bodyHtml = '',
                yes_no = b => {
                    var icon = ['icon-yes', 'icon-no'][+b], alt = ['True', 'False'][+b], title = ['В сети', 'Вне сети'][+b];
                    return `<img src="/static/admin/img/${icon}.svg" alt=${alt} title=${title}>`
                }
            if(!$('table tbody').length) $('table').append('<tbody></tbody>')
            $('table tbody').children().remove();
            for (var key in response) bodyHtml += `
            <tr>
                <td><a href="/admin/auth/user/${response[key][0]}/change/">${key}</a></td>
                <td>${response[key][1]}</td>
                <td>${response[key][2]}</td>
                <td>${response[key][3]}</td>
                <td>${yes_no(response[key][4])}</td>
            </tr>`;
            $('table tbody').append(bodyHtml);
            $('.ajax-loader.users-activity').hide();
        },
    });
};

$(document).on('change', '#users-list [name="users_org"]', () => { getUsersData() });
$(document).on('change', '#users-list [name="refresh"]', () => { getUsersData() });

$(document).ready(() => init())