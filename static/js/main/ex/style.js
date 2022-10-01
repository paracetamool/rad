/**------------добавление tooltip (подсказка)------------------- */
// var tooltipOpt = {
//     trigger  : 'hover',
//     placement: 'auto',
//     container: 'body',
// };

// $(document).ajaxSuccess(() => { $('[data-toggle="tooltip"]').tooltip(tooltipOpt) });


/* ---------------Скрипт стилей при нажатии и наведении на кнопки левого блока-----------------*/
$("#sidebar_ex_v_rabote_otvet").click(function(){
    $(this).attr('class' , 'activ_ex_value')
    $('#sidebar_ex_v_rabote_zapros').attr('class' , 'none_activ_ex_value')
    var Main_block = document.getElementById('main_inform_body');
    Main_block.style.display = "none";
    document.getElementById("title_name").innerHTML = 'Информация по выбранной экспертизе'
})

$("#sidebar_ex_v_rabote_otvet").mouseenter(function(){
    $(this).attr('style' , 'color: black')

})

$("#sidebar_ex_v_rabote_otvet").mouseleave(function(){
    $(this).attr('style' , 'color: #777')
})

/*-----------*/

$("#sidebar_ex_v_rabote_zapros").click(function(){
    $(this).attr('class' , 'activ_ex_value')
    $('#sidebar_ex_v_rabote_otvet').attr('class' , 'none_activ_ex_value')
    var Main_block = document.getElementById('main_inform_body');
    Main_block.style.display = "none";
    document.getElementById("title_name").innerHTML = 'Информация по выбранной экспертизе'
})

$("#sidebar_ex_v_rabote_zapros").mouseenter(function(){
    $(this).attr('style' , 'color: black')
})

$("#sidebar_ex_v_rabote_zapros").mouseleave(function(){
    $(this).attr('style' , 'color: #777')

})

/* --------------------------------*/