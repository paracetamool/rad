moment.updateLocale(moment.locale(), { invalidDate: "Invalid Date Example" });

    var MainTable = $('#id_table_raz').DataTable({
            processing: true,
            scrollY: "calc(100vh - 290px)",
            ajax : {
                url : '/get_table_archive_data/',
                data : function(d) {
                    d.input_data_start_day = CheckboxFilter.data_start_day
                    d.input_data_end_day = CheckboxFilter.data_end_day
                    d.input_data_start_year = CheckboxFilter.data_start_year
                    d.input_data_end_year = CheckboxFilter.data_end_year
                    d.name_organ = CheckboxFilter.name_organ;
                    d.sbros_name = CheckboxFilter.sbros;
                    d.vibros_name = CheckboxFilter.vibros;
                },
            },
            dom: `
                <'row'<'col-sm-12'tr>>
                <'row'<'col-sm-5'><'col-sm-7'p>>`,
            columnDefs: [
                {
                    targets: 6,
                    render: $.fn.dataTable.render.moment('DD.MM.YYYY','DD.MM.YYYY'  )
                }],
            buttons: {
                dom: {buttonLiner: { tag: null }},

            },
            initComplete : function(){
                $('#sbros_checkbox').on("click", function(){
                    CheckboxFilter['sbros'] = 'active'
                    CheckboxFilter['vibros'] = ''
                    ReloadTable()
                })

                $('#vibros_checkbox').on("click", function(){
                    CheckboxFilter['sbros'] = ''
                    CheckboxFilter['vibros'] = 'active'
                    ReloadTable()
                })

                $('#all_checkbox').on("click", function(){
                    CheckboxFilter['sbros'] = ''
                    CheckboxFilter['vibros'] = ''
                    ReloadTable()
                })
 
                $('input[id^="id_input_data_"]').datetimepicker(window.location.pathname.includes('search_annual_reports') ? datepickerOpt2 : datepickerOpt1).mask(window.location.pathname.includes('search_annual_reports') ? "0000" : "00.00.0000", window.location.pathname.includes('search_annual_reports') ? dateMaskOpt2 : dateMaskOpt1);
                //---------------------------------
                $('.selectpicker option:selected').removeAttr('selected')
                $('#id_select_organiz').selectpicker('refresh')
                
                CheckboxFilter['name_organ'] = []

                //---Проверяю применение скрипта по времени (заполенние невидимых дивов в шаблоне по мере изменения значения инпута сроков)--------------------
                
                $(document).on('change', '#id_range', function () {
                    CheckboxFilter['data'] = $(this).val()
                })
                //---------------------------------
                $('#dropdown_name_organ').on("click",function(){
                    $(this).find('.dropdown-menu')[0].attributes.style.value = "width: 350px; padding-top: 0px; overflow: visible;" 
                    
                })

                $('button.btn.dropdown-toggle.btn-default.bs-placeholder').attr('style','border-radius:0;')
                $('button#btn_srok_arch.btn.btn-default.dropdown-toggle').attr('style','border-radius: 0;')


            },
            language: {url: "/static/DataTables/json/custom.json"},
            lengthMenu: [[20, 25, 50, 100, -1], [20, 25, 50, 100, "Все"]],
            order: [[ 0, "asc" ]],
            drawCallback: function(settings) {
                var pagination = $(this).closest('.dataTables_wrapper').find('.dataTables_paginate')
                pagination.toggle(this.api().page.info().pages > 1)
                $('[role="tooltip"]').remove()
            }, 
    })

    MainTable.on( 'order.dt search.dt print.dt', function () {
        MainTable.column(0, {search:'applied', order:'applied'}).nodes().each( function (cell, i) {
            cell.innerHTML = i+1;
        } );
    } ).draw();
    
    var buttons = new $.fn.dataTable.Buttons(MainTable, {
        buttons: [
            {
                extend   : 'excel',
                text     : '<i class="fa fa-file-excel-o"></i>',
                titleAttr: 'Сохранить в Excel',
                attr: {
                    'data-toggle':'tooltip',
                },
                title: '',
                filename:'Архив экспертных заключений',
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
                extend   : 'pdf',
                text     : '<i class="fa fa-file-pdf-o"></i>',
                titleAttr: 'Сохранить в PDF',
                attr: {
                    'data-toggle':'tooltip',
                },
                filename:'Архив экспертных заключений',
                exportOptions: {
                    columns: [0,1,2,3,4,5,6]
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
                title: '',
                exportOptions: {
                    columns: [0,1,2,3,4,5,6]
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
        /**------------------------------------------- */
    MainTable.order( [6,'desc'] ).draw();
        /**------------------------------------------- */


    $('#poisk').keyup(function(){
        MainTable.search($(this).val()).draw() ;
    })

    function ReloadTable() {
        MainTable.ajax.reload()
        
    }
    $(document).on('change', 'select.label-picker', function () {
        CheckboxFilter['name_organ'] = $(this).val()
        MainTable.ajax.reload()
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


    /*------------------------Скрипт по выводу информации в модальном окне во вкладке Архив--------------------------*/
    function Inform_Ex_archive(id_exp){
    
        $.ajax({
            method : "GET",
            url : '/get_modal_table_archive/',
            data : {
                'id_ex_arch': id_exp,
            },
            dataType: 'json',
            success: function(data){
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
                //------------------------------
                $('#nav_pills_expertiza').attr('class','active')
                $('#menu1').attr('class','tab-pane fade in active')
                $('#nav_pills_process').attr('class','')
                $('#menu2').attr('class','tab-pane fade')

                //-----------------------------

                document.getElementById("organizovannie_ex").innerHTML = Number(data.vse_istochniki) - Number(data.neorg_istochniki)
                document.getElementById("neorganizovannie_ex").innerHTML = data.neorg_istochniki
                document.getElementById("vsego_istochnikov_ex").innerHTML = data.vse_istochniki

                if (Number(String(data.data_utvergd.slice(6, 10)))>=2019){
                    document.getElementById("admin_rtn").style.display = "";
                    document.getElementById("admin_tkp").style.display = "";
                    document.getElementById("admin_org").style.display = "";
                } else{
                    document.getElementById("admin_rtn").style.display = "none";
                    document.getElementById("admin_tkp").style.display = "none";
                    document.getElementById("admin_org").style.display = "none";
                }
                // Выставление навазния файлов(ссылок) в модальном окне
                url_pismo_rtn1 = data.url_pismo_rtn
                id_pismo_rtn1 = 'pismo_rtn_o_ex2'
                list_pismo_rtn1 =  data.list_pismo_rtn
                list_name1 = 'Письмо из РТН / ТО'.split(" ")
                ChangeSybmol(url_pismo_rtn1,id_pismo_rtn1,list_pismo_rtn1,list_name1)

                url_pismo_v_rtn2 = data.url_pismo_v_rtn
                id_pismo_rtn2 = "pismo_v_rtn"
                list_pismo_v_rtn2 =  data.list_pismo_v_rtn
                list_name2 = 'Письмо в РТН / ТО'.split(" ")
                ChangeSybmol(url_pismo_v_rtn2,id_pismo_rtn2,list_pismo_v_rtn2,list_name2)

                url_pismo_org3= data.url_pismo_org
                id_pismo_org3 = "pismo_org"
                list_pismo_ot_org3 =  data.list_pismo_ot_org
                list_name3 = 'Письмо из организации'.split(" ")
                ChangeSybmol(url_pismo_org3,id_pismo_org3,list_pismo_ot_org3,list_name3)

                url_pismo_org4= data.url_pismo_v_org
                id_pismo_org4 = "pismo_v_org"
                list_pismo_v_org4 =  data.list_pismo_v_org
                list_name4 = 'Письмо в организацию'.split(" ")
                ChangeSybmol(url_pismo_org4,id_pismo_org4,list_pismo_v_org4,list_name4)

                url_zapros_tkp5= data.url_zapros_tkp1
                id_zapros_tkp5 = "zapros_tkp2"
                list_list_zapros_tkp5 =  data.list_zapros_tkp
                list_name5 = 'Запрос ТКП'.split(" ")
                ChangeSybmol(url_zapros_tkp5,id_zapros_tkp5,list_list_zapros_tkp5,list_name5)

                url_otvet_tkp6= data.url_otvet_tkp
                id_otvet_zapros_tkp6 = "otvet_zapros_tkp2"
                list_otvet_tkp6 =  data.list_otvet_tkp
                list_name6 = 'Ответ ТКП'.split(" ")
                ChangeSybmol(url_otvet_tkp6,id_otvet_zapros_tkp6,list_otvet_tkp6,list_name6)

                url_zakl_dogov7= data.url_zakl_dogov
                id_zakl_dogovor7 = "zakl_dogovor2"
                list_zakl_dogovor7 =  data.list_zakl_dogovor
                list_name7 = 'Заключенный договор'.split(" ")
                ChangeSybmol(url_zakl_dogov7,id_zakl_dogovor7,list_zakl_dogovor7,list_name7)

                url_Ex_zakl8= data.url_Ex_zakl
                id_ex_zakl8 = "ex_zakl"
                list_expertn_zakl8 =  data.list_expertn_zakl
                list_name8 = ('ДНП '+ data.nomer_DNP).split(" ")
                ChangeSybmol(url_Ex_zakl8,id_ex_zakl8,list_expertn_zakl8,list_name8)

                url_proekt_norm9= data.url_proekt_norm
                id_proekt_normat9 = "proekt_normat2"
                list_proekt_normat9 =  data.list_proekt_normat
                if (data.gos_usluga == 'Разрешение на выброс радиоактивных веществ в атмосферу'){
                    list_name9 = 'Нормативы ПДВ РВ'.split(" ")
                } else{
                    list_name9 = 'Нормативы ДС РВ'.split(" ")
                }
                ChangeSybmol(url_proekt_norm9,id_proekt_normat9,list_proekt_normat9,list_name9)

                url_act10= data.url_act
                id_act10 = "act_sdacha-priem2"
                list_akt10 =  data.list_akt
                list_name10 = 'АКТ'.split(" ")
                ChangeSybmol(url_act10,id_act10,list_akt10,list_name10)
                //  -------

                document.getElementById("utvergdeno_zakl").innerHTML = data.full_name_utvergd.join("") 
                document.getElementById("ruk_raboti").innerHTML = data.full_name_ruk.join("") 
                document.getElementById("ruk_podrazdel").innerHTML = data.full_name_ruk_podraz.join("") 
                document.getElementById("experti").innerHTML = data.full_name_exp.join("") 
                document.getElementById("name_zagolovok2").innerHTML = data.nazvanie_polnoe 
                document.getElementById("tip_raz2").innerHTML = data.gos_usluga
                document.getElementById("vidachi_raz2").innerHTML = data.data_utvergd
                document.getElementById("redact_id").setAttribute("href", '/admin/Expertize/cexpertiza/'+String(id_exp)+'/change/')
            },
            // error: function(data){
            //     console.log('не оке')
            // }
        })
    }

    var modal = document.getElementById('myModal');

    $("#close").click(function(){
        modal.style.display = "none";
        $('.modal-content').attr("style","animation-name : animatetop;")
    })

    /**--------------------------- --------------------------- --------------------------------- */

    //___________________Выброс и Сброс Checkbox____________________________

$('#vibros_checkbox').on("click",function(){
    $('#sbros_checkbox').removeClass('active')
    if ($(this)[0].attributes.class.value == 'btn btn-default btn-sm'){
        $(this).attr('name','active')
        $('#sbros_checkbox').attr('name','')
        
    } else{
        $(this).attr('name','')
        $('#sbros_checkbox').attr('name','')
    }
    MainTable.ajax.reload()
})

$('#sbros_checkbox').on("click",function(){
    $('#vibros_checkbox').removeClass('active')
    if ($(this)[0].attributes.class.value == 'btn btn-default btn-sm'){
        $(this).attr('name','active')
        $('#vibros_checkbox').attr('name','')
    } else{
        $('#vibros_checkbox').attr('name','')
        $(this).attr('name','')
    }
    MainTable.ajax.reload()
})
    /**--------------------------- --------------------------- --------------------------------- */
    function Clear_all() {
        MainTable.search('').draw()

        $('#id_input_data_start').val('')
        $('#id_input_data_end').val('')
        $('#id_range').attr("style","color: rgb(153, 153, 153);")
        $('#id_range').text('Временной интервал') 

        $('.selectpicker option:selected').removeAttr('selected')
        $('#id_select_organiz').selectpicker('refresh') // первый способ, второй в разрешениях

        CheckboxFilter['name_organ'] = []

        $('#vibros_checkbox').removeClass('active')
        $('#vibros_checkbox').removeClass('focus')
        $('#vibros_checkbox').attr('name','')
        $('#sbros_checkbox').removeClass('active')
        $('#sbros_checkbox').removeClass('focus')
        $('#sbros_checkbox').attr('name','')
        $('#all_checkbox').addClass('active')

        CheckboxFilter['sbros'] = ''
        CheckboxFilter['vibros'] = ''

        CheckboxFilter['data_start_day'] = ''
        CheckboxFilter['data_end_day'] = ''
        CheckboxFilter['data_start_year'] = ''
        CheckboxFilter['data_end_year'] = ''
        $('#id_input_start_day').val('')
        $('#id_input_end_day').val('')
        $('#id_input_start_year').val('')
        $('#id_input_end_year').val('')

        MainTable.order( [6,'desc'] ).draw();
        MainTable.ajax.reload()

        MainTable.search('').draw()
        $('#poisk').val('')
    }


    function Clear_data(){
        CheckboxFilter['data_start_day'] = ''
        CheckboxFilter['data_end_day'] = ''
        CheckboxFilter['data_start_year'] = ''
        CheckboxFilter['data_end_year'] = ''
        document.getElementById("id_input_year_data_start").value = ""
        document.getElementById("id_input_year_data_end").value = ""
        document.getElementById("id_input_data_start").value = ""
        document.getElementById("id_input_data_end").value = ""
        document.getElementById("id_range").innerHTML = "Временной интервал"
        document.getElementById("id_range").setAttribute("style", 'color:#999999;' )
        MainTable.ajax.reload()
        
    }
    // --------------------Стилизация для кнопок по времени в DropDown-------------------------
    $('.dropdown').on('click', '.dropdown-menu > div > div > label', function(e) {
        e.preventDefault();
        e.stopPropagation();
    });

    $('#god_checkbox').on('click', function(){
        CheckboxFilter['data_start_day'] = ''
        CheckboxFilter['data_end_day'] = ''
        CheckboxFilter['data_start_year'] = ''
        CheckboxFilter['data_end_year'] = ''
        $('#id_input_start_day').val('')
        $('#id_input_end_day').val('')
        $('#id_input_start_year').val('')
        $('#id_input_end_year').val('')

        $('#tr_data_day').attr('style','display:none')
        $('#tr_data_year').attr('style','display:')
        
        $('#den_checkbox').removeClass('active')
        if ($(this)[0].attributes.class.value == 'btn btn-default btn-sm'){
            $('#god_checkbox').addClass('active')
        } 
        $('#god_checkbox').attr('name','active')
        $('#den_checkbox').attr('name','')
        document.getElementById("id_range").innerHTML = "Временной интервал"
        document.getElementById("id_range").setAttribute("style", 'color:#999999;' )
        MainTable.ajax.reload()
    })

    $('#den_checkbox').on('click', function(){
        CheckboxFilter['data_start_day'] = ''
        CheckboxFilter['data_end_day'] = ''
        CheckboxFilter['data_start_year'] = ''
        CheckboxFilter['data_end_year'] = ''
        $('#id_input_start_day').val('')
        $('#id_input_end_day').val('')
        $('#id_input_start_year').val('')
        $('#id_input_end_year').val('')

        $('#tr_data_year').attr('style','display:none')
        $('#tr_data_day').attr('style','display:')

        $('#god_checkbox').removeClass('active')
        if ($(this)[0].attributes.class.value == 'btn btn-default btn-sm'){
            $('#den_checkbox').addClass('active')
        } 
        $('#den_checkbox').attr('name','active')
        $('#god_checkbox').attr('name','')
        document.getElementById("id_range").innerHTML = "Временной интервал"
        document.getElementById("id_range").setAttribute("style", 'color:#999999;' )
        MainTable.ajax.reload()
    })


    $('#clear_data_checkbox').on('click', function(){
        $('#tr_data_day').attr('style','display:none')
        $('#tr_data_year').attr('style','display:')
        $('#den_checkbox').attr('name','')
        $('#god_checkbox').attr('name','active')
        $('#den_checkbox').removeClass('active')
        $('#god_checkbox').removeClass('active')
        $('#god_checkbox').addClass('active')
        CheckboxFilter['data_start_day'] = ''
        CheckboxFilter['data_end_day'] = ''
        CheckboxFilter['data_start_year'] = ''
        CheckboxFilter['data_end_year'] = ''
        $('#id_input_start_day').val('')
        $('#id_input_end_day').val('')
        $('#id_input_start_year').val('')
        $('#id_input_end_year').val('')
        document.getElementById("id_range").innerHTML = "Временной интервал"
        document.getElementById("id_range").setAttribute("style", 'color:#999999;' )
        MainTable.ajax.reload()
    })

    
    $('#id_input_start_day').on("blur", function(){
        CheckboxFilter['data_start_day'] = $(this).val()
        CheckboxFilter['data_end_day'] = $('#id_input_end_day').val()
        CheckboxFilter['data_start_year'] = ''
        CheckboxFilter['data_end_year'] = ''
        MainTable.ajax.reload()
    })


    $('#id_input_end_day').on("blur", function(){
        CheckboxFilter['data_end_day'] = $(this).val()
        CheckboxFilter['data_start_day'] = $('#id_input_start_day').val()
        CheckboxFilter['data_start_year'] = ''
        CheckboxFilter['data_end_year'] = ''
        MainTable.ajax.reload()
    })


    $('#id_input_start_year').on("blur", function(){
        CheckboxFilter['data_start_year'] = $(this).val()
        CheckboxFilter['data_end_year'] = $('#id_input_end_year').val()
        CheckboxFilter['data_start_day'] = ''
        CheckboxFilter['data_end_day'] = ''
        MainTable.ajax.reload()
    })


    $('#id_input_end_year').on("blur", function(){
        CheckboxFilter['data_end_year'] = $(this).val()
        CheckboxFilter['data_start_year'] = $('#id_input_start_year').val()
        CheckboxFilter['data_start_day'] = ''
        CheckboxFilter['data_end_day'] = ''

        MainTable.ajax.reload()
    })
    // ---------------------------------------------
    $('#Clear_all_arch').attr('style','border-radius: 0  3px 3px 0 ')
    // setTimeout(function() { console.log('123123113')},1000)