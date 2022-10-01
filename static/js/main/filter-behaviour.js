var filterSelected = {
    'mtu' : [],
    'org' : [],
    'tip' : [],
    'ust' : [],
    'exp' : [],
    'kat' : [],
    'nep' : [],
    'kor' : [],
    'ines': [],
    'ind' : [],
    'krit': [],
};

$('select:not(#id_select_1, #id_select_2, #id_select_quarter)').on('changed.bs.select', function() { filterBehaviour(this.id.split('id_select_')[1]) });

function getFiltersData() {
    for (var key in filterSelected) filterSelected[key] = [];
    $.ajax({
        method: 'GET',
        url: '/rr/get_filters_data/',
        data: {'mode': window.location.pathname.includes('search_violations') ? 'violations' : window.location.pathname.includes('search_annual_reports') ? 'selfassessment' : $('.nav-pills li.active a').attr('data-mode')},
        dataType: 'json',
        success: (response) => {
            if (window.location.pathname.includes('summary')) {
                $('select').each((i, el) => { $(el).parents(':eq(1)').hide() });
                $('#filters-actived div:not(#id_div_data_start, #id_div_data_end, #id_div_select_quarter)').remove();
                $('#id_div_data_start, #id_div_data_end, #id_div_select_quarter').hide();
            };
            for (var key in response) {
                $('#id_select_' + key + ' option').remove();
                response[key].forEach((item) => {
                    $('#id_select_' + key).append('<option value="' + item + '">' + item + '</option>');
                    if ((window.location.pathname.includes('search')) && (key in list_data)) list_data[key].push(item);
                    else if (window.location.pathname.includes('summary')) { $('#id_select_' + key).parents(':eq(1)').show(); $('#filters-actived').append(`<div id="id_div_${item.replace(/[\s.,%/,{()}]/g, '')}" class="filter-divs">${item}<i class="fa fa-times" aria-hidden="true" onclick="closeFilterItem('${key}', '${item}');"></i></div>`) };
                });
                $('#id_select_' + key).selectpicker('refresh');
            };
            if (window.location.pathname.includes('summary')) {
                ['#id_input_data_start', '#id_input_data_end'].forEach((el) => { $(el).data('DateTimePicker').date(null).format(mode == 'violations' ? 'DD.MM.YYYY' : 'YYYY'); $(el).mask(mode == 'violations' ? "00.00.0000" : "0000", mode == 'violations' ? dateMaskOpt1 : dateMaskOpt2); });
                if (mode == 'violations') $('#id_select_quarter').parents(':eq(1)').show();
                else { $('#id_select_mtu ~ [role="combobox"] a').click(); $('#id_button_filter').click() }
            };
            $('#id_select_quarter').parents(':eq(1)').show();
        },
    });
};

function filterBehaviour(selection) {
    for (key in filterSelected) if (key != 'mode') filterSelected[key].forEach((item) => {$("#id_div_" + item.replace(/[\s.,%/,{()}]/g, '')).hide()});
    $('#id_div_data_start, #id_div_data_end, #id_div_select_quarter').hide();
    filterSelected[selection] = $('#id_select_' + selection).val();
    filterSelected['mode'] = window.location.pathname.includes('search_violations') ? 'violations' : window.location.pathname.includes('search_annual_reports') ? 'selfassessment' : $('.nav-pills li.active a').attr('data-mode');
    if (filterSelected['mode'] == 'violations' || window.location.pathname.includes('search_annual_reports')) {
        $.ajax({
            method: "GET",
            url: "/rr/update_filters_data/",
            data: filterSelected,
            dataType: 'json',
            success: (response) => {
                for (key in response) {
                    $('#id_select_' + key + ' option').prop('disabled', true);
                    response[key].forEach((item) => { $('#id_select_' + key + ' option[value="' + item + '"]').prop('disabled', false) });
                    $('#id_select_' + key).selectpicker('refresh');
                };
            },
        });
    };
};
