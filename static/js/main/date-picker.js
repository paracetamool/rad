var datepickerOpt1 = {
    format          : 'DD.MM.YYYY',
    toolbarPlacement: 'top',
    showTodayButton : true,
    showClear       : true,
    showClose       : true,
    locale          : 'ru',
};

var datepickerOpt2 = {
    format          : 'YYYY',
    toolbarPlacement: 'top',
    showTodayButton : true,
    showClear       : true,
    showClose       : true,
    locale          : 'ru',
};

var dateMaskOpt1 = {
    placeholder  : "__.__.____",
    selectOnFocus: true,
};

var dateMaskOpt2 = {
    placeholder  : "год",
    selectOnFocus: true,
};




$('input[id^="id_input_data_"]').datetimepicker(window.location.pathname.includes('search_annual_reports') ? datepickerOpt2 : datepickerOpt1).mask(window.location.pathname.includes('search_annual_reports') ? "0000" : "00.00.0000", window.location.pathname.includes('search_annual_reports') ? dateMaskOpt2 : dateMaskOpt1);

$('input[id^="id_input_year_data_"]').datetimepicker(window.location.pathname.includes('search_annual_reports') ? datepickerOpt2 : datepickerOpt2).mask(window.location.pathname.includes('search_annual_reports') ? "0000" : "00.00.0000", window.location.pathname.includes('search_annual_reports') ? dateMaskOpt2 : dateMaskOpt2);


// -----------------------------------------------------------------------


$('#id_input_start_day').datetimepicker(window.location.pathname.includes('search_annual_reports') ? datepickerOpt2 : datepickerOpt1).mask(window.location.pathname.includes('search_annual_reports') ? "0000" : "00.00.0000", window.location.pathname.includes('search_annual_reports') ? dateMaskOpt2 : dateMaskOpt1);
$('#id_input_end_day').datetimepicker(window.location.pathname.includes('search_annual_reports') ? datepickerOpt2 : datepickerOpt1).mask(window.location.pathname.includes('search_annual_reports') ? "0000" : "00.00.0000", window.location.pathname.includes('search_annual_reports') ? dateMaskOpt2 : dateMaskOpt1);


$('#id_input_start_year').datetimepicker(window.location.pathname.includes('search_annual_reports') ? datepickerOpt2 : datepickerOpt2).mask(window.location.pathname.includes('search_annual_reports') ? "0000" : "00.00.0000", window.location.pathname.includes('search_annual_reports') ? dateMaskOpt2 : dateMaskOpt2);
$('#id_input_end_year').datetimepicker(window.location.pathname.includes('search_annual_reports') ? datepickerOpt2 : datepickerOpt2).mask(window.location.pathname.includes('search_annual_reports') ? "0000" : "00.00.0000", window.location.pathname.includes('search_annual_reports') ? dateMaskOpt2 : dateMaskOpt2);




// --------------------Для подробной даты------------------
$(document).on('dp.change', '#id_input_start_day', () => {
    if ($('#id_input_start_day').val() && new Date($('#id_input_start_day').val().split(".").reverse().join("-")) > new Date($('#id_input_end_day').val().split(".").reverse().join("-"))) {
        var data_start = $('#id_input_end_day').val(), data_end = $('#id_input_start_day').val();
        $('#id_input_start_day').val(data_start);
        $('#id_input_end_day').val(data_end);
    };
    if ($('#id_input_start_day').val()) {
        if($('#id_input_end_day').val()) $('#id_range').html('От: ' + $('#id_input_start_day').val() + ' до: ' + $('#id_input_end_day').val() + ($("#id_select_quarter").val() && $("#id_select_quarter").val() != '' ? ' (' + $("#id_select_quarter").val() + ')' : ''));
        else $('#id_range').html('От: ' + $('#id_input_start_day').val() + ($("#id_select_quarter").val() && $("#id_select_quarter").val() != '' ? ' (' + $("#id_select_quarter").val() + ')' : ''));
        $('#id_range').css('color', '#333');
    } else {
        if($('#id_input_end_day').val()) $('#id_range').html('До: ' + $('#id_input_end_day').val() + ($("#id_select_quarter").val() && $("#id_select_quarter").val() != '' ? ' (' + $("#id_select_quarter").val() + ')' : '')).css('color', '#333');
        else $('#id_range').html('Временной интервал').css('color', '#999');
    };
});

