$(document).ajaxSuccess(() => { $('select + button, #filter-timerange button, [data-toggle="tooltip"], [aria-controls="id_table_nar"]').tooltip(tooltipOpt) });

$(document).ready(() => { getFiltersData() });

$(document).on('changed.bs.select', '#id_select_1', function() {
    $('#id_select_2 option').remove();

    if ($(this).find('option:selected').val() == "МТУ")                                  list_data['mtu'].forEach((item) => { $('#id_select_2').append('<option value="' + item + '">' + item + '</option>') });
    else if ($(this).find('option:selected').val() == "ЭО")                              list_data['org'].forEach((item) => { $('#id_select_2').append('<option value="' + item + '">' + item + '</option>') });
    else if ($(this).find('option:selected').val() == "ИЯУ")                             list_data['ust'].forEach((item) => { $('#id_select_2').append('<option value="' + item + '">' + item + '</option>') });
    else if ($(this).find('option:selected').val() == "Категориям нарушений")            list_data['kat'].forEach((item) => { $('#id_select_2').append('<option value="' + item + '">' + item + '</option>') });
    else if ($(this).find('option:selected').val() == "Непосредственной причине отказа") list_data['nep'].forEach((item) => { $('#id_select_2').append('<option value="' + item + '">' + item + '</option>') });
    else if ($(this).find('option:selected').val() == "Коренной причине отказа")         list_data['kor'].forEach((item) => { $('#id_select_2').append('<option value="' + item + '">' + item + '</option>') });

    $('#id_select_2').parents(':eq(1)').css('opacity', '1.0');
    $('#id_select_2').prop('disabled', false).selectpicker('refresh');
});

$(document).on('changed.bs.select', '#id_select_2', () => { searchTab.ajax.reload() });
$(document).on('click', '#id_button_advanced_search', () => { searchTab.ajax.reload() });
$(document).on('click', '#id_button_advanced_clear, [data-toggle="tab"]', () => { updateData() });

$(document).on('change', '#id_input_all', () => {
    if($('#id_input_all').val()) $('#id_text').html('Текст: ' + $('#id_input_all').val()).css('color', '#333');
    else $('#id_text').html('Текст').css('color', '#999');
});
