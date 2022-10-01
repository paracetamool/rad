function updateData() {
    $('#id_select_1 option:first').prop('selected', true);
    $('#id_select_2 option').remove();
    $('#id_select_2').parents(':eq(1)').css('opacity','0.3');
    $('#id_select_2').prop('disabled', true).selectpicker('refresh');

    $('select:not([name$="length"])').each((i, el) => { $(el).find('option').prop('disabled', false); $(el).selectpicker('val', '') });

    $('#id_text').html('Текст').css('color', '#999');
    $('#id_input_all').val('');

    $('#id_range').html('Временной интервал').css('color', '#999');
    $('#id_input_data_start, #id_input_data_end').val('');

    searchTab.ajax.reload();
};