$(document).on('dp.change', '#id_input_end_day', () => {
    if ($("#id_input_start_day").val() && new Date($('#id_input_start_day').val().split(".").reverse().join("-")) > new Date($("#id_input_end_day").val().split(".").reverse().join("-"))) {
        var data_start = $("#id_input_end_day").val(), data_end = $("#id_input_start_day").val();
        $("#id_input_start_day").val(data_start);
        $('#id_input_end_day').val(data_end);
    };
    if($('#id_input_end_day').val()) {
        if($('#id_input_start_day').val()) $('#id_range').html('От: ' + $('#id_input_start_day').val() + ' до: ' + $('#id_input_end_day').val() + ($("#id_select_quarter").val() && $("#id_select_quarter").val() != '' ? ' (' + $("#id_select_quarter").val() + ')' : ''));
        else $('#id_range').html('До: ' + $('#id_input_end_day').val() + ($("#id_select_quarter").val() && $("#id_select_quarter").val() != '' ? ' (' + $("#id_select_quarter").val() + ')' : ''));
        $('#id_range').css('color', '#333');
    } else {
        if($('#id_input_start_day').val()) $('#id_range').html('От: ' + $('#id_input_start_day').val() + ($("#id_select_quarter").val() && $("#id_select_quarter").val() != '' ? ' (' + $("#id_select_quarter").val() + ')' : '')).css('color', '#333');
        else $('#id_range').html('Временной интервал').css('color', '#999');
    };
});


// --------------------Для годов------------------
$(document).on('dp.change', '#id_input_start_year', () => {
    if ($('#id_input_start_year').val() && new Date($('#id_input_start_year').val().split(".").reverse().join("-")) > new Date($('#id_input_end_year').val().split(".").reverse().join("-"))) {
        var data_start = $('#id_input_end_year').val(), data_end = $('#id_input_start_year').val();
        $('#id_input_start_year').val(data_start);
        $('#id_input_end_year').val(data_end);
    };
    if ($('#id_input_start_year').val()) {
        if($('#id_input_end_year').val()) $('#id_range').html('От: ' + $('#id_input_start_year').val() + ' до: ' + $('#id_input_end_year').val() + ($("#id_select_quarter").val() && $("#id_select_quarter").val() != '' ? ' (' + $("#id_select_quarter").val() + ')' : ''));
        else $('#id_range').html('От: ' + $('#id_input_start_year').val() + ($("#id_select_quarter").val() && $("#id_select_quarter").val() != '' ? ' (' + $("#id_select_quarter").val() + ')' : ''));
        $('#id_range').css('color', '#333');
    } else {
        if($('#id_input_end_year').val()) $('#id_range').html('До: ' + $('#id_input_end_year').val() + ($("#id_select_quarter").val() && $("#id_select_quarter").val() != '' ? ' (' + $("#id_select_quarter").val() + ')' : '')).css('color', '#333');
        else $('#id_range').html('Временной интервал').css('color', '#999');
    };
});

$(document).on('dp.change', '#id_input_end_year', () => {
    if ($("#id_input_start_year").val() && new Date($('#id_input_start_year').val().split(".").reverse().join("-")) > new Date($("#id_input_end_year").val().split(".").reverse().join("-"))) {
        var data_start = $("#id_input_end_year").val(), data_end = $("#id_input_start_year").val();
        $("#id_input_start_year").val(data_start);
        $('#id_input_end_year').val(data_end);
    };
    if($('#id_input_end_year').val()) {
        if($('#id_input_start_year').val()) $('#id_range').html('От: ' + $('#id_input_start_year').val() + ' до: ' + $('#id_input_end_year').val() + ($("#id_select_quarter").val() && $("#id_select_quarter").val() != '' ? ' (' + $("#id_select_quarter").val() + ')' : ''));
        else $('#id_range').html('До: ' + $('#id_input_end_year').val() + ($("#id_select_quarter").val() && $("#id_select_quarter").val() != '' ? ' (' + $("#id_select_quarter").val() + ')' : ''));
        $('#id_range').css('color', '#333');
    } else {
        if($('#id_input_start_year').val()) $('#id_range').html('От: ' + $('#id_input_start_year').val() + ($("#id_select_quarter").val() && $("#id_select_quarter").val() != '' ? ' (' + $("#id_select_quarter").val() + ')' : '')).css('color', '#333');
        else $('#id_range').html('Временной интервал').css('color', '#999');
    };
});



//-----------------------------------Запрет закрытия selectpicker в dropdown-menu---------------------------------------
//----------------------------------------(необходимо для id_select_quarter)--------------------------------------------

var selectpickerIsClicked = false;
$('.dropdown-menu').on('click', function(e) {
    if ($(e.target).closest('.bootstrap-select.open').is(':visible') || $(e.target).closest('.btn.dropdown-toggle.btn-default').is(':visible')) {
        selectpickerIsClicked = true;
    }
});

$('.dropdown').on('hide.bs.dropdown', function(e) {
    if (selectpickerIsClicked) {
        e.preventDefault();
        selectpickerIsClicked = false;
    }
});
