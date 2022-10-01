moment.updateLocale(moment.locale(), { invalidDate: "Неопределен" });

var MainTable = $('#id_table_raz').DataTable({
    processing: true,
    scrollY: "calc(100vh - 260px)",
    ajax : {
        url : '/get_table_expertizi_data/',
        data : function(d) {
            d.v_rabote_otvet = $('#otvet_ex').attr('name');
            d.v_rabote_zapros = $('#zapros_ex').attr('name');
            d.vse_ex = $('#vse_ex').attr('name');
            d.srok1 = $('#opisanie_color1').attr('name');
            d.srok2 = $('#opisanie_color2').attr('name');
            d.srok3 = $('#opisanie_color3').attr('name');
            d.sbros_ex = $('#sbros_checkbox').attr('name');
            d.vibros_ex = $('#vibros_checkbox').attr('name');
        }
    },
    paging: true,
    bFilter: true,
    ordering: true,
    lengthMenu: [[20, 25, 50, 100, -1], [20, 25, 50, 100, "Все"]],
    language: {url: "/static/DataTables/json/custom.json"},
    order: [[ 0, "asc" ]],
    dom:
        `<'row'<'col-sm-3'><'col-sm-2'>>
        <'row'<'col-sm-12'tr>>
        <'row'<'col-sm-5'><'col-sm-7'p>>`,
    
    columnDefs: [
        {
            targets: 4,
            render: $.fn.dataTable.render.moment('DD.MM.YYYY','DD.MM.YYYY'  )
    }],
    aoColumnDefs: [
        { 'bSortable': false, 'aTargets': [ 0 ] }
    ],
    initComplete:function(){
        $('button.btn.dropdown-toggle.btn-default.bs-placeholder').attr('style','border-radius:0;')
        $('button#btn_srok_arch.btn.btn-default.dropdown-toggle').attr('style','border-top-left-radius:0;border-bottom-left-radius: 0;')
    },
    drawCallback: function(settings) {
        var pagination = $(this).closest('.dataTables_wrapper').find('.dataTables_paginate')
        pagination.toggle(this.api().page.info().pages > 1)
        $('[role="tooltip"]').remove()
    },
    "createdRow": function( row, data, dataIndex ) {
        var div = document.createElement('div');
        div.innerHTML = data[1];
        var result = div.firstChild;
        if (Number(result.attributes.name.value ) == 2){
            $(row).addClass("warning")
        } else if (Number(result.attributes.name.value ) == 3){
            $(row).addClass("danger")
        } else if (Number(result.attributes.name.value ) == 1){
            $(row).addClass("success")
        } else if (Number(result.attributes.name.value ) == 5){
            $(row).addClass("info")
            $(row).attr('style','font-weight:bold')
        }


    } 
})

MainTable.on( 'order.dt search.dt', function () {
    MainTable.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
        cell.innerHTML = '<div>' + String(i+1) + '</div>';
    } );
} ).draw();


var buttons = new $.fn.dataTable.Buttons(MainTable, {
    buttons:[
        {
            extend : 'excel',
            text : '<i class="fa fa-file-excel-o"></i>',
            titleAttr : 'Сохранить в Excel',
            attr: {
                'data-toggle':'tooltip',
            },
            title: '',
            filename:'Экспертизы в работе',   
            customize: function( xlsx, row ) {
                var sheet = xlsx.xl.worksheets['sheet1.xml'];
                 $('row c[r^="A"]', sheet).attr( 's', 50);
                 $('row:eq(0) c', sheet).attr( 's', 2 );
                 $('row c[r^="A"]', sheet).each( function(i,elem){
                    if (i == 0){
                        return true  
                    } else {
                        $('v', this).text(i);  
                    } 
                 })
            },
            autoFilter:true,   
        },
        {
            extend : 'pdf',
            text   : '<i class="fa fa-file-pdf-o"></i>',
            titleAttr: 'Сохранить в PDF',
            attr: {
                'data-toggle':'tooltip',
            },
            filename: 'Экспертизы в работе',
            exportOptions: {
                columns: [0,1,2,3,4]
            },
            customize: function (pdf, row){
                // console.log(pdf.content)
                var Len = pdf.content[1].table.body.length
                for (let i =0 ; i < Len ;i++){
                    if (i!=0){
                        pdf.content[1].table.body[i][0].text = i
                    }
                }
            }
        },
        {
            extend   : 'print',
            text     : '<i class="fa fa-print"></i>',
            titleAttr: 'Печать',
            attr: {
                'data-toggle':'tooltip',
            },
            exportOptions: {
                    columns: [0,1,2,3,4]
                },
            // customize: function(window){
            //     var Len = window.document.querySelectorAll("tbody tr").length
            //     for (let i=0;i<Len;i++){
            //         console.log(window.document.querySelectorAll("tbody tr td:first-child")[i].innerHTML = i+1)
            //     }
            // }
        },
       
    ],
}).container().appendTo($('#bt_copy_xl_pdf'));
MainTable.order( [4,'asc'] ).draw();

/**-----------Функции на кнопки "Ответ" и "Запрос"---------- */
function Otvet_ex(){
    document.getElementById('otvet_ex').setAttribute('name','active')
    document.getElementById('zapros_ex').setAttribute('name','')
    document.getElementById('vse_ex').setAttribute('name','')
    document.getElementById('title_name').innerHTML = 'Сводная информация'
    MainTable.ajax.reload()
}

