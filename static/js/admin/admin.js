django.jQuery(function(){
// Меняем title для перевода с английского на русский
    django.jQuery('.grp-add-handler').prop('title', 'Добавить запись')
    django.jQuery('.grp-remove-handlerm, .grp-delete-handler').prop('title', 'Удалить запись')
    django.jQuery('#grp-open-all, .grp-open-handler').prop('title', 'Открыть все записи')
    django.jQuery('#grp-close-all, .grp-close-handler').prop('title', 'Свернуть все записи')

// Если DtipDocument пустой (т.е. нет ни одного сохраненного типа документа), то открываем отображение парвого инлайна CEdocumentInline и скрываем ExistDtipDocumentInline
    if (!django.jQuery('div[id$="dtipdocument_set-group"] tbody').length) {
        django.jQuery('div[id$="dtipdocument_set-group"]').hide()
        django.jQuery('#cedocument_set-0').removeClass('grp-closed').addClass('grp-open')
    }

// При добавлении новой экспертизы скрываем отображение JERPersonInline и CEdocumentInline, а также открываем отображение парвого инлайна CEdocumentInline
    if (django.jQuery('#id_organizaciya').val() == '') {
        django.jQuery('#jerperson_set-group, #cedocument_set-group').removeClass('grp-open').addClass('grp-closed')
        django.jQuery('#cedocument_set-0').removeClass('grp-closed').addClass('grp-open')
    }
// Установливаем для эдемента cedocument_set-empty класс grp-open, что бы все последующие открываемые документы также сразу были раскрыты
    django.jQuery('#cedocument_set-empty').removeClass('grp-closed').addClass('grp-open')

// Скрыть информацию о Разрешении у существующих записей не соответствующих типу Разрешение (inline - ExistDtipDocumentInline)
    django.jQuery('tbody[id^="cedocument_set"][id*="dtipdocument_set"] div.grp-readonly').each(function (index, element) {
        if (django.jQuery(element).find('a').text() != 'Разрешение') django.jQuery('#' + django.jQuery(element).parents('tbody')[0].id + '-jddrazr_set-group').parent().hide()
    })

// Скрыть информацию о Разрешении у существующих записей не соответствующих типу Разрешение (inline - AddDtipDocumentInline)
    django.jQuery('select[name^="cedocument_set"][name$="tip"]').each(function (index, element) {
        if (django.jQuery(element).val() != '1') django.jQuery('#' + element.name.split('-tip')[0] + '-jddrazr_set-group').parent().hide()
    })

// Добавление новых наборов форм
    django.jQuery(document).on('formset:added', function(event, $row, formsetName) {
// При добавлении нового документа скрываем ExistDtipDocumentInline
        if (formsetName.includes('cedocument_set')) django.jQuery('#' + $row[0].id + '-dtipdocument_set-group').hide()
// При добавлении нового типа документа скрываем информацию о Разрешении
        if (formsetName.includes('dtipdocument_set')) django.jQuery('#' + $row[0].id + '-jddrazr_set-group').parent('td').hide()
    })

// Проверка выбранного типа и в соответствии этим открываем / скрываем информацию о Разрешении
    django.jQuery('select[name^="cedocument_set"][name$="tip"]').on('change', function() {
        var elem = django.jQuery('#' + django.jQuery(this)[0].name.split('-tip')[0] + '-jddrazr_set-group').parent('td')
        if (django.jQuery(this).val() == '1') elem.show()
        else elem.hide()
    })


// Проверка выбранного типа документа и открытие / скрытие необходимого количества дат
    django.jQuery('select[name^="cedocument_set"][name$="tip"]').on('change', function() {
        var elem1 = django.jQuery('#' + django.jQuery(this)[0].name.split('-dtipdocument')[0] + '-jdatadocument_set-group').find('table')

        var tbody_data_1 = elem1.find('#' + django.jQuery(this)[0].name.split('-dtipdocument')[0] + '-jdatadocument_set-0')
        var tbody_data_2 = elem1.find('#' + django.jQuery(this)[0].name.split('-dtipdocument')[0] + '-jdatadocument_set-1')
        var tbody_data_3 = elem1.find('#' + django.jQuery(this)[0].name.split('-dtipdocument')[0] + '-jdatadocument_set-2')

        if (django.jQuery(this).val() == '1') tbody_data_1.show(), tbody_data_2.show(), tbody_data_3.show()
        else if (django.jQuery(this).val() == '2') tbody_data_1.hide(), tbody_data_2.hide(), tbody_data_3.hide()
        else if (django.jQuery(this).val() == '4') tbody_data_1.show(), tbody_data_2.show(), tbody_data_3.hide()
        else if (django.jQuery(this).val() == '5') tbody_data_1.show(), tbody_data_2.show(), tbody_data_3.hide()
        else if (django.jQuery(this).val() == '6') tbody_data_1.hide(), tbody_data_2.hide(), tbody_data_3.hide()
        else if (django.jQuery(this).val() == '7') tbody_data_1.show(), tbody_data_2.show(), tbody_data_3.hide()
        else if (django.jQuery(this).val() == '8') tbody_data_1.hide(), tbody_data_2.hide(), tbody_data_3.hide()
        else if (django.jQuery(this).val() == '9') tbody_data_1.show(), tbody_data_2.show(), tbody_data_3.hide()
        else if (django.jQuery(this).val() == '10') tbody_data_1.show(), tbody_data_2.hide(), tbody_data_3.hide()
        else if (django.jQuery(this).val() == '12') tbody_data_1.hide(), tbody_data_2.hide(), tbody_data_3.hide()
        else if (django.jQuery(this).val() == '13') tbody_data_1.hide(), tbody_data_2.hide(), tbody_data_3.hide()
        else if (django.jQuery(this).val() == '14') tbody_data_1.show(), tbody_data_2.show(), tbody_data_3.hide()
        else if (django.jQuery(this).val() == '15') tbody_data_1.hide(), tbody_data_2.hide(), tbody_data_3.hide()
        else if (django.jQuery(this).val() == '18') tbody_data_1.hide(), tbody_data_2.hide(), tbody_data_3.hide()
        else if (django.jQuery(this).val() == '19') tbody_data_1.hide(), tbody_data_2.hide(), tbody_data_3.hide()
        else if (django.jQuery(this).val() == '20') tbody_data_1.hide(), tbody_data_2.hide(), tbody_data_3.hide()
        else tbody_data_1.hide(), tbody_data_2.hide(), tbody_data_3.hide()
    })

// Проверка выбранного типа документа и открытие / скрытие необходимого количества дат
django.jQuery('select[name^="cedocument_set"][name$="tip"]').on('change', function() {
    var elem1 = django.jQuery('#' + django.jQuery(this)[0].name.split('-dtipdocument')[0] + '-jdatadocument_set-group').find('table')
    var tbody_data_1 = elem1.find('#' + django.jQuery(this)[0].name.split('-dtipdocument')[0] + '-jdatadocument_set-0').find('#id_'+django.jQuery(this)[0].name.split('-dtipdocument')[0]+'-jdatadocument_set-0-opisanie_data')
    var tbody_data_2 = elem1.find('#' + django.jQuery(this)[0].name.split('-dtipdocument')[0] + '-jdatadocument_set-1').find('#id_'+django.jQuery(this)[0].name.split('-dtipdocument')[0]+'-jdatadocument_set-1-opisanie_data')
    var tbody_data_3 = elem1.find('#' + django.jQuery(this)[0].name.split('-dtipdocument')[0] + '-jdatadocument_set-2').find('#id_'+django.jQuery(this)[0].name.split('-dtipdocument')[0]+'-jdatadocument_set-2-opisanie_data')

    tbody_data_1.empty()
    tbody_data_2.empty()
    tbody_data_3.empty()
    console.log(tbody_data_1.val())

    // if (django.jQuery(this).val() == '1') tbody_data_1.find('option[value="1"]')[0].selected = true, tbody_data_2.find('option[value="2"]')[0].selected = true, tbody_data_3.find('option[value="4"]')[0].selected = true
    
    // else tbody_data_1.val(''), tbody_data_2.val(''), tbody_data_3.val('')
    
})

})