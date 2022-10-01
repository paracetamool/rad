//--------------------------------Проверка input типа date и применение datepicker-------------------------------------
$("#id_new_date").datepicker($.datepicker.regional["ru"]);
$("#id_new_date_end").datepicker($.datepicker.regional["ru"]);
$("#id_input_data_start").datepicker($.datepicker.regional["ru"]);
$("#id_input_data_end").datepicker($.datepicker.regional["ru"]);
//----------------------------------Запрет закрытия selectpicker в dropdown-menu---------------------------------------
var selectpickerIsClicked = false;
$('.selectpicker').selectpicker({
    container: 'body',
    dropupAuto: false
});

$('.dropdown-menu').on('click', function (e) {
    if ($(e.target).closest('.bootstrap-select.open').is(':visible') || $(e.target).closest('.btn.dropdown-toggle.btn-default').is(':visible')) {
        selectpickerIsClicked = true;
    }
});

$('#ui-datepicker-div').on('click', function (e) {
    selectpickerIsClicked = true;
});

$('.dropdown').on('hide.bs.dropdown', function (e) {
    if (selectpickerIsClicked) {
        e.preventDefault();
        selectpickerIsClicked = false;
    }
});

$('input[id^="id_input_data_"]').datetimepicker(window.location.pathname.includes('search_annual_reports') ? datepickerOpt2 : datepickerOpt1).mask(window.location.pathname.includes('search_annual_reports') ? "0000" : "00.00.0000", window.location.pathname.includes('search_annual_reports') ? dateMaskOpt2 : dateMaskOpt1);