function Zapros_ex(){
    document.getElementById('zapros_ex').setAttribute('name','active')
    document.getElementById('otvet_ex').setAttribute('name','')
    document.getElementById('vse_ex').setAttribute('name','')
    document.getElementById('title_name').innerHTML = 'Сводная информация'
    MainTable.ajax.reload()
}

function Vse_ex(){
    document.getElementById('vse_ex').setAttribute('name','active')
    document.getElementById('otvet_ex').setAttribute('name','')
    document.getElementById('zapros_ex').setAttribute('name','')
    document.getElementById('title_name').innerHTML = 'Сводная информация'
    MainTable.ajax.reload()
}

/**-----------------Выброс , Сбросы и все вместе-------------- */


$('#vibros_checkbox').click( function  () {
    $('#sbros_checkbox').removeClass('active')
    $('#sbros_checkbox').attr('name','')
    $('#id_tip_all').removeClass('active')
    $(this).attr('name','active')
    MainTable.ajax.reload()
});

$('#sbros_checkbox').click( function  () { 
    $('#vibros_checkbox').removeClass('active')
    $('#vibros_checkbox').attr('name','')
    $('#id_tip_all').removeClass('active')
    $(this).attr('name','active')
    MainTable.ajax.reload()
});

$('#id_tip_all').click( function  () { 
    $('#vibros_checkbox').removeClass('active')
    $('#sbros_checkbox').removeClass('active')
    $('#vibros_checkbox').attr('name','')
    $('#sbros_checkbox').attr('name','')
    $(this).attr('name','active')
    MainTable.ajax.reload()
});
/**----------Сроки--------------------- */


$('.bt_all').on('click',function(){
    document.getElementById('opisanie_color1').setAttribute('name','')
    document.getElementById('opisanie_color2').setAttribute('name','')
    document.getElementById('opisanie_color3').setAttribute('name','')
    $('#btn_srok_arch')[0].className = 'btn btn-default dropdown-toggle'
    $('#btn_srok_arch')[0].innerHTML = '<div id=\"id_range\">Вывести все сроки</div>\n<span class=\"bs-caret\"><span class=\"caret\"></span></span>\n'
    MainTable.ajax.reload();
})

$('.bt_success').on('click',function(){
    document.getElementById('opisanie_color1').setAttribute('name','active')
    document.getElementById('opisanie_color2').setAttribute('name','')
    document.getElementById('opisanie_color3').setAttribute('name','')
    $('#btn_srok_arch')[0].className = 'btn bt_success dropdown-toggle'
    $('#btn_srok_arch')[0].innerHTML = '<div id=\"id_range\">Более половины срока</div>\n<span class=\"bs-caret\"><span class=\"caret\"></span></span>\n'
    MainTable.ajax.reload();   
})

$('.btn_warning').on('click',function(){
    document.getElementById('opisanie_color1').setAttribute('name','')
    document.getElementById('opisanie_color2').setAttribute('name','active')
    document.getElementById('opisanie_color3').setAttribute('name','')
    $('#btn_srok_arch')[0].className = 'btn btn_warning dropdown-toggle'
    $('#btn_srok_arch')[0].innerHTML = '<div id=\"id_range\">Менее половины срока</div>\n<span class=\"bs-caret\"><span class=\"caret\"></span></span>\n'
    MainTable.ajax.reload();   
})

$('.btn_danger').on('click',function(){
    document.getElementById('opisanie_color1').setAttribute('name','')
    document.getElementById('opisanie_color2').setAttribute('name','')
    document.getElementById('opisanie_color3').setAttribute('name','active')
    $('#btn_srok_arch')[0].className = 'btn btn_danger dropdown-toggle'
    $('#btn_srok_arch')[0].innerHTML = '<div id=\"id_range\">Осталось менее недели</div>\n<span class=\"bs-caret\"><span class=\"caret\"></span></span>\n'
    MainTable.ajax.reload();    
})


    //Функция по добавлению названий файлов в модальном окне
    function ChangeSybmol(url,id_teg,list_data,list_name){
        var  name_file = list_name.join(" ")
        var name_file_other = name_file + "_"
        if (url== 'Отсутствует'){
            document.getElementById(id_teg).innerHTML = '<span class="glyphicon glyphicon-minus"></span>'
        } else {
            document.getElementById(id_teg).innerHTML = ''
            list_data.forEach(function (item, i, arr){
                p = document.createElement('p')
                p.setAttribute('style','margin:0;')
                a = document.createElement('a')
                a.setAttribute("href", item['url'])
                a.setAttribute("target", '_blank')
                if (i==0){
                    a.innerHTML = name_file
                } else {
                    a.innerHTML = name_file_other + String(i+1)
                }
                p.appendChild(a)
                document.getElementById(id_teg).appendChild(p)
            })
        }
    }



