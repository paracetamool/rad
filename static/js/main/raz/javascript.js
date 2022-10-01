
var now = new Date();

moment.updateLocale(moment.locale(), { invalidDate: "Invalid Date Example" });

var MainTable = $('#id_table_raz').DataTable({
        processing: true,
        ajax : {
            url : '/get_table_razreshenie_data/',
            data : function(d) {
                d.tip_razresheniya_1 = $('#id_tip_vibros').attr('name');
                d.tip_razresheniya_2 = $('#id_tip_sbros').attr('name');
                d.name_organ = CheckboxFilter.name_organ;
                d.srok1 = $('#opisanie_color1').attr('name');
                d.srok2 = $('#opisanie_color2').attr('name');
                d.srok3 = $('#opisanie_color3').attr('name');
            }
        },
        paging: true,
        bFilter: true,
        ordering: true,
        searching: true,
        "sDom":"ltip",
        language: {url: "/static/DataTables/json/custom.json"},
        scrollY: "calc(100vh - 290px)",
        lengthMenu: [[20, 25, 50, 100, -1], [20, 25, 50, 100, "Все"]],
        order: [[ 3, "asc" ]],
        aaSorting : [[3, 'desc']],
        dom:
        `<'row'<'col-sm-4'><'col-sm-2 text-right'>>
        <'row'<'col-sm-12'tr>>
        <'row'<'col-sm-5'><'col-sm-7'p>>`,
        columnDefs: [
            {
            targets: 4,
            render: $.fn.dataTable.render.moment('YYYY-MM-DD','DD.MM.YYYY'  )
        },
        {
            targets: 5,
            render: $.fn.dataTable.render.moment('DD.MM.YYYY','DD.MM.YYYY'  )
        },
        {
            targets: 1,
            "visible": false,
        }
        ],

        initComplete: function(){
            $('button.btn.dropdown-toggle.btn-default.bs-placeholder').attr('style','border-radius:0;')
            $('button#btn_srok_arch.btn.btn-default.dropdown-toggle').attr('style','border-radius: 0;')

            $('#dropdown_name_organ').on("click",function(){
                $(this).find('.dropdown-menu')[0].attributes.style.value = "width: 350px; padding-top: 0px; overflow: visible;" 
                
            })

            
        },
        "createdRow": function( row, data, dataIndex ) {
            N_M = now.getMonth()
            N_Y = now.getFullYear()
            R_M = Number(data[5].slice(3,5))
            R_Y = Number(data[5].slice(6,10))
            V_Y = R_Y - N_Y
            if (V_Y < 0) {
                $(row).addClass("danger")
            } else if (V_Y == 0) {
                if (N_M < R_M) {
                    $(row).addClass("warning")
                } else {
                    $(row).addClass("danger")
                }
            } else  {
                if (V_Y > 1){
                    $(row).addClass("success")
                } else{
                    if (((12 - N_M) + R_M) <= 12) {
                        $(row).addClass("warning")
                    } else {
                        $(row).addClass("success")
                    }
                }
            }
        },
        drawCallback: function(settings) {
            var pagination = $(this).closest('.dataTables_wrapper').find('.dataTables_paginate')
            pagination.toggle(this.api().page.info().pages > 1)
            $('[role="tooltip"]').remove()
        },          
    })

    MainTable.on( 'order.dt search.dt ', function () {
        MainTable.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = '<div>' + String(i+1) + '</div>';
        } );
    } ).draw();

    var buttons = new $.fn.dataTable.Buttons(MainTable, {
        buttons: [
            {
                extend   : 'excelHtml5',
                text     : '<i class="fa fa-file-excel-o"></i>',
                titleAttr: 'Сохранить в Excel',
                attr: {
                    'data-toggle':'tooltip',
                },
                filename:'Архив Разрешений',
                customize: function( xlsx, row ) {
                    var sheet = xlsx.xl.worksheets['sheet1.xml'];
                    $('row c[r^="D"], row c[r^="G"]', sheet).attr( 's', 50);
                    $('row:eq(0) c', sheet).attr( 's', 2 );
                    for (i=1;i<=1000;i++){
                        $('c[r=A'+String(i+2)+'] t', sheet).text( String(i) );
                    }
                },
                exportOptions: {
                    columns: [1,2,3,4,5,6,7,8]
                },
                autoFilter:true,
            },
            {
                extend   : 'pdf',
                text     : '<i class="fa fa-file-pdf-o"></i>',
                titleAttr: 'Сохранить в PDF',
                attr: {
                    'data-toggle':'tooltip',
                },
                filename:'Архив Разрешений',
                exportOptions: {
                    columns: [0,2,3,4,5,6,7,8]
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
                filename:'Архив Разрешений',
                exportOptions: {
                    columns: [2,3,4,5,6,7,8]
                },
                // customize: function(window){
                //     var Len = window.document.querySelectorAll("tbody tr").length
                //     for (let i=0;i<Len;i++){
                //         console.log(window.document.querySelectorAll("tbody tr td:first-child")[i].innerHTML = i+1)
                //     }
                // }
            },
        ]
    }).container().appendTo($('#bt_copy_xl_pdf'));

    MainTable.order( [5,'asc'] ).draw();
    $('#poisk').keyup(function(){
        MainTable.search($(this).val()).draw() ;
    })
/**-------------------------- */

    function updateDataVibros() {
        document.getElementById('id_tip_vibros').setAttribute('name','active')
        document.getElementById('id_tip_sbros').setAttribute('name','')
        document.getElementById('th_tip_razr').setAttribute('data-orderable','false')
        MainTable.ajax.reload()
    }

    function updateDataSbros() {
        document.getElementById('id_tip_vibros').setAttribute('name','')
        document.getElementById('id_tip_sbros').setAttribute('name','active')
        document.getElementById('th_tip_razr').setAttribute('data-orderable','false')
        MainTable.ajax.reload()
    }

    function updateDataAll() {
        document.getElementById('id_tip_vibros').setAttribute('name','')
        document.getElementById('id_tip_sbros').setAttribute('name','')
        document.getElementById('th_tip_razr').setAttribute('data-orderable','true')
        MainTable.ajax.reload()
    }

    $('#id_tip_vibros').click( function vivod () {
        updateDataVibros()
    });

    $('#id_tip_sbros').click( function vivod () { 
        updateDataSbros()
    });

    $('#id_tip_all').click( function vivod () { 
        updateDataAll()
    });


    $(document).on('change', 'select.label-picker', function () {
        CheckboxFilter['name_organ'] = $(this).val()
        MainTable.ajax.reload()
    })

    //----------------------------------------------//

    $('.bt_all').on('click',function(){
        $('#opisanie_color1').attr('name','');
        $('#opisanie_color2').attr('name','');
        $('#opisanie_color3').attr('name','');
        $('#btn_srok_arch')[0].className = 'btn btn-default dropdown-toggle'
        $('#btn_srok_arch')[0].innerHTML = '<div id=\"id_range\">Вывести все сроки</div>\n<span class=\"bs-caret\"><span class=\"caret\"></span></span>\n'
        MainTable.ajax.reload()
    })

    $('.bt_success').on('click',function(){
        $('#opisanie_color1').attr('name','active');
        $('#opisanie_color2').attr('name','');
        $('#opisanie_color3').attr('name','');
        $('#btn_srok_arch')[0].className = 'btn bt_success dropdown-toggle'
        $('#btn_srok_arch')[0].innerHTML = '<div id=\"id_range\">Больше года</div>\n<span class=\"bs-caret\"><span class=\"caret\"></span></span>\n'
        MainTable.ajax.reload()
    })

    $('.btn_warning').on('click',function(){
        $('#opisanie_color1').attr('name','');
        $('#opisanie_color2').attr('name','active');
        $('#opisanie_color3').attr('name','');
        $('#btn_srok_arch')[0].className = 'btn btn_warning dropdown-toggle'
        $('#btn_srok_arch')[0].innerHTML = '<div id=\"id_range\">Меньше года</div>\n<span class=\"bs-caret\"><span class=\"caret\"></span></span>\n'
        MainTable.ajax.reload()
    })


    $('.btn_danger').on('click',function(){
        $('#opisanie_color1').attr('name','');
        $('#opisanie_color2').attr('name','');
        $('#opisanie_color3').attr('name','active');
        $('#btn_srok_arch')[0].className = 'btn btn_danger dropdown-toggle'
        $('#btn_srok_arch')[0].innerHTML = '<div id=\"id_range\">Истек</div>\n<span class=\"bs-caret\"><span class=\"caret\"></span></span>\n'
        MainTable.ajax.reload()
    })

    $('#dropdown_name_organ').on("click",function(){
        $(this).find('.dropdown-menu')[0].attributes.style.value = "width: 320px; padding-top: 0px; overflow: visible;" 
        
    })
    

/**-------------------------- */
function Clear_all(){

    // $('.selectpicker option:selected').removeAttr('selected')
    // $('#id_select_organiz').selectpicker('refresh')

    $('.selectpicker').selectpicker('val', 'Организации'); // второй способ, первый в архиве

    $('#id_tip_sbros').removeClass()
    $('#id_tip_sbros').addClass('btn btn-sm btn-default')
    $('#id_tip_sbros').attr('name','');

    $('#id_tip_vibros').removeClass()
    $('#id_tip_vibros').addClass('btn btn-sm btn-default')
    $('#id_tip_vibros').attr('name','');

    $('#id_tip_all').removeClass()
    $('#id_tip_all').addClass('btn btn-sm btn-default active')
    CheckboxFilter['name_organ'] = []

    MainTable.search('').draw()
    $('#poisk').val('')

    $('#opisanie_color1').attr('name','');
    $('#opisanie_color2').attr('name','');
    $('#opisanie_color3').attr('name','');
    $('#btn_srok_arch')[0].className = 'btn btn-default dropdown-toggle'
    $('#btn_srok_arch')[0].innerHTML = '<div id=\"id_range\">Вывести все сроки</div>\n<span class=\"bs-caret\"><span class=\"caret\"></span></span>\n'
    
    MainTable.ajax.reload()
    

 

    // $('div.filter-option-inner-inner').innerHTML = 'Организации'
    // console.log($('.filter-option-inner-inner'))
    
    // CheckboxFilter['name_organ'] = []
    // MainTable.search('').draw()
    // MainTable.ajax.reload()



}

//------------------Функции за модальныое окно Разрешений------------------- // 
function ModalWindow(a) {

    $.ajax({
        method : "GET",
        url : '/get_modal_table_razresheniya/',
        data : {
            'id_raz': a
        },
        dataType: 'json',
        success: function(data){
            if (data.kolvo_expertiz == 1){
                document.getElementById("btn_drugie_raz").setAttribute("class","btn btn-default btn-sm disabled")
                var ul = document.getElementById("drop_down_raz")
                ul.innerHTML = ''
            } else {
                document.getElementById("btn_drugie_raz").setAttribute("class","btn btn-primary dropdown-toggle")
                var ul = document.getElementById("drop_down_raz")
                ul.innerHTML = ''
                data.drugie_razreshen.forEach(function(entry){
                    var ul = document.getElementById("drop_down_raz")
                    li = document.createElement("li")
                    if (data.data_vidachi == entry[1]){
                        li.setAttribute("style","background:#D2D2D2; ")
                        li.innerHTML = '<a onclick="NewRazreshenie(' + String(entry[2]) + ')" href="#"> от ' + entry[1] + ' № '+ entry[0]  +'</a>'
                    } else {
                        li.innerHTML = '<a onclick="NewRazreshenie(' + String(entry[2]) + ')" href="#"> от ' + entry[1] + ' № '+ entry[0]  +'</a>'
                    }
                    ul.appendChild(li)
                })
            }

            if (data.actual == 'актуальное'){
                $('#actual').html('')
            } else{
                $('#actual').html('Внимание - не действующее разрешение!')
            }
            document.getElementById("name-zagolovok").innerHTML = data.name_polnoe
            document.getElementById("tip_raz").innerHTML = data.tip_razresheniya
            document.getElementById("nomer_raz").innerHTML = data.nomer_razresheniya
            document.getElementById("vidano_raz").innerHTML = data.kem_vidano
            document.getElementById("nomer_raz").setAttribute("href", data.fayl_url_raz)
            
            if (data.fayl_url_expert_zakl == undefined) {
                document.getElementById("fayl_expertn_zakl").setAttribute("style", 'pointer-events: none;color:black;')
                document.getElementById("fayl_expertn_zakl").innerHTML = 'Экспертное заключение отсутствует. Работа выполнена не ФБУ «НТЦ ЯРБ»'
            } else {
                document.getElementById("fayl_expertn_zakl").innerHTML = 'ДНП '+data.DNP
                document.getElementById("fayl_expertn_zakl").setAttribute("style", 'pointer-events: auto;color:#6299c8;')
                document.getElementById("fayl_expertn_zakl").setAttribute("href", data.fayl_url_expert_zakl)
            }
    
            if (data.tip_razresheniya == 'Разрешение на выброс радиоактивных веществ в атмосферный воздух'){
                document.getElementById("fayl_proekta_norm").innerHTML = 'Нормативы ПДВ РВ'
            } else {
                document.getElementById("fayl_proekta_norm").innerHTML = 'Нормативы ДС РВ'
            }
            
            if ( data.fayl_url_proekta_normat == undefined) {
                document.getElementById("fayl_proekta_norm").setAttribute("style", 'pointer-events: none;color:black;')
            } else {
                document.getElementById("fayl_proekta_norm").setAttribute("style", 'pointer-events: auto;color:#6299c8;')
                document.getElementById("fayl_proekta_norm").setAttribute("href", data.fayl_url_proekta_normat)
            }

            document.getElementById("organizovannie_raz").innerHTML = Number(data.vse_istochniki) - Number(data.neorganizovannie_istochniki)
            document.getElementById("neorganizovannie_raz").innerHTML = Number(data.neorganizovannie_istochniki)
            document.getElementById("vsego_istochnikov_raz").innerHTML = Number(data.vse_istochniki)
            if (data.prochaya_inf == ''){
                document.getElementById('tr_prochaya_inf').style.display = "none";
            } else{
                document.getElementById('tr_prochaya_inf').style.display = "";
                document.getElementById("prochaya_inf").innerHTML = data.prochaya_inf
            }
            document.getElementById("vidachi_raz").innerHTML = data.data_vidachi
            document.getElementById("nachalo_raz").innerHTML = data.data_nachala
            document.getElementById("konec_raz").innerHTML = data.data_okonchaniya


            // document.getElementById("redact_expertizi").setAttribute("onclick", '')
        },
        error: function(data){
        }
    })
}


function NewRazreshenie(id_exp){
    ModalWindow(id_exp)
}


var modal = document.getElementById('myModal');

$("#close").click(function(){
    modal.style.display = "none";
    $('.modal-content').attr("style","animation-name : animatetop;")
})


$('#Clear_all_raz').attr('style','border-radius: 0  3px 3px 0 ')