/*------------------------Скрипт по выводу информации на вкладке Экспертизы в работе--------------------------*/
function Inform_Ex_v_rabote(aa, b, c,ff){
    var treb_deyst = b.join(' ')
    if (c == 4){color_td = '#D2D2D2'}
    else if (c == 3){color_td = '#f2dede'} 
    else if (c == 2){color_td = '#fcf8e3'} 
    else if (c == 1){color_td = '#dff0d8'}

    if ((String(ff.join('')) == "Неопределен") || (ff == 4)){srok_td = ' Срок неопределен'} 
    else {srok_td = 'до ' + String(ff.join(''))}

    $.ajax({
        method: "GET",
        url: '/get_inform_block_ex/',
        data : {
            'idd_ex': aa,
            'treb_deystv':b
        },
        dataType: 'json',
        success: function(data) {
            //-------------Вывод истории----------------
            tbody = document.getElementById("table_tbody_actions")
            tbody.innerHTML = ''

            if (String(Object.getOwnPropertyNames(data.action_list).length) == String(0)){
                document.getElementById("table_process_istorii").style.display = "none";
                document.getElementById("p_process_istorii").style.display = "";
            } else {
                document.getElementById("table_process_istorii").style.display = "";
                document.getElementById("p_process_istorii").style.display = "none";
            }

            for (var prop in data.action_list) {
                tr = document.createElement('tr')
                td1 = document.createElement('td')
                td1.innerHTML = data.action_list[prop][1]
                tr.appendChild(td1)
                td2 = document.createElement('td')
                td2.innerHTML = data.action_list[prop][0]
                tr.appendChild(td2)
                td3 = document.createElement('td')
                td3.innerHTML = data.action_list[prop][2]
                tr.appendChild(td3)
                tbody.appendChild(tr)  
              }
            //-----------------------------
            $('#nav_pills_expertiza').attr('class','active')
            $('#menu1').attr('class','tab-pane fade in active')
            $('#nav_pills_process').attr('class','')
            $('#menu2').attr('class','tab-pane fade')
            //-----------------------------
            if (c == 5){
                document.getElementById("title_name").innerHTML = data.nazvanie_polnoe + ' - Заполнена неправильно, что-то лишнее или чего-то не хватает!'
                $('#title_name').attr('style','font-weight:bold;color:red;text-align:center;')
                $('#tip_deystviya').innerHTML = treb_deyst
                $('#tip_deystviya').attr('style','font-weight:bold;color:red;text-align:center;')
            } else {
                document.getElementById("title_name").innerHTML = data.nazvanie_polnoe
                $('#title_name').attr('style','font-weight:normal;color:black;text-align:center;')
                $('#tip_deystviya').innerHTML = treb_deyst
                $('#tip_deystviya').attr('style','')
            }
            document.getElementById("tip_ex").innerHTML = data.gos_usluga
            document.getElementById("organizovannie_ex").innerHTML = Number(data.vse_istochiki) - Number(data.neorg_istochniki)
            document.getElementById("neorganizovannie_ex").innerHTML = data.neorg_istochniki
            document.getElementById("vsego_istochnikov_ex").innerHTML = data.vse_istochiki
            document.getElementById("tip_deystviya").innerHTML = treb_deyst
            // Условия по закрашиванию необходимых полей
            $('#pismo_v_rtn').attr('style','text-align: center;background:#fff; border-radius: 0;')
            $('#pismo_v_rtn').removeAttr('data-original-title')
            $('#pismo_v_org').attr('style','text-align: center;background:#fff; border-radius: 0;')
            $('#pismo_v_org').removeAttr('data-original-title')
            $('#pismo_rtn_o_ex').attr('style','text-align: center;background:#fff; border-radius: 0;')
            $('#pismo_rtn_o_ex').removeAttr('data-original-title')
            $('#pismo_org_o_ex').attr('style','text-align: center;background:#fff; border-radius: 0;')
            $('#pismo_org_o_ex').removeAttr('data-original-title')
            $('#zapros_tkp').attr('style','text-align: center;background:#fff; border-radius: 0;')
            $('#zapros_tkp').removeAttr('data-original-title')
            $('#proekt_dogov_TZ').attr('style','text-align: center;background:#fff; border-radius: 0;')
            $('#proekt_dogov_TZ').removeAttr('data-original-title')
            $('#zapros_snig_cen').attr('style','text-align: center;background:#fff; border-radius: 0;')
            $('#zapros_snig_cen').removeAttr('data-original-title')
            $('#otvet_snig_cen').attr('style','text-align: center;background:#fff; border-radius: 0;')
            $('#otvet_snig_cen').removeAttr('data-original-title')
            $('#zakl_dogovor').attr('style','text-align: center;background:#fff; border-radius: 0;')
            $('#zakl_dogovor').removeAttr('data-original-title')
            $('#proekt_normat').attr('style','text-align: center;background:#fff; border-radius: 0;')
            $('#proekt_normat').removeAttr('data-original-title')
            $('#otvet_zapros_tkp').attr('style','text-align: center;background:#fff; border-radius: 0;')
            $('#otvet_zapros_tkp').removeAttr('data-original-title')
            $('#otvet_proekt_dogov_TZ').attr('style','text-align: center;background:#fff; border-radius: 0;')
            $('#otvet_proekt_dogov_TZ').removeAttr('data-original-title')
            $('#ex_zakl_pismo_RTN').parent().attr('style','text-align: center;background:#fff; border-radius: 0;')
            $('#ex_zakl_pismo_RTN').parent().removeAttr('data-original-title')
            $('#akt').attr('style','text-align: center;background:#fff; border-radius: 0;')
            $('#akt').removeAttr('data-original-title')
            //---------------------
            if (data.data_document == 'Не утверждено' | data.data_document == ''){
                document.getElementById("konec_ex").innerHTML = 'Экспертное заключение не утверждено'
                $('#konec_ex').removeClass('data_ex_zakl_error')
                $('#konec_ex').addClass('data_ex_zakl_not_error')
                $('#errors').removeClass('p_error')
                $('#errors').addClass('not_p_eror')
            }
            else if (data.data_document == 'Нет даты утверждения') {
                document.getElementById("konec_ex").innerHTML = 'Так как ЭЗ подгрузили, то необходимо указать дату утверждения!!'
                $('#konec_ex').removeClass('data_ex_zakl_not_error')
                $('#konec_ex').addClass('data_ex_zakl_error')
                $('#errors').removeClass('not_p_eror')
                $('#errors').addClass('p_error')
            }
            else {
                document.getElementById("konec_ex").innerHTML = document.getElementById("konec_ex").innerHTML = data.data_document
                $('#konec_ex').removeClass('data_ex_zakl_error')
                $('#konec_ex').addClass('data_ex_zakl_not_error')
                $('#errors').removeClass('p_error')
                $('#errors').addClass('not_p_eror')
            }
            // проверка на наличие участников экспертизы
            if (String(data.rukovoditel) == ''){document.getElementById("tr_ruk_expertizi").style.display = "none";} 
            else {document.getElementById("tr_ruk_expertizi").style.display = "";}

            if (String(data.expert) == ''){document.getElementById("tr_experti").style.display = "none";} 
            else {document.getElementById("tr_experti").style.display = "";}

            if (String(data.rukovod_otdeleniya) == ''){document.getElementById("tr_ruk_podrazdel").style.display = "none";} 
            else {document.getElementById("tr_ruk_podrazdel").style.display = "";}
            // конец проверки
            document.getElementById("experti_raboti").innerHTML = data.expert.join("");
            document.getElementById("rukovoditel_raboti").innerHTML = data.rukovoditel
            document.getElementById("rukovoditel_podrazdeleniya").innerHTML = data.rukovod_otdeleniya
            // Выставление навазния файлов(ссылок) в модальном окне
            // Проверка на наличие "запроса и ответа о снижении цены"
            if (data.url_zapros_ceni == 'Отсутствует' && data.url_otvet_ceni == 'Отсутствует'){document.getElementById("snigenie_cen").style.display = "none";} else {
                document.getElementById("snigenie_cen").style.display = "";

                url_zapros_ceni_1 = data.url_zapros_ceni
                id_zapros_snig_cen_1 = 'zapros_snig_cen'
                list_zapros_ceni_1 =  data.list_zapros_ceni
                list_name_1 = 'Запрос о снижении цены'.split(" ")
                ChangeSybmol(url_zapros_ceni_1,id_zapros_snig_cen_1,list_zapros_ceni_1,list_name_1)

                url_otvet_ceni_2 = data.url_otvet_ceni
                id_otvet_snig_cen_2 = 'otvet_snig_cen'
                list_otvet_ceni_2 =  data.list_otvet_ceni
                list_name_2 = 'Ответ на запрос о снижении цены'.split(" ")
                ChangeSybmol(url_otvet_ceni_2,id_otvet_snig_cen_2,list_otvet_ceni_2,list_name_2)
            }
            // Проверка на наличие "письма из РТН об экспертизе"
            url_pismo_rtn1 = data.url_pismo_rtn
            id_pismo_rtn1 = 'pismo_rtn_o_ex'
            list_pismo_rtn1 =  data.list_pismo_rtn
            list_name1 = 'Письмо из РТН / ТО'.split(" ")
            ChangeSybmol(url_pismo_rtn1,id_pismo_rtn1,list_pismo_rtn1,list_name1)

            // Проверка на наличие "письма в РТН об окончании экспертизы"
            url_pismo_v_rtn2 = data.url_pismo_v_rtn
            id_pismo_rtn2 = "pismo_v_rtn"
            list_pismo_v_rtn2 =  data.list_pismo_v_rtn
            list_name2 = 'Письмо в РТН / ТО'.split(" ")
            ChangeSybmol(url_pismo_v_rtn2,id_pismo_rtn2,list_pismo_v_rtn2,list_name2)

            // Проверка на наличие "письма от Заявителя об экспертизе"
            url_pismo_org3= data.url_pismo_org
            id_pismo_org3 = "pismo_org_o_ex"
            list_ot_organizacii3 =  data.list_ot_organizacii
            list_name3 = 'Письмо из организации'.split(" ")
            ChangeSybmol(url_pismo_org3,id_pismo_org3,list_ot_organizacii3,list_name3)

            // Проверка на наличие "письма Заявителю об отправке ЭЗ по Договору"
            url_pismo_org4= data.url_pismo_v_org
            id_pismo_org4 = "pismo_v_org"
            list_pismo_v_org4 =  data.list_v_organizacii
            list_name4 = 'Письмо в организацию по договору'.split(" ")
            ChangeSybmol(url_pismo_org4,id_pismo_org4,list_pismo_v_org4,list_name4)

            // Проверка на наличие "запроса ТКП от Заявителя"
            url_zapros_tkp5= data.url_zapros_tkp1
            id_zapros_tkp5 = "zapros_tkp"
            list_list_zapros_tkp5 =  data.list_zapros_tkp
            list_name5 = 'Запрос ТКП'.split(" ")
            ChangeSybmol(url_zapros_tkp5,id_zapros_tkp5,list_list_zapros_tkp5,list_name5)

            // Проверка на наличие "Ответа на запрос ТКП Заявителя"
            url_otvet_tkp6= data.url_otvet_tkp
            id_otvet_zapros_tkp6 = "otvet_zapros_tkp"
            list_otvet_tkp6 =  data.list_otvet_tkp
            list_name6 = 'Ответ ТКП'.split(" ")
            ChangeSybmol(url_otvet_tkp6,id_otvet_zapros_tkp6,list_otvet_tkp6,list_name6)
            
            // Проверка на наличие "письма и ответа о проекте договора"
            if (data.url_dogov_TZ == 'Отсутствует' && data.url_otvet_dogov_TZ == 'Отсутствует'){document.getElementById("tr_proekt_dogovora").style.display = "none";} else{
                document.getElementById("tr_proekt_dogovora").style.display = "";

                url_dogov_TZ7= data.url_dogov_TZ
                id_proekt_dogov_TZ7 = "proekt_dogov_TZ"
                list_pismo_dogovor7 =  data.list_pismo_dogovor
                list_name7 = 'Письмо о проекте договора'.split(" ")
                ChangeSybmol(url_dogov_TZ7,id_proekt_dogov_TZ7,list_pismo_dogovor7,list_name7)

                url_dogov_TZ8= data.url_otvet_dogov_TZ
                id_proekt_dogov_TZ8 = "otvet_proekt_dogov_TZ"
                list_otvet_dogovor8 =  data.list_otvet_dogovor
                list_name8 = 'Ответ на проект договора'.split(" ")
                ChangeSybmol(url_dogov_TZ8,id_proekt_dogov_TZ8,list_otvet_dogovor8,list_name8)
            }
            
            // Проверка на наличие "письма Заявителю об отправке ЭЗ по Гарантийному письму"
            url_pismo_v_org_garant9= data.url_pismo_v_org_garant
            id_proekt_dogov_TZ9 = "td_pismo_garant"
            list_v_organizacii_garant9 =  data.list_v_organizacii_garant
            list_name9 = 'Письмо в организацию по гарантийному письму'.split(" ")
            ChangeSybmol(url_pismo_v_org_garant9,id_proekt_dogov_TZ9,list_v_organizacii_garant9,list_name9)

            // Проверка на наличие "Гарантийного письма"
            if (data.url_garant_pismo == 'Отсутствует'){
                document.getElementById("tr_garant_pismo").style.display = "none";
                document.getElementById("pismo_garant").style.display = "none";
                document.getElementById("th_pismo_org_o_ex").setAttribute('rowspan','1')
                document.getElementById("pismo_org_o_ex").setAttribute('rowspan','1')
            } else {
                document.getElementById("pismo_garant").style.display = "";
                document.getElementById("th_pismo_org_o_ex").setAttribute('rowspan','2')
                document.getElementById("pismo_org_o_ex").setAttribute('rowspan','2')
                document.getElementById("tr_garant_pismo").style.display = "";
            }

            url_garant_pismot10= data.url_garant_pismo
            id_garant_pismo10 = "garant_pismo"
            list_garant_pismo10 =  data.list_garant_pismo
            list_name10 = 'Гарантийное письмо'.split(" ")
            ChangeSybmol(url_garant_pismot10,id_garant_pismo10,list_garant_pismo10,list_name10)

            // Проверка на наличие "Заключенного договора"
            url_zakl_dogov11= data.url_zakl_dogov
            id_zakl_dogovor11 = "zakl_dogovor"
            list_zakl_dogovor11 =  data.list_zakl_dogovor
            list_name11 = 'Заключенный договор'.split(" ")
            ChangeSybmol(url_zakl_dogov11,id_zakl_dogovor11,list_zakl_dogovor11,list_name11)

            // Проверка на наличие "Проекта нормативов"
            url_proekt_norm12= data.url_proekt_norm
            id_proekt_normat12 = "proekt_normat"
            list_proekt_normativov12 =  data.list_proekt_normativov
            if (data.gos_usluga == 'Выдача разрешения на выброс радиоактивных веществ'){list_name12 = 'Нормативы ПДВ РВ'.split(" ")} 
            else{list_name12 = 'Нормативы ДС РВ'.split(" ")}

            ChangeSybmol(url_proekt_norm12,id_proekt_normat12,list_proekt_normativov12,list_name12)

            // Проверка на наличие "Акта сдачи-приемки"
            url_akt13= data.url_akt
            id_akt13 = "akt"
            list_Akt13 =  data.list_Akt
            list_name13 = 'Акт сдачи-приемки'.split(" ")
            ChangeSybmol(url_akt13,id_akt13,list_Akt13,list_name13)

            // Проверка на наличие "Служебные записки"
            if (String(data.url_sluzhebki) == 'Отсутствует'){ document.getElementById("block_prochie_dok").style.display = "none";} 
            else {document.getElementById("block_prochie_dok").style.display = "";}
            url_sluzhebki14= data.url_sluzhebki
            id_sluzhebki14 = "sluzhebki"
            list_sluzhebki14 =  data.list_sluzhebki
            list_name14 = 'Служебная записка'.split(" ")
            ChangeSybmol(url_sluzhebki14,id_sluzhebki14,list_sluzhebki14,list_name14)
            
            // небольшая проверка на предмет наличия ошибок в части незаполненых полей после загрузки ЭЗ
            if (String(data.url_Ex_zakl) == 'Отсутствует'){
                document.getElementById("ex_zakl_pismo_RTN").setAttribute("style", 'pointer-events: none; color: black;')
                document.getElementById("ex_zakl_pismo_RTN").innerHTML = '<span class="glyphicon glyphicon-minus"></span>'
                document.getElementById("kem_utvergdeno").style.display = "none";
                $('#ex_zakl_pismo_RTN').removeClass('nomer_ex_zakl_error')
                $('#ex_zakl_pismo_RTN').addClass('nomer_ex_zakl_not_error') 
            } else {
                document.getElementById("ex_zakl_pismo_RTN").setAttribute("href", data.url_Ex_zakl)
                document.getElementById("ex_zakl_pismo_RTN").setAttribute("style", 'pointer-events: auto; color: #337ab7;')
                
                document.getElementById("kem_utvergdeno").style.display = "";
                document.getElementById("utvergdeno_raboti").innerHTML = '';
                // Проверяем на наличие ошибок в заполнении для уже загруженного ЭЗ
                if (data.utvergdaet == '' | data.nomer_expertnogo_zaklucheniya == 'Номер не указан' | data.data_document == 'Нет даты утверждения') {
                    $('#errors').removeClass('not_p_eror')
                    $('#errors').addClass('p_error')
                    // проверяем на наличие Лица, который утвердил экспертизу
                    if (data.utvergdaet == '') {
                        document.getElementById("utvergdeno_raboti").innerHTML = 'Так как ЭЗ подгрузили, то необходимо указать кем оно утверждено!!'
                        $('#utvergdeno_raboti').removeClass('data_ex_zakl_not_error')
                        $('#utvergdeno_raboti').addClass('data_ex_zakl_error')
                    } else{
                        document.getElementById("utvergdeno_raboti").innerHTML = data.utvergdaet
                        $('#utvergdeno_raboti').removeClass('data_ex_zakl_error')
                        $('#utvergdeno_raboti').addClass('data_ex_zakl_not_error')
                    }
                    // Проверяем на наличие номера экспертного закючения
                    if (data.nomer_expertnogo_zaklucheniya == 'Номер не указан'){
                        $('#ex_zakl_pismo_RTN').removeClass('nomer_ex_zakl_not_error')
                        $('#ex_zakl_pismo_RTN').addClass('nomer_ex_zakl_error')
                        $('#ex_zakl_pismo_RTN').attr('style','color: white')
                        document.getElementById("ex_zakl_pismo_RTN").innerHTML = data.nomer_expertnogo_zaklucheniya
                    } else {
                        $('#ex_zakl_pismo_RTN').removeClass('nomer_ex_zakl_error')
                        $('#ex_zakl_pismo_RTN').addClass('nomer_ex_zakl_not_error')
                        $('#ex_zakl_pismo_RTN').attr('style','color: #337ab7') 
                        document.getElementById("ex_zakl_pismo_RTN").innerHTML = 'ДНП ' + data.nomer_expertnogo_zaklucheniya
                    }
                } else{
                    document.getElementById("ex_zakl_pismo_RTN").innerHTML = 'ДНП ' + data.nomer_expertnogo_zaklucheniya
                    document.getElementById("utvergdeno_raboti").innerHTML = data.utvergdaet
                    $('#utvergdeno_raboti').removeClass('data_ex_zakl_error')
                    $('#utvergdeno_raboti').addClass('data_ex_zakl_not_error')
                    $('#ex_zakl_pismo_RTN').removeClass('nomer_ex_zakl_error')
                    $('#ex_zakl_pismo_RTN').addClass('nomer_ex_zakl_not_error') 
                    $('#errors').removeClass('p_error')
                    $('#errors').addClass('not_p_eror')
                }
                
            }
            
            // Цветовая зарисовка необходимых документов со сроками и требующим действием в tooltype
            if (String(treb_deyst) == 'Письмо в организацию и РТН/ТО'){
                $('#pismo_v_rtn').attr('style','text-align: center;background:'+color_td+'; border-radius: 5px;')
                $('#pismo_v_rtn').attr('data-placement','top')
                $('#pismo_v_rtn').attr('data-toggle','tooltip')
                $('#pismo_v_rtn').attr('data-original-title','Подготовка письма в Ростехнадзор (или территориальный орган).' + srok_td )
                document.getElementById("pismo_v_rtn").innerHTML = srok_td

                $('#pismo_v_org').attr('style','text-align: center;background:'+color_td+'; border-radius: 5px;')
                $('#pismo_v_org').attr('data-placement','top')
                $('#pismo_v_org').attr('data-toggle','tooltip')
                $('#pismo_v_org').attr('data-original-title','Подготовка письма в организацию.' + srok_td )
                document.getElementById("pismo_v_org").innerHTML = srok_td
            } else if (String(treb_deyst) == 'Запрос ТКП'){
                $('#zapros_tkp').attr('style','text-align: center;background:'+color_td+'; border-radius: 5px;')
                $('#zapros_tkp').attr('data-placement','top')
                $('#zapros_tkp').attr('data-toggle','tooltip')
                $('#zapros_tkp').attr('data-original-title','Ожидается запрос ТКП.' + srok_td )
                document.getElementById("zapros_tkp").innerHTML = srok_td
            } else if (String(treb_deyst) == 'Ожидается проект договора и ТЗ'){
                $('#proekt_dogov_TZ').attr('style','text-align: center;background:'+color_td+'; border-radius: 5px;')
                $('#proekt_dogov_TZ').attr('data-placement','top')
                $('#proekt_dogov_TZ').attr('data-toggle','tooltip')
                $('#proekt_dogov_TZ').attr('data-original-title','Ожидается проект договора и ТЗ. ' + srok_td)
                document.getElementById("proekt_dogov_TZ").innerHTML = srok_td
            } else if (String(treb_deyst) == 'Ожидается заключение договора'){
                $('#zakl_dogovor').attr('style','text-align: center;background:'+color_td+'; border-radius: 5px;')
                $('#zakl_dogovor').attr('data-placement','top')
                $('#zakl_dogovor').attr('data-toggle','tooltip')
                $('#zakl_dogovor').attr('data-original-title','Ожидается заключение договора. '  + srok_td)
                document.getElementById("zakl_dogovor").innerHTML = srok_td
            } else if (String(treb_deyst) == 'Получение проекта нормативов'){
                $('#proekt_normat').attr('style','text-align: center;background:'+color_td+'; border-radius: 5px;')
                $('#proekt_normat').attr('data-placement','top')
                $('#proekt_normat').attr('data-toggle','tooltip')
                $('#proekt_normat').attr('data-original-title','Ожидается получение проекта нормативов. ' + srok_td)
                document.getElementById("proekt_normat").innerHTML = srok_td
            } else if (String(treb_deyst) == 'Ответ на запрос ТКП'){
                $('#otvet_zapros_tkp').attr('style','text-align: center;background:'+color_td+'; border-radius: 5px;')
                $('#otvet_zapros_tkp').attr('data-placement','top')
                $('#otvet_zapros_tkp').attr('data-toggle','tooltip')
                $('#otvet_zapros_tkp').attr('data-original-title','Подготовка ответа на запрос ТКП. '  + srok_td)
                document.getElementById("otvet_zapros_tkp").innerHTML = srok_td
            } else if (String(treb_deyst) == 'Ответ на письмо о проекте договора'){
                $('#otvet_proekt_dogov_TZ').attr('style','text-align: center;background:'+color_td+'; border-radius: 5px;')
                $('#otvet_proekt_dogov_TZ').attr('data-placement','top')
                $('#otvet_proekt_dogov_TZ').attr('data-toggle','tooltip')
                $('#otvet_proekt_dogov_TZ').attr('data-original-title','Подготовка ответа на письмо о проекте договора. ' + srok_td)
                document.getElementById("otvet_proekt_dogov_TZ").innerHTML = srok_td
            } else if (String(treb_deyst) == 'Ответ на запрос о снижении цены'){
                $('#otvet_snig_cen').attr('style','text-align: center;background:'+color_td+'; border-radius: 5px;')
                $('#otvet_snig_cen').attr('data-placement','top')
                $('#otvet_snig_cen').attr('data-toggle','tooltip')
                $('#otvet_snig_cen').attr('data-original-title','Подготовка ответа на запрос о снижении цены. ' + srok_td)
                document.getElementById("otvet_snig_cen").innerHTML = srok_td
            } else if (String(treb_deyst) == 'Подготовка экспертного заключения'){
                $('#ex_zakl_pismo_RTN').parent().attr('style','text-align: center;background:'+color_td+'; border-radius: 5px;')
                $('#ex_zakl_pismo_RTN').parent().attr('data-placement','top')
                $('#ex_zakl_pismo_RTN').parent().attr('data-toggle','tooltip')
                $('#ex_zakl_pismo_RTN').parent().attr('data-original-title','Подготовка экспертного заключения. ' + srok_td)
                document.getElementById("ex_zakl_pismo_RTN").innerHTML = srok_td
            } else if (String(treb_deyst) == 'Оформление Акта'){
                $('#akt').attr('style','text-align: center;background:'+color_td+'; border-radius: 5px;')
                $('#akt').attr('data-placement','top')
                $('#akt').attr('data-toggle','tooltip')
                $('#akt').attr('data-original-title','Подготовка Акта сдачи-приемки')
                document.getElementById("akt").innerHTML = 'ЭЗ утверждено ' +data.data_document+'</br> Ожидается оформление Акта'
            } else if (String(treb_deyst) == 'Основные документы загружены'){
                $('#pismo_v_rtn').attr('style','text-align: center;background:'+color_td+'; border-radius: 5px;')
                $('#pismo_v_rtn').attr('data-placement','top')
                $('#pismo_v_rtn').attr('data-toggle','tooltip')
                $('#pismo_v_rtn').attr('data-original-title','Подготовка письма в Ростехнадзор (или территориальный орган).' + srok_td )
                document.getElementById("pismo_v_rtn").innerHTML = srok_td

                $('#pismo_v_org').attr('style','text-align: center;background:'+color_td+'; border-radius: 5px;')
                $('#pismo_v_org').attr('data-placement','top')
                $('#pismo_v_org').attr('data-toggle','tooltip')
                $('#pismo_v_org').attr('data-original-title','Подготовка письма в организацию.' + srok_td )
                document.getElementById("pismo_v_org").innerHTML = srok_td
            } else if (String(treb_deyst) == 'Подготовка писем в РТН/ТО и организацию'){
                $('#pismo_v_rtn').attr('style','text-align: center;background:'+color_td+'; border-radius: 5px;')
                $('#pismo_v_rtn').attr('data-placement','top')
                $('#pismo_v_rtn').attr('data-toggle','tooltip')
                $('#pismo_v_rtn').attr('data-original-title','Подготовка письма в Ростехнадзор (или территориальный орган).' + srok_td )
                document.getElementById("pismo_v_rtn").innerHTML = srok_td

                $('#pismo_v_org').attr('style','text-align: center;background:'+color_td+'; border-radius: 5px;')
                $('#pismo_v_org').attr('data-placement','top')
                $('#pismo_v_org').attr('data-toggle','tooltip')
                $('#pismo_v_org').attr('data-original-title','Подготовка письма в организацию.' + srok_td )
                document.getElementById("pismo_v_org").innerHTML = srok_td
            } else if (String(treb_deyst) == 'Все документы подгружены'){
                $('#tip_deystviya').attr('class','success')
                
            } else if (String(treb_deyst) == 'Ожидание проекта нормативов'){
                $('#pismo_rtn_o_ex').attr('style','text-align: center;background:'+color_td+'; border-radius: 5px;')
                $('#pismo_rtn_o_ex').attr('data-placement','top')
                $('#pismo_rtn_o_ex').attr('data-toggle','tooltip')
                $('#pismo_rtn_o_ex').attr('data-original-title','Ожидание письма из Ростехнадзора или территориального органа с проектом нормативов.' + srok_td )
                document.getElementById("pismo_rtn_o_ex").innerHTML = srok_td
                
                $('#proekt_normat').attr('style','text-align: center;background:'+color_td+'; border-radius: 5px;')
                $('#proekt_normat').attr('data-placement','top')
                $('#proekt_normat').attr('data-toggle','tooltip')
                $('#proekt_normat').attr('data-original-title','Ожидается получение проекта нормативов. ' + srok_td)
                document.getElementById("proekt_normat").innerHTML = srok_td
            } else if (String(treb_deyst) == 'Направление по договору'){
                $('#pismo_v_org').attr('style','text-align: center;background:'+color_td+'; border-radius: 5px;')
                $('#pismo_v_org').attr('data-placement','top')
                $('#pismo_v_org').attr('data-toggle','tooltip')
                $('#pismo_v_org').attr('data-original-title','Подготовка письма в организацию с комплектом документов по договору ' + srok_td )

                $('#akt').attr('style','text-align: center;background:'+color_td+'; border-radius: 5px;')
                $('#akt').attr('data-placement','top')
                $('#akt').attr('data-toggle','tooltip')
                $('#akt').attr('data-original-title','Подготовка Акта сдачи-приемки ' + srok_td )
            } else if (String(treb_deyst) == 'Ожидается подписанный Акт'){
                $('#akt').attr('style','text-align: center;background:'+color_td+'; border-radius: 5px;')
                $('#akt').attr('data-placement','top')
                $('#akt').attr('data-toggle','tooltip')
                $('#akt').attr('data-original-title','От организации ожидается подписанный Акт сдачи-приемки ' + srok_td )
            }
            document.getElementById("redact_id").setAttribute("href", '/admin/Expertize/cexpertiza/'+String(aa)+'/change/')  
        },
        error: function(data){
            alert('Ajax-скрипт модального окна в экспертизе не сработал')
        },
    })
}

var modal = document.getElementById('myModal');

$("#close").click(function(){
    modal.style.display = "none";
    $('.modal-content').attr("style","animation-name : animatetop;")
})


function Clear_all_ex(){
    document.getElementById('opisanie_color1').setAttribute('name','')
    document.getElementById('opisanie_color2').setAttribute('name','')
    document.getElementById('opisanie_color3').setAttribute('name','')
    $('#btn_srok_arch')[0].className = 'btn btn-default dropdown-toggle'
    $('#btn_srok_arch')[0].innerHTML = '<div id=\"id_range\">Вывести все сроки</div>\n<span class=\"bs-caret\"><span class=\"caret\"></span></span>\n'

    $('#vibros_checkbox').removeClass('active')
    $('#sbros_checkbox').removeClass('active')
    $('#vibros_checkbox').attr('name','')
    $('#sbros_checkbox').attr('name','')
    $('#id_tip_all').attr('name','active')
    $('#id_tip_all').addClass('active')

    $('#otvet_ex').removeClass('active')
    $('#zapros_ex').removeClass('active')
    $('#vse_ex').removeClass('active')
    $('#vse_ex').addClass('active')

    Vse_ex()
}


