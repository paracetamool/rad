from django.utils.text import get_text_list
from django.utils.translation import gettext
from django.contrib.admin.models import LogEntry
from django.utils.timezone import localtime
from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import connection, reset_queries
from .models import *
import time
import functools
import random
import json


def Expertizi(request):
    """Функция для отображения записей Экспертизы"""
    if request.user.is_authenticated:
        if str(request.user.groups.all()[0]) == 'Обычный пользователь':
            return HttpResponseRedirect('/raz/')
        Documenti_vse = DtipDocument.objects.select_related(
            "document__expertiza__organizaciya")
        Document_ZaklDogovor = Documenti_vse.filter(
            tip__tip="Договор заключенный")
        # --------здесь составляю список айди из организаций, которые имеют письмо из РТН по проведении экспертизы
        List_org = []
        for i in Document_ZaklDogovor:
            id1 = i.document.expertiza.organizaciya.id
            zakl_dogovor = Documenti_vse.filter(document__expertiza__organizaciya__id=int(
                id1)).filter(tip__tip="Договор заключенный")
            ExpertZakluchenie = Documenti_vse.filter(document__expertiza__organizaciya__id=int(
                id1)).filter(tip__tip="Экспертное заключение")
            if zakl_dogovor.exists() == True and ExpertZakluchenie.exists() == True:
                name = Corganizaciya.objects.get(pk=int(id1)).nazvanie_korotkoe
                midlname = name.replace("«", "")
                newname = midlname.replace("»", "")
                if len(List_org) == 0:
                    List_org.append(newname)
                else:
                    if newname not in List_org:
                        List_org.append(newname)
                    else:
                        continue
        context = {
            'name': List_org,
        }
        return render(request, 'expertizi.html', context)
    else:
        return HttpResponseRedirect(reverse('login'))


def Razreshenie(request):
    """ Функция для отображения страницы Разрешения и отображения названий организаций """
    if request.user.is_authenticated:
        if str(request.user.groups.all()[0]) == 'Редакторы ПЭО':
            return HttpResponseRedirect('/ex/')

        Document_RAzresheniya = DtipDocument.objects.select_related("document__expertiza__organizaciya", 'document__expertiza__organizaciya__tip').filter(
            tip__tip="Разрешение").order_by('document__expertiza__organizaciya__nazvanie_korotkoe')
        List_org = []
        list_org = []
        # ----------сначала фильтруем все атомные станции по алфавиту-------------
        for obj in Document_RAzresheniya:
            slovar = {}
            if obj.document.expertiza.organizaciya.tip.tip == 'АО «Концерн Росэнергоатом»':
                name = str(obj.document.expertiza.organizaciya.nazvanie_select)
            else:
                continue
            if len(List_org) == 0:
                slovar['name'] = name
                List_org.append(slovar)
                list_org.append(name)
            else:
                if name not in list_org:
                    slovar['name'] = name
                    List_org.append(slovar)
                    list_org.append(name)
                else:
                    continue
        # ----------затем фильтруем все остальные предприятия по алфавиту-------------
        for obj in Document_RAzresheniya:
            slovar = {}
            if obj.document.expertiza.organizaciya.tip.tip == 'АО «Концерн Росэнергоатом»':
                continue
            else:
                name = str(obj.document.expertiza.organizaciya.nazvanie_select)
            if len(List_org) == 0:
                slovar['name'] = name
                List_org.append(slovar)
                list_org.append(name)
            else:
                if name not in list_org:
                    slovar['name'] = name
                    List_org.append(slovar)
                    list_org.append(name)
                else:
                    continue
        data = {
            'data': List_org,
        }
        return render(request, 'rasresgenie.html', data)
    else:
        return HttpResponseRedirect(reverse('login'))


def Archive(request):
    """Функция для отображения записей Архив экспертиз и их названий для фильтрации"""
    if request.user.is_authenticated:
        # if str(request.user.groups.all()[0]) == 'Редакторы ПЭО':
        #     return HttpResponseRedirect('/ex/')
        Main_document = DtipDocument.objects.select_related(
            'document__expertiza__organizaciya', 'document__expertiza__tip', 'tip')
        Main_document = Main_document.filter(tip__tip="Экспертное заключение")

        Expertiza = Cexpertiza.objects.select_related(
            'organizaciya', 'tip').all().order_by('organizaciya__nazvanie_korotkoe')
        Expertiza = Expertiza.filter(
            pk__in=Main_document.values_list('document__expertiza', flat=True))
        list_name_orga = []
        # ----------сначала фильтруем все атомные станции по алфавиту-------------
        for expertiza in Expertiza:
            if expertiza.is_deleted:
                slovar = {}
                if expertiza.organizaciya.tip.tip == 'АО «Концерн Росэнергоатом»':
                    name = str(expertiza.organizaciya.nazvanie_select)
                else:
                    continue
                slovar['name'] = name
                if slovar not in list_name_orga:
                    list_name_orga.append(slovar)
                else:
                    continue
        # ----------затем фильтруем все остальные предприятия по алфавиту-------------
        for expertiza in Expertiza:
            if expertiza.is_deleted:
                slovar = {}
                if expertiza.organizaciya.tip.tip == 'АО «Концерн Росэнергоатом»':
                    continue
                else:
                    name = str(expertiza.organizaciya.nazvanie_select)
                slovar['name'] = name
                if slovar not in list_name_orga:
                    list_name_orga.append(slovar)
                else:
                    continue

        data = {
            'name': list_name_orga,
        }
        return render(request, 'archive.html', data)
    else:
        return HttpResponseRedirect(reverse('login'))
# ---------------------Функция проверки скорости запроса QuerySet---------------------------


def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()
        start_queries = len(connection.queries)
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        end_queries = len(connection.queries)
        # print(f"Function : {func.__name__}")
        # print(f"Number of Queries : {end_queries - start_queries}")
        # print(f"Finished in : {(end - start):.2f}s")
        return result
    return inner_func


@query_debugger
def get_table_razreshenie_data(request):
    """Функция для заполнения таблицы по Разрешениям в зависимости от фильтрации"""
    data = {}
    est_li_vibrosi = str(request.GET.get('tip_razresheniya_1', ''))
    est_li_sbrosi = str(request.GET.get('tip_razresheniya_2', ''))

    srok1 = str(request.GET.get('srok1', False))
    srok2 = str(request.GET.get('srok2', False))
    srok3 = str(request.GET.get('srok3', False))
    if srok1 == "active" and srok2 == '' and srok3 == '':
        srok = 'srok1'
    elif srok1 == "" and srok2 == 'active' and srok3 == '':
        srok = 'srok2'
    elif srok1 == "" and srok2 == '' and srok3 == 'active':
        srok = 'srok3'
    elif srok1 == "" and srok2 == '' and srok3 == '':
        srok = ''
    list_organizations = request.GET.getlist('name_organ[]')
    # ----------------------------------------------------------
    TipDocument_Select = DtipDocument.objects.select_related(
        'document__expertiza__organizaciya__tip', 'document__expertiza__tip', 'tip').filter(tip__tip="Разрешение")
    DATA = JdataDocument.objects.select_related('document', 'opisanie_data')
    DATA2 = DATA.filter(
        opisanie_data__opisanie="Дата окончания действия разрешения")
    DATA3 = DATA.filter(
        opisanie_data__opisanie="Дата начала действия разрешения")
    DATA4 = DATA.filter(opisanie_data__opisanie="Дата выдачи разрешения")

    Razresheniya = TipDocument_Select.order_by(
        'document__expertiza__organizaciya__nazvanie_korotkoe')
    if est_li_vibrosi == 'active':
        Razresheniya_gos_usl = Razresheniya.filter(
            document__expertiza__tip__tip="Выброс")
    elif est_li_sbrosi == 'active':
        Razresheniya_gos_usl = Razresheniya.filter(
            document__expertiza__tip__tip="Сброс")
    elif est_li_vibrosi == '' and est_li_sbrosi == '':
        Razresheniya_gos_usl = Razresheniya
    spisok_dannih = []
    spisok_dannih1 = []
    i = 0
    N_M = int(datetime.now().month)
    N_Y = int(datetime.now().year)
    # -------------------------------------------
    # вначале составляю список из организаций которые имеют разрешения ( без повторений)
    list_organiz = []
    if len(list_organizations) == 0:
        for obj1 in Razresheniya_gos_usl:
            name_korotkoe = obj1.document.expertiza.organizaciya.nazvanie_select
            if len(list_organiz) == 0:
                list_organiz.append(name_korotkoe)
            else:
                if name_korotkoe not in list_organiz:
                    list_organiz.append(name_korotkoe)
                else:
                    continue
    else:
        list_organiz = list_organizations
    
    def Vivod_po_srokam(srok, R_M, R_Y):
        """" Функция по проверке сроков действия разрешения """
        V_Y = R_Y - N_Y
        if srok == '': vivod = 'ok'
        elif srok == 'srok1':
            if V_Y > 1: vivod = 'ok'
            elif V_Y == 1:
                if (12 - N_M) + R_M >= 12: vivod = 'ok'
                else: vivod = ''
            else:
                vivod = ''
        elif srok == 'srok2':
            if V_Y == 1:
                if (12 - N_M) + R_M >= 12: vivod = ''
                else: vivod = 'ok'
            elif V_Y == 0:
                if R_M - N_M > 0: vivod = 'ok'
                else: vivod = ''
            else:
                vivod = ''
        elif srok == 'srok3':
            if V_Y < 0: vivod = 'ok'
            elif V_Y == 0:
                if R_M - N_M < 0: vivod = 'ok'
                else: vivod = ''
            else:
                vivod = ''
        return vivod


    # далее прохожусь по названиям и узнаю какие организации имеют по несколько разрешений
    t = 1
    for name1 in list_organiz:
        Razresheniya1 = Razresheniya_gos_usl.filter(
            document__expertiza__organizaciya__nazvanie_select=name1)

        if est_li_vibrosi == '' and est_li_sbrosi == '':
        
            for tipp in ['Сброс', 'Выброс']:
                Razresheniya2 = Razresheniya1.filter(
                    document__expertiza__tip__tip=tipp)
                if Razresheniya2.exists():
                    if (Razresheniya2.count() > 1):
                        list_id_doc = []
                        list_dat_doc = []
                        for obj2 in Razresheniya2:
                            list_id_doc.append(obj2.document.id)
                        for id_doc in list_id_doc:
                            data = DATA4.get(
                                document__id=id_doc).data.strftime("%Y-%m-%d")
                            list_dat_doc.append(data)
                        # сортирую даты выдачи
                        sort_list_dat = sorted(list_dat_doc)
                        actual_data = sort_list_dat[len(sort_list_dat)-1]
                        # актуальное айди документа (Разрешения то есть)
                        actual_id_doc = list_id_doc[list_dat_doc.index(
                            actual_data)]
                        Razresheniya2 = Razresheniya2.filter(
                            document__id=actual_id_doc)
                    for obj in Razresheniya2:
                        row = []
                        i = i+1
                        name_korotkoe = obj.document.expertiza.organizaciya.nazvanie_korotkoe
                        id_doc_razresh = obj.document.id
                        tip_razresehniya = obj.document.expertiza.tip.tip
                        if str(tip_razresehniya) == 'Выброс': 
                            title_gos_usluga = 'Разрешение на выброс радиоактивных веществ в атмосферный воздух'
                        elif str(tip_razresehniya) == 'Сброс': 
                            title_gos_usluga = 'Разрешение на сброс радиоактивных веществ в водный объект'
                        # Dannie_razresheniya = JDDrazr.objects.get(document__document__id = id_doc_razresh)
                        try:
                            nomer_razresheniya = JDDrazr.objects.get(
                                document__document__id=id_doc_razresh).nomer
                        except:
                            nomer_razresheniya = 'не выставлен'

                        fayl_url_raz = obj.document.fayl.url
                        try:
                            kolichestvo_istochnikov = int(
                                obj.document.expertiza.kolichestvo_istochnikov)
                        except:
                            kolichestvo_istochnikov = '0'

                        try:
                            neorgistochnikov = int(
                                obj.document.expertiza.neorganizovan_istochniki)
                        except:
                            neorgistochnikov = '0'
                        id_expertizi = obj.document.expertiza.id
                        id_razresehniya = obj.document.id

                        if int(neorgistochnikov) == 0:
                            title_neorgistochn = 'Отсутствуют'
                            kolichestvo_neorgistochnikov = 0
                        else:
                            title_neorgistochn = 'Присутствуют'
                            kolichestvo_neorgistochnikov = neorgistochnikov

                        for dat in DATA3:
                            id_documenta = dat.document.id
                            if id_razresehniya == id_documenta:
                                data_nachala = dat.data.strftime("%Y-%m-%d")

                        for dat in DATA2:
                            id_documenta = dat.document.id
                            if id_razresehniya == id_documenta:
                                data_okonchaniya = dat.data.strftime(
                                    "%d.%m.%Y")
                        R_M = int(data_okonchaniya[3:5])
                        R_Y = int(data_okonchaniya[6:10])

                        vivod = Vivod_po_srokam(srok, R_M, R_Y)
                        
                        if vivod == 'ok':
                            row.append(
                                '<div name="1" style="text-align:center;">' + '</div>')
                            row.append(
                                '<div  style="text-align:center;">' + 'sdf' + '</div>')
                            row.append('<div style="text-align:left;"><a data-target="#myModal" data-toggle="modal" href="#id_modal_raz_info" onclick= "ModalWindow(' + str(
                                id_expertizi) + ')"' + '>' + str(name_korotkoe) + '</a></div>')
                            row.append('<div data-toggle="tooltip" title="'+ str(title_gos_usluga) +'" style="text-align:center;">' +
                                       str(tip_razresehniya) + ' РВ' + '</div>')
                            row.append(data_nachala)
                            row.append(data_okonchaniya)
                            row.append('<div data-toggle="tooltip" title="Общее число источников '+ str(kolichestvo_istochnikov) +'" style="text-align:center;">' +
                                       str(kolichestvo_istochnikov) + '</div>')
                            row.append('<div data-toggle="tooltip" title="'+title_neorgistochn +
                                       '" style="text-align:center;">' + str(kolichestvo_neorgistochnikov) + '</div>')
                            row.append('<div style="text-align:left;" ><a target="_blank" href="' +
                                       fayl_url_raz + '">' + str(nomer_razresheniya) + '</a></div>')
                        else:
                            continue
                        spisok_dannih1.append(row)
                    t += 1
        else:
            if (Razresheniya1.count() > 1):
                list_id_doc = []
                list_dat_doc = []
                for obj2 in Razresheniya1:
                    list_id_doc.append(obj2.document.id)
                for id_doc in list_id_doc:
                    data = DATA4.get(
                        document__id=id_doc).data.strftime("%Y-%m-%d")
                    list_dat_doc.append(data)
                sort_list_dat = sorted(list_dat_doc)  # сортирую даты выдачи
                actual_data = sort_list_dat[len(sort_list_dat)-1]
                # актуальное айди документа (Разрешения то есть)
                actual_id_doc = list_id_doc[list_dat_doc.index(actual_data)]
                Razresheniya1 = Razresheniya1.filter(
                    document__id=actual_id_doc)
            for obj in Razresheniya1:
                row = []
                i = i+1
                name_korotkoe = obj.document.expertiza.organizaciya.nazvanie_korotkoe
                id_doc_razresh = obj.document.id
                tip_razresehniya = obj.document.expertiza.tip.tip
                # Dannie_razresheniya = JDDrazr.objects.get(document__document__id = id_doc_razresh)
                try:
                    nomer_razresheniya = JDDrazr.objects.get(
                        document__document__id=id_doc_razresh).nomer
                except:
                    nomer_razresheniya = 'не выставлен'

                # if  str(obj.document.nomer_razresheniya) == '':
                #     nomer_razresheniya = 'не выставлен'
                # else:
                #     nomer_razresheniya = obj.document.nomer_razresheniya

                fayl_url_raz = obj.document.fayl.url
                if obj.document.expertiza.kolichestvo_istochnikov == None:
                    kolichestvo_istochnikov = 0
                else:
                    kolichestvo_istochnikov = int(
                        obj.document.expertiza.kolichestvo_istochnikov)
                id_expertizi = obj.document.expertiza.id
                id_razresehniya = obj.document.id

                if str(obj.document.expertiza.neorganizovan_istochniki) == '' or obj.document.expertiza.neorganizovan_istochniki == None or int(obj.document.expertiza.neorganizovan_istochniki) == 0:
                    title_neorgistochn = 'Отсутствуют'
                    kolichestvo_neorgistochnikov = 0
                else:
                    title_neorgistochn = 'Присутствуют'
                    kolichestvo_neorgistochnikov = str(
                        obj.document.expertiza.neorganizovan_istochniki)

                for dat in DATA3:
                    id_documenta = dat.document.id
                    if id_razresehniya == id_documenta:
                        data_nachala = dat.data.strftime("%Y-%m-%d")

                for dat in DATA2:
                    id_documenta = dat.document.id
                    if id_razresehniya == id_documenta:
                        data_okonchaniya = dat.data.strftime("%d.%m.%Y")
                R_M = int(data_okonchaniya[3:5])
                R_Y = int(data_okonchaniya[6:10])

                vivod = Vivod_po_srokam(srok, R_M, R_Y)
                if vivod == 'ok':
                    row.append(
                        '<div name="1" style="text-align:center;">'+'</div>')
                    row.append('<div style="text-align:center;">' +
                               'sfd' + '</div>')
                    row.append('<div style="text-align:left;"><a data-target="#myModal" data-toggle="modal" href="#id_modal_raz_info" onclick= "ModalWindow(' +
                               str(id_expertizi) + ')"' + '>' + str(name_korotkoe) + '</a></div>')
                    row.append('<div style="text-align:center;">' +
                               str(tip_razresehniya) + ' РВ' + '</div>')
                    row.append(data_nachala)
                    row.append(data_okonchaniya)
                    row.append('<div style="text-align:center;">' +
                               str(kolichestvo_istochnikov) + '</div>')
                    row.append('<div data-toggle="tooltip" title="'+title_neorgistochn +
                               '" style="text-align:center;">' + str(kolichestvo_neorgistochnikov) + '</div>')
                    row.append('<div style="text-align:left;" ><a target="_blank" href="' +
                               fayl_url_raz + '">' + str(nomer_razresheniya) + '</a></div>')
                else:
                    continue
                spisok_dannih.append(row)
    # -------------------------------------------
    last_spisok = []
    if est_li_vibrosi == '' and est_li_sbrosi == '':
        last_spisok = spisok_dannih1
    else:
        last_spisok = spisok_dannih
    m = 0
    for k in last_spisok:
        m = m+1
        last_spisok[m-1][0] = '<div>' + str(m) + '</div>'

    data = {
        "recordsFiltered": 3,
        "recordsTotal": 3,
        "data": last_spisok,
    }
    return JsonResponse(data)


@query_debugger
def get_modal_table_razresheniya(request):
    """Функция для заполнения Модального окна по Разрешениям в зависимости от нажатой организации"""
    if request.GET:
        DATA = {}
        polniu_spisok_razresheniy = []
        id_raz_doc = 0
        # Получаю айди экспертизы - это и есть айди разрешения
        id_rasresheniya = int(request.GET.get('id_raz'))
        MAIN_DOC = DtipDocument.objects.select_related(
            'document__expertiza__organizaciya__tip').order_by('-document__expertiza__data')
        DATA_DOCUMENTA = JdataDocument.objects.select_related('document')

        doc_razresh = MAIN_DOC.filter(document__expertiza__id=id_rasresheniya)
        for k in doc_razresh:
            polnoe_nazvanie = k.document.expertiza.organizaciya.nazvanie_polnoe
            tip_razreshe = k.document.expertiza.tip.tip
            nomer_DNP = k.document.expertiza.nomer_expertizi
            break
        Razreshenie_organizacii = MAIN_DOC.filter(document__expertiza__organizaciya__nazvanie_polnoe=polnoe_nazvanie).filter(
            document__expertiza__tip__tip=tip_razreshe).filter(tip__tip="Разрешение")
        spisok_id_expertiz = []
        for obj in Razreshenie_organizacii:
            pobochniy_spisok_razresheniy = []
            spisok_id_expertiz.append(obj.document.expertiza.id)
            try:
                nomer_razresheniya = JDDrazr.objects.get(
                    document__document__id=obj.document.id).nomer
            except:
                nomer_razresheniya = 'не выставлен'

            pobochniy_spisok_razresheniy.append(nomer_razresheniya)
            pobochniy_spisok_razresheniy.append('')
            pobochniy_spisok_razresheniy.append(obj.document.expertiza.id)
            pobochniy_spisok_razresheniy.append('')

            polniu_spisok_razresheniy.append(pobochniy_spisok_razresheniy)

        spisok_id_expertiz_sort = list(set(spisok_id_expertiz))
        kolvo_expertiz = len(spisok_id_expertiz_sort)
        # --------------------Быстрая сортировка Хоара-----------------------------

        def quicksort(nums):
            if len(nums) <= 1:
                return nums
            else:
                q = random.choice(nums)
            l_nums = [n for n in nums if n < q]
            e_nums = [q] * nums.count(q)
            b_nums = [n for n in nums if n > q]
            return quicksort(l_nums) + e_nums + quicksort(b_nums)

        # -------------------------------------------------
        str_actual_razr = 'актуальное'

        if kolvo_expertiz > 1:
            list_dat_vidachi = []
            for obj in polniu_spisok_razresheniy:
                id_ex = obj[2]
                id_doc = MAIN_DOC.filter(tip__tip="Разрешение").get(
                    document__expertiza__id=str(id_ex)).document.id
                obj[3] = id_doc
                data_vidachi_all = DATA_DOCUMENTA.filter(opisanie_data__opisanie="Дата выдачи разрешения").get(
                    document__id=id_doc).data.strftime("%d.%m.%Y")
                list_dat_vidachi.append(
                    datetime.strptime(data_vidachi_all, "%d.%m.%Y"))
                obj[1] = data_vidachi_all
            # актуаьная дата выдачи
            actual_data = quicksort(list_dat_vidachi)[-1].strftime("%d.%m.%Y")
            # ниже ищу айди экспертизы к этой дате
            for k in polniu_spisok_razresheniy:
                if k[1] == actual_data:
                    id_actual_exp = k[2]
                    break

            if id_actual_exp != id_rasresheniya:
                str_actual_razr = 'неактуальное'

        # ------------------------------------
        if kolvo_expertiz > 1:
            sort_list_dat = quicksort(list_dat_vidachi)
            sort_poln_spisok_raz = []
            for data in sort_list_dat:
                sort_pobochn_spisok = []
                for obj in polniu_spisok_razresheniy:

                    if datetime.strptime(obj[1], "%d.%m.%Y") == data:
                        index_pob_spisk = polniu_spisok_razresheniy.index(obj)
                        break
                sort_pobochn_spisok.append(
                    polniu_spisok_razresheniy[index_pob_spisk][0])
                sort_pobochn_spisok.append(
                    polniu_spisok_razresheniy[index_pob_spisk][1])
                sort_pobochn_spisok.append(
                    polniu_spisok_razresheniy[index_pob_spisk][2])
                sort_pobochn_spisok.append(
                    polniu_spisok_razresheniy[index_pob_spisk][3])
                sort_poln_spisok_raz.append(sort_pobochn_spisok)
        else:
            sort_poln_spisok_raz = []
        # ------------------------------------
        # В списке ниже выводятся элементы, являющимися своими списками и которые содержат "номер разрешения", "дату выдачи", "айди экспертизы", "айди документа разрешения"
        Doc_razresheniya = MAIN_DOC.filter(tip__tip="Разрешение").filter(
            document__expertiza__id=str(id_rasresheniya))
        Doc_proekt_normat = MAIN_DOC.filter(tip__tip="Проект нормативов").filter(
            document__expertiza__id=str(id_rasresheniya))
        Doc_expert_zaklych = MAIN_DOC.filter(tip__tip="Экспертное заключение").filter(
            document__expertiza__id=str(id_rasresheniya))
        for obj in Doc_razresheniya:
            id_raz_doc = obj.document.id
            vibros_or_sbros = obj.document.expertiza.tip.tip
            if vibros_or_sbros == 'Выброс':
                tip_razresheniya = 'Разрешение на выброс радиоактивных веществ в атмосферный воздух'
            if vibros_or_sbros == 'Сброс':
                tip_razresheniya = 'Разрешение на сброс радиоактивных веществ в водный объект'

            try:
                prochaya_inform = JDDrazr.objects.get(
                    document__document__id=id_raz_doc).opisanie
            except:
                prochaya_inform = ''
            try:
                nomer_razr_actual = JDDrazr.objects.get(
                    document__document__id=id_raz_doc).nomer
            except:
                nomer_razr_actual = 'не выставлен'
            try:
                vidano = JDDrazr.objects.get(
                    document__document__id=id_raz_doc).kem_vidano.poln
            except:
                vidano = ''

            DATA = {
                'kolvo_expertiz': kolvo_expertiz,
                'id_raz_doc': obj.document.id,
                'name_polnoe': obj.document.expertiza.organizaciya.nazvanie_polnoe,
                'tip_razresheniya': tip_razresheniya,
                'vse_istochniki': obj.document.expertiza.kolichestvo_istochnikov,
                'neorganizovannie_istochniki': obj.document.expertiza.neorganizovan_istochniki,
                'prochaya_inf': prochaya_inform,
                'nomer_razresheniya': nomer_razr_actual,
                'kem_vidano': vidano,
                'fayl_url_raz': obj.document.fayl.url,
                'drugie_razreshen': sort_poln_spisok_raz,
                'actual': str_actual_razr,
                'DNP': nomer_DNP,
            }

            break
        try:
            for obj in Doc_proekt_normat:
                DATA['fayl_url_proekta_normat'] = obj.document.fayl.url
                DATA['fayl_name_proekta_normat'] = obj.document.fayl.name.replace(
                    "file/", "")
                break
        except:
            DATA['fayl_url_proekta_normat'] = ''

        try:
            for obj in Doc_expert_zaklych:
                DATA['fayl_url_expert_zakl'] = obj.document.fayl.url
                DATA['fayl_name_expert_zakl'] = obj.document.fayl.name.replace(
                    "file/", "")
                break
        except:
            DATA['fayl_url_expert_zakl'] = ''
        try:
            for data in DATA_DOCUMENTA.filter(opisanie_data__opisanie="Дата выдачи разрешения").filter(document__id=id_raz_doc):
                dati_vida4i = data.data.strftime("%d.%m.%Y")
        except:
            dati_vida4i = 'не выставлена'

        try:
            for data in DATA_DOCUMENTA.filter(opisanie_data__opisanie="Дата начала действия разрешения").filter(document__id=id_raz_doc):
                dati_nachala = data.data.strftime("%d.%m.%Y")
        except:
            dati_nachala = 'не выставлена'

        try:
            for data in DATA_DOCUMENTA.filter(opisanie_data__opisanie="Дата окончания действия разрешения").filter(document__id=id_raz_doc):
                dati_okon4aniya = data.data.strftime("%d.%m.%Y")
        except:
            dati_okon4aniya = 'не выставлена'

        DATA["data_vidachi"] = dati_vida4i
        DATA["data_nachala"] = dati_nachala
        DATA["data_okonchaniya"] = dati_okon4aniya
        return JsonResponse(DATA)
    else:
        return HttpResponse('0')


@query_debugger
def get_table_expertizi_data(request):
    """Функция для заполнения таблицы с экспертизами в работе в зависимости 
    от нажатой кнопки В работе (запрос организации или ответ НТЦ) 
    """
    if request.GET:

        spisok_dannih1 = []
        spisok_dannih2 = []
        data_seichas = datetime.now().date()
        DATA_DOCUMENT = JdataDocument.objects.select_related(
            'document', 'opisanie_data').all()
        Main_document = DtipDocument.objects.select_related('document__expertiza__organizaciya', 'document__expertiza__tip', 'tip').order_by(
            'document__expertiza__organizaciya__nazvanie_korotkoe')
        Expertiza = Cexpertiza.objects.select_related(
            'organizaciya', 'tip').order_by('organizaciya__nazvanie_polnoe').all()
        srok_main = 'all'
        if request.GET.get('srok1') == 'active':
            srok_main = 1
        elif request.GET.get('srok2') == 'active':
            srok_main = 2
        elif request.GET.get('srok3') == 'active':
            srok_main = 3
        # Main_document = Main_document.exclude(tip__tip = "Экспертное заключение" )
        # Expertiza = Expertiza.filter(pk__in = Main_document.values_list('document__expertiza',flat=True))
        if request.GET.get('sbros_ex') == '' and request.GET.get('vibros_ex') == '':
            Main_document1 = Main_document
            Expertiza1 = Expertiza
        elif request.GET.get('sbros_ex') == 'active':
            Main_document1 = Main_document.filter(
                document__expertiza__tip__tip='Сброс')
            Expertiza1 = Expertiza.filter(tip__tip='Сброс')
        elif request.GET.get('vibros_ex') == 'active':
            Main_document1 = Main_document.filter(
                document__expertiza__tip__tip='Выброс')
            Expertiza1 = Expertiza.filter(tip__tip='Выброс')
        list_id_expertiz = []

        for obj in Expertiza1:
            if obj.is_deleted == False:
                list_id_expertiz.append(obj.id)

        index = 0
        for id_exp in list_id_expertiz:
            znachenie = ''
            treb_deyst = ''
            treb_title = ''
            srok_doc = ''
            title_treb = ''
            index = index + 1
            row = []

            Pismo_v_RTN = Main_document1.filter(document__expertiza__id=id_exp).filter(
                tip__tip="Письмо в Ростехнадзор")
            Pismo_v_organ = Main_document1.filter(
                document__expertiza__id=id_exp).filter(tip__tip="Письмо в организацию по договору")
            Pismo_v_organ_garant = Main_document1.filter(
                document__expertiza__id=id_exp).filter(tip__tip="Письмо в организацию по гарантийному письму")
            Pismo_iz_rtn = Main_document1.filter(document__expertiza__id=id_exp).filter(
                tip__tip="Письмо из Ростехнадзора/Территориального органа о проведении экспертизы")
            Pismo_iz_organ = Main_document1.filter(document__expertiza__id=id_exp).filter(
                tip__tip="Письмо из организации о проведении экспертизы")
            Zapros_TKP = Main_document1.filter(
                document__expertiza__id=id_exp).filter(tip__tip="Запрос ТКП")
            Otvet_TKP = Main_document1.filter(document__expertiza__id=id_exp).filter(
                tip__tip="Ответ на запрос ТКП")
            Pismo_Dogovor_TZ = Main_document1.filter(document__expertiza__id=id_exp).filter(
                tip__tip="Письмо о проекте договора и ТЗ")
            Otvet_Pismo_Dogovor_TZ = Main_document1.filter(document__expertiza__id=id_exp).filter(
                tip__tip="Ответ на письмо о проекте договора и ТЗ")
            Snigenie_cen = Main_document1.filter(document__expertiza__id=id_exp).filter(
                tip__tip="Запрос о снижении цены")
            Otvet_snigenie_cen = Main_document1.filter(
                document__expertiza__id=id_exp).filter(tip__tip="Ответ о снижении цены")
            zakl_dogovor = Main_document1.filter(
                document__expertiza__id=id_exp).filter(tip__tip="Договор заключенный")
            Garant_pismo = Main_document1.filter(
                document__expertiza__id=id_exp).filter(tip__tip="Гарантийное письмо")
            Proekt_normat = Main_document1.filter(
                document__expertiza__id=id_exp).filter(tip__tip="Проект нормативов")
            Expertn_zaklyuchenie = Main_document1.filter(
                document__expertiza__id=id_exp).filter(tip__tip="Экспертное заключение")
            AKT = Main_document1.filter(
                document__expertiza__id=id_exp).filter(tip__tip="Акт")

            Expertiza_get = Expertiza1.get(id=id_exp)
            if Zapros_TKP.exists() and Otvet_TKP.exists() and Pismo_Dogovor_TZ.exists() and Otvet_Pismo_Dogovor_TZ.exists() == False \
                    and zakl_dogovor.exists() == False:
                pass
            Nazvanie_org = Expertiza_get.organizaciya.nazvanie_korotkoe
            if Expertiza_get.tip.tip == 'Выброс':
                gos_usluga, gos_title = 'Выброс РВ', 'Выдача разрешения на выброс радиоактивных веществ в атмосферный воздух'
            if Expertiza_get.tip.tip == 'Сброс':
                gos_usluga, gos_title = 'Сброс РВ', 'Выдача разрешения на сброс радиоактивных веществ в водный объект'

            if (Zapros_TKP.exists() and Otvet_TKP.exists() and Pismo_Dogovor_TZ.exists() == False and Otvet_Pismo_Dogovor_TZ.exists() == False and zakl_dogovor.exists() == False and Garant_pismo.exists() == False  and AKT.exists() == False and (Otvet_snigenie_cen.exists() or Snigenie_cen.exists() == False)) or \
                    (Zapros_TKP.exists() and Otvet_TKP.exists() and Pismo_Dogovor_TZ.exists() and Otvet_Pismo_Dogovor_TZ.exists() and zakl_dogovor.exists() == False and Garant_pismo.exists() == False  and AKT.exists() == False and (Otvet_snigenie_cen.exists() or Snigenie_cen.exists() == False)) or \
                    (Zapros_TKP.exists() == False and Otvet_TKP.exists() == False and Pismo_Dogovor_TZ.exists() == False and Otvet_Pismo_Dogovor_TZ.exists() == False and zakl_dogovor.exists() == False and Garant_pismo.exists() == False  and Expertn_zaklyuchenie.exists() == False and Pismo_iz_rtn.exists() == False and AKT.exists() == False and (Otvet_snigenie_cen.exists() or Snigenie_cen.exists() == False)) or \
                    (Pismo_iz_rtn.exists() and Pismo_v_RTN.exists() and Pismo_v_organ.exists() and Zapros_TKP.exists() == False and Otvet_TKP.exists() == False and Pismo_Dogovor_TZ.exists() == False and Otvet_Pismo_Dogovor_TZ.exists() == False and zakl_dogovor.exists() == False and Garant_pismo.exists() == False  and AKT.exists() == False and Expertn_zaklyuchenie.exists() == False and (Otvet_snigenie_cen.exists() or Snigenie_cen.exists() == False)) or \
                    (Pismo_v_RTN.exists() == False and Pismo_v_organ.exists() == False and Pismo_iz_rtn.exists() == False and Pismo_iz_organ.exists() == False and Zapros_TKP.exists() == False and Otvet_TKP.exists() == False and Pismo_Dogovor_TZ.exists() == False and Otvet_Pismo_Dogovor_TZ.exists() == False and zakl_dogovor.exists() == False and Garant_pismo.exists() == False  and Proekt_normat.exists() == False and Expertn_zaklyuchenie.exists() == False and AKT.exists() == False and (Otvet_snigenie_cen.exists() or Snigenie_cen.exists() == False)) or \
                    (Pismo_v_RTN.exists() and Pismo_v_organ.exists() and zakl_dogovor.exists() == False and Garant_pismo.exists() and Proekt_normat.exists() and Expertn_zaklyuchenie.exists()  and AKT.exists() == False ) or (Pismo_v_RTN.exists() and Pismo_v_organ.exists() and Zapros_TKP.exists() and Otvet_TKP.exists() and zakl_dogovor.exists() and Proekt_normat.exists() and Expertn_zaklyuchenie.exists() and AKT.exists() == False) or (Pismo_v_RTN.exists() and Pismo_v_organ.exists() and Zapros_TKP.exists() and Otvet_TKP.exists() and zakl_dogovor.exists() and Proekt_normat.exists() and Expertn_zaklyuchenie.exists() and Garant_pismo.exists() and Pismo_v_organ_garant.exists() and AKT.exists() == False):
                if (Pismo_v_RTN.exists() and Pismo_v_organ.exists() and Zapros_TKP.exists() and Otvet_TKP.exists() and zakl_dogovor.exists() and Proekt_normat.exists() and Expertn_zaklyuchenie.exists() and AKT.exists() == False) or (Pismo_v_RTN.exists() and Pismo_v_organ.exists() and Zapros_TKP.exists() and Otvet_TKP.exists() and zakl_dogovor.exists() and Proekt_normat.exists() and Expertn_zaklyuchenie.exists() and Garant_pismo.exists() and Pismo_v_organ_garant.exists() and AKT.exists() == False):
                    znachenie = '4'
                    treb_deyst, treb_title = 'Ожидается подписанный Акт', 'От организации ожидается подписанный Акт сдачи-приемки'
                else:
                    treb_deyst, treb_title = 'Ожидается заключение договора', "От организации ожидается заключение договора"
                    znachenie = '4'

                row.append('<div>' + '1' + '</div>')
                row.append('<div name="'+str(znachenie)+'" style="text-align:left;"><a data-target="#myModal" data-toggle="modal" href="#id_modal_ex_info" onclick= "Inform_Ex_v_rabote(' +
                           str(id_exp)+',' + str(treb_deyst.split()) + ','+str(znachenie) + ',' + str(znachenie.split()) + ')"' + '>' + str(Nazvanie_org) + '</a></div>')
                row.append('<div data-placement="top" data-toggle="tooltip" title="' +
                           str(gos_title) + '">' + gos_usluga + '</div>')
                row.append('<div style="text-align:center;" data-placement="top" data-toggle="tooltip" title="' +
                           treb_title + '" >' + treb_deyst + '</div>')
                row.append(
                    '<div style="text-align:center;" data-placement="top" data-toggle="tooltip" title="Срок неопределен">' + 'Неопределено' + '</div>')
                if srok_main == 1 and znachenie == '1':
                    spisok_dannih1.append(row)
                elif srok_main == 2 and znachenie == '2':
                    spisok_dannih1.append(row)
                elif srok_main == 3 and znachenie == '3':
                    spisok_dannih1.append(row)
                elif srok_main == 'all':
                    spisok_dannih1.append(row)
                else:
                    continue
            elif Pismo_v_RTN.exists() and Pismo_v_organ.exists() and Zapros_TKP.exists() and Otvet_TKP.exists() and zakl_dogovor.exists() and Proekt_normat.exists() and Expertn_zaklyuchenie.exists() and AKT.exists() == False:
                znachenie = '4'
                treb_deyst, title_treb = 'Ответ на запрос о снижении цены', 'Подготовка ответа на запрос запрос о снижении цены'
            else:
                def Znachenie(data1, data2):
                    if (data1 == 'Неопределен') or (data2 == 'Неопределен'):
                        znachenie = '4'
                        return znachenie
                    if int((data1 - data_seichas).days) < 7:
                        znachenie = '3'
                    else:
                        if (data_seichas - data2) <= (data1-data2)/2:
                            znachenie = '1'
                        elif ((data_seichas - data2) > (data1-data2)/2):
                            znachenie = '2'
                    return znachenie
                if Pismo_iz_rtn.exists() and Zapros_TKP.exists() == False and Otvet_TKP.exists() == False and Pismo_Dogovor_TZ.exists() == False and Otvet_Pismo_Dogovor_TZ.exists() == False and zakl_dogovor.exists() == False and AKT.exists() == False and Expertn_zaklyuchenie.exists() == False and Pismo_v_RTN.exists() == False and Pismo_v_organ.exists() == False:
                    srok_doc = 'Неопределен'
                    treb_deyst, title_treb = 'Письмо в организацию и РТН/ТО', 'Подготовка письма в организацию и Ростехнадзор (или территориальный орган)'
                    znachenie = '4'
                elif Snigenie_cen.exists() and Otvet_snigenie_cen.exists() == False and zakl_dogovor.exists() == False and AKT.exists() == False and Expertn_zaklyuchenie.exists() == False:
                    for k in Snigenie_cen.filter(document__expertiza__id=id_exp):
                        id_document = k.document.id
                    try:
                        sroc_predost_doc = DATA_DOCUMENT.filter(
                            opisanie_data__opisanie="Срок подготовки ответа").get(document__id=id_document).data
                        srok_doc = sroc_predost_doc.strftime("%d.%m.%Y")
                    except:
                        sroc_predost_doc = 'Неопределен'
                        srok_doc = 'Неопределен'
                    try:
                        data_vidachi_doc = DATA_DOCUMENT.filter(
                            opisanie_data__opisanie="Дата поступления документа").get(document__id=id_document).data
                    except:
                        data_vidachi_doc = 'Неопределен'
                    znachenie = Znachenie(sroc_predost_doc, data_vidachi_doc)
                    treb_deyst, title_treb = 'Ответ на запрос о снижении цены', 'Подготовка ответа на запрос запрос о снижении цены'
                elif Zapros_TKP.exists() == True  \
                        and Otvet_TKP.exists() == False and Pismo_Dogovor_TZ.exists() == False  \
                        and Otvet_Pismo_Dogovor_TZ.exists() == False and zakl_dogovor.exists() == False and AKT.exists() == False and Expertn_zaklyuchenie.exists() == False:
                    for k in Zapros_TKP.filter(document__expertiza__id=id_exp):
                        id_document = k.document.id
                    try:
                        sroc_predost_doc = DATA_DOCUMENT.filter(
                            opisanie_data__opisanie="Срок подготовки ответа").get(document__id=id_document).data
                        srok_doc = sroc_predost_doc.strftime("%d.%m.%Y")
                    except:
                        sroc_predost_doc = 'Неопределен'
                        srok_doc = 'Неопределен'
                    try:
                        data_vidachi_doc = DATA_DOCUMENT.filter(
                            opisanie_data__opisanie="Дата поступления документа").get(document__id=id_document).data
                    except:
                        data_vidachi_doc = 'Неопределен'
                    znachenie = Znachenie(sroc_predost_doc, data_vidachi_doc)
                    treb_deyst, title_treb = 'Ответ на запрос ТКП', 'Подготовка ответа на запрос ТКП'
                elif Zapros_TKP.exists() and Otvet_TKP.exists() and Pismo_Dogovor_TZ.exists() and Otvet_Pismo_Dogovor_TZ.exists() == False \
                        and zakl_dogovor.exists() == False and AKT.exists() == False:
                    for k in Pismo_Dogovor_TZ.filter(document__expertiza__id=id_exp):
                        id_document = k.document.id
                    try:
                        sroc_predost_doc = DATA_DOCUMENT.filter(
                            opisanie_data__opisanie="Срок подготовки ответа").get(document__id=id_document).data
                        srok_doc = sroc_predost_doc.strftime("%d.%m.%Y")
                    except:
                        sroc_predost_doc = 'Неопределен'
                        srok_doc = 'Неопределен'
                    try:
                        data_vidachi_doc = DATA_DOCUMENT.filter(
                            opisanie_data__opisanie="Дата поступления документа").get(document__id=id_document).data
                    except:
                        data_vidachi_doc = 'Неопределен'
                    znachenie = Znachenie(sroc_predost_doc, data_vidachi_doc)
                    treb_deyst, title_treb = 'Ответ на письмо о проекте договора', 'Подготовка ответа на письмо о проекте договора'
                elif Zapros_TKP.exists() and Otvet_TKP.exists() and Pismo_Dogovor_TZ.exists() and Otvet_Pismo_Dogovor_TZ.exists() and zakl_dogovor.exists() \
                        and Proekt_normat.exists() and Expertn_zaklyuchenie.exists() == False and AKT.exists() == False:

                    for k in zakl_dogovor.filter(document__expertiza__id=id_exp):
                        id_document = k.document.id

                    try:
                        sroc_predost_doc = DATA_DOCUMENT.filter(
                            opisanie_data__opisanie="Срок подготовки экспертного заключения").get(document__id=id_document).data
                        srok_doc = sroc_predost_doc.strftime("%d.%m.%Y")
                    except:
                        sroc_predost_doc = 'Неопределен'
                        srok_doc = 'Неопределен'

                    try:
                        data_vidachi_doc = DATA_DOCUMENT.filter(
                            opisanie_data__opisanie="Дата заключения договора").get(document__id=id_document).data
                    except:
                        data_vidachi_doc = 'Неопределен'
                    znachenie = Znachenie(sroc_predost_doc, data_vidachi_doc)
                    if request.user.groups.filter(name='Редакторы ПЭО').exists():
                        treb_deyst, title_treb = 'Оформление Акта', 'Оформление Акта сдачи-приемки услуги'
                    else:
                        treb_deyst, title_treb = 'Подготовка экспертного заключения', 'Подготовка экспертного заключения'

                elif Zapros_TKP.exists() == True and zakl_dogovor.exists() == True  \
                        and Proekt_normat.exists() == True and Expertn_zaklyuchenie.exists() == False and AKT.exists() == False:
                    for k in zakl_dogovor.filter(document__expertiza__id=id_exp):
                        id_document = k.document.id

                    try:
                        sroc_predost_doc = DATA_DOCUMENT.filter(
                            opisanie_data__opisanie="Срок подготовки экспертного заключения").get(document__id=id_document).data
                        srok_doc = sroc_predost_doc.strftime("%d.%m.%Y")
                    except:
                        sroc_predost_doc = 'Неопределен'
                        srok_doc = 'Неопределен'
                    try:
                        data_vidachi_doc = DATA_DOCUMENT.filter(
                            opisanie_data__opisanie="Дата заключения договора").get(document__id=id_document).data
                    except:
                        data_vidachi_doc = 'Неопределен'
                    znachenie = Znachenie(sroc_predost_doc, data_vidachi_doc)
                    if request.user.groups.filter(name='Редакторы ПЭО').exists():
                        treb_deyst, title_treb = 'Оформление Акта', 'Оформление Акта сдачи-приемки услуги'
                    else:
                        treb_deyst, title_treb = 'Подготовка экспертного заключения', 'Подготовка экспертного заключения'
                elif Zapros_TKP.exists() == True  \
                        and Otvet_TKP.exists() == False and Pismo_Dogovor_TZ.exists() == True  \
                        and Otvet_Pismo_Dogovor_TZ.exists() == False and zakl_dogovor.exists() == False  \
                        and Proekt_normat.exists() == False and AKT.exists() == False:

                    for k in Pismo_Dogovor_TZ.filter(document__expertiza__id=id_exp):
                        id_document = k.document.id
                    try:
                        sroc_predost_doc = DATA_DOCUMENT.filter(
                            opisanie_data__opisanie="Срок подготовки ответа").get(document__id=id_document).data
                        srok_doc = sroc_predost_doc.strftime("%d.%m.%Y")
                    except:
                        sroc_predost_doc = 'Неопределен'
                        srok_doc = 'Неопределен'
                    try:
                        data_vidachi_doc = DATA_DOCUMENT.filter(
                            opisanie_data__opisanie="Дата поступления документа").get(document__id=id_document).data
                    except:
                        data_vidachi_doc = 'Неопределен'
                    znachenie = Znachenie(sroc_predost_doc, data_vidachi_doc)
                    treb_deyst, title_treb = 'Ответ на запрос ТКП', 'Подготовка ответа на запрос ТКП'
                elif Zapros_TKP.exists() == True  \
                        and Otvet_TKP.exists() == False and Pismo_Dogovor_TZ.exists() == True  \
                        and Otvet_Pismo_Dogovor_TZ.exists() == False and zakl_dogovor.exists() == False  \
                        and Proekt_normat.exists() == True and AKT.exists() == False:

                    for k in Zapros_TKP.filter(document__expertiza__id=id_exp):
                        id_document = k.document.id
                    try:
                        sroc_predost_doc = DATA_DOCUMENT.filter(
                            opisanie_data__opisanie="Срок подготовки ответа").get(document__id=id_document).data
                        srok_doc = sroc_predost_doc.strftime("%d.%m.%Y")
                    except:
                        sroc_predost_doc = 'Неопределен'
                        srok_doc = 'Неопределен'
                    try:
                        data_vidachi_doc = DATA_DOCUMENT.filter(
                            opisanie_data__opisanie="Дата поступления документа").get(document__id=id_document).data
                    except:
                        data_vidachi_doc = 'Неопределен'
                    znachenie = Znachenie(sroc_predost_doc, data_vidachi_doc)
                    treb_deyst, title_treb = 'Ответ на запрос ТКП', 'Подготовка ответа на запрос ТКП'
                elif Zapros_TKP.exists() == True  \
                        and Otvet_TKP.exists() == False and Pismo_Dogovor_TZ.exists() == False  \
                        and Otvet_Pismo_Dogovor_TZ.exists() == False and zakl_dogovor.exists() == False  \
                        and Proekt_normat.exists() == False and AKT.exists() == False:

                    for k in Zapros_TKP.filter(document__expertiza__id=id_exp):
                        id_document = k.document.id
                    try:
                        sroc_predost_doc = DATA_DOCUMENT.filter(
                            opisanie_data__opisanie="Срок подготовки ответа").get(document__id=id_document).data
                        srok_doc = sroc_predost_doc.strftime("%d.%m.%Y")
                    except:
                        sroc_predost_doc = 'Неопределен'
                        srok_doc = 'Неопределен'
                    try:
                        data_vidachi_doc = DATA_DOCUMENT.filter(
                            opisanie_data__opisanie="Дата поступления документа").get(document__id=id_document).data
                    except:
                        data_vidachi_doc = 'Неопределен'
                    znachenie = Znachenie(sroc_predost_doc, data_vidachi_doc)
                    treb_deyst, title_treb = 'Ответ на запрос ТКП', 'Подготовка ответа на запрос ТКП'
                elif Zapros_TKP.exists() == True  \
                        and Otvet_TKP.exists() == False and Pismo_Dogovor_TZ.exists() == True  \
                        and Otvet_Pismo_Dogovor_TZ.exists() == False and zakl_dogovor.exists() == False  \
                        and Proekt_normat.exists() == False and AKT.exists() == False:

                    for k in Pismo_Dogovor_TZ.filter(document__expertiza__id=id_exp):
                        id_document = k.document.id
                    try:
                        sroc_predost_doc = DATA_DOCUMENT.filter(
                            opisanie_data__opisanie="Срок подготовки ответа").get(document__id=id_document).data
                        srok_doc = sroc_predost_doc.strftime("%d.%m.%Y")
                    except:
                        sroc_predost_doc = 'Неопределен'
                        srok_doc = 'Неопределен'
                    try:
                        data_vidachi_doc = DATA_DOCUMENT.filter(
                            opisanie_data__opisanie="Дата поступления документа").get(document__id=id_document).data
                    except:
                        data_vidachi_doc = 'Неопределен'
                    znachenie = Znachenie(sroc_predost_doc, data_vidachi_doc)
                    treb_deyst, title_treb = 'Ответ на запрос ТКП', 'Подготовка ответа на запрос ТКП'
                elif Zapros_TKP.exists() == True  \
                        and Otvet_TKP.exists() == False and Pismo_Dogovor_TZ.exists() == True  \
                        and Otvet_Pismo_Dogovor_TZ.exists() == False and zakl_dogovor.exists() == False  \
                        and Proekt_normat.exists() == True and AKT.exists() == False:

                    for k in Pismo_Dogovor_TZ.filter(document__expertiza__id=id_exp):
                        id_document = k.document.id
                    try:
                        sroc_predost_doc = DATA_DOCUMENT.filter(
                            opisanie_data__opisanie="Срок подготовки ответа").get(document__id=id_document).data
                        srok_doc = sroc_predost_doc.strftime("%d.%m.%Y")
                    except:
                        sroc_predost_doc = 'Неопределен'
                        srok_doc = 'Неопределен'
                    try:
                        data_vidachi_doc = DATA_DOCUMENT.filter(
                            opisanie_data__opisanie="Дата поступления документа").get(document__id=id_document).data
                    except:
                        data_vidachi_doc = 'Неопределен'
                    znachenie = Znachenie(sroc_predost_doc, data_vidachi_doc)
                    treb_deyst, title_treb = 'Ответ на запрос ТКП', 'Подготовка ответа на запрос ТКП'
                elif Zapros_TKP.exists() and Otvet_TKP.exists() and zakl_dogovor.exists() and Proekt_normat.exists() and Expertn_zaklyuchenie.exists() and AKT.exists() == False:
                    srok_doc = ''

                    for k in zakl_dogovor.filter(document__expertiza__id=id_exp):
                        id_document = k.document.id

                    if Garant_pismo.exists():
                        if Pismo_v_organ.exists() == False:
                            treb_deyst, title_treb = 'Направление по договору', 'Направление комплекта документов по договору'
                    else:
                        treb_deyst, title_treb = 'Оформление Акта', 'Оформление Акта сдачи-приемки'
                   
                    try:
                        sroc_predost_doc = DATA_DOCUMENT.filter(
                            opisanie_data__opisanie="Срок подготовки экспертного заключения").get(document__id=id_document).data
                        srok_doc = sroc_predost_doc.strftime("%d.%m.%Y")
                    except:
                        sroc_predost_doc = 'Неопределен'
                        srok_doc = 'Неопределен'
                    try:
                        data_vidachi_doc = DATA_DOCUMENT.filter(
                            opisanie_data__opisanie="Дата заключения договора").get(document__id=id_document).data
                    except:
                        data_vidachi_doc = 'Неопределен'
                    znachenie = Znachenie(
                        sroc_predost_doc, data_vidachi_doc)
                elif Zapros_TKP.exists() and Otvet_TKP.exists() and zakl_dogovor.exists() and Proekt_normat.exists() and Expertn_zaklyuchenie.exists() and AKT.exists() and Pismo_v_RTN.exists() and Pismo_v_organ.exists() :
                    treb_deyst, title_treb = 'Экспертиза окончена', 'Экспертиза окончена. Все документы подгружены. Необходимо перевести ее в Архив'
                    srok_doc = 'Неопределен'
                    znachenie = '4'
                elif (Pismo_v_RTN.exists() == False and Pismo_v_organ.exists() == False and zakl_dogovor.exists() == False and Garant_pismo.exists() and Proekt_normat.exists() and Expertn_zaklyuchenie.exists() and AKT.exists() == False ):
                    srok_doc = 'Неопределен'
                    znachenie = '4'
                    if request.user.groups.filter(name='Редакторы ПЭО').exists():
                        treb_deyst, title_treb = 'Ожидается заключение договора',"От организации ожидается заключение договора"
                    else:
                        treb_deyst, title_treb = 'Подготовка писем в РТН/ТО и организацию','Подготовка писем в Ростехнадзор или территориальны орган и в организацию'
                elif Pismo_v_RTN.exists() == False and Pismo_v_organ.exists() == False and zakl_dogovor.exists() == False and Garant_pismo.exists() and Proekt_normat.exists() and Expertn_zaklyuchenie.exists() == False and AKT.exists() == False:
                    srok_doc = 'Неопределен'
                    znachenie = '4'
                    if request.user.groups.filter(name='Редакторы ПЭО').exists():
                        treb_deyst, title_treb = 'Ожидается заключение договора',"От организации ожидается заключение договора"
                    else:
                        treb_deyst, title_treb = 'Подготовка экспертного заключения','Подготовка экспертного заключения'
                elif Zapros_TKP.exists() and Otvet_TKP.exists() and zakl_dogovor.exists() and Proekt_normat.exists() == False and Pismo_iz_rtn.exists() == False:
                    treb_deyst, title_treb = 'Ожидание проекта нормативов', 'Ожидание письма из Ростехнадзора или территориального органа о проведении экспертизы и предоставлении проекта нормативов'
                    srok_doc = 'Неопределен'
                    znachenie = '4'
                elif Zapros_TKP.exists() and Otvet_TKP.exists() and zakl_dogovor.exists() and Proekt_normat.exists() and Expertn_zaklyuchenie.exists() and AKT.exists():
                    treb_deyst, title_treb = 'Основные документы загружены', 'Основные документы загружены, осталось загрузить письма в организацию и Ростехнадзор или территориальный орган. После этого необходимо перевести экспертизу в Архив'
                    srok_doc = 'Неопределен'
                    znachenie = '4'

                else:
                    if Pismo_v_RTN.exists() == False and Pismo_v_organ.exists() == False and Pismo_iz_rtn.exists() == False and Pismo_iz_organ.exists() == False and Zapros_TKP.exists() == False and Otvet_TKP.exists() == False and Pismo_Dogovor_TZ.exists() == False and Otvet_Pismo_Dogovor_TZ.exists() == False and zakl_dogovor.exists() == False and Proekt_normat.exists() == False and Expertn_zaklyuchenie.exists() == False and AKT.exists() == True:
                        znachenie = '5'
                        treb_deyst, title_treb = 'Загружен только Акт', 'Загружен только Акт'
                        srok_doc = '-'
                    elif Pismo_v_organ.exists() and Pismo_iz_organ.exists() and zakl_dogovor.exists() and Zapros_TKP.exists() == False and Otvet_TKP.exists() == False and Pismo_Dogovor_TZ.exists() == False and Otvet_Pismo_Dogovor_TZ.exists() == False:
                        znachenie = '5'
                        treb_deyst, title_treb = 'Загружен заключенный договор без запроса и ответа ТКП', 'Загружен заключенный договор без запроса и ответа ТКП'
                        srok_doc = '-'
                    elif Pismo_v_RTN.exists() == False and Pismo_v_organ.exists() == False and Pismo_iz_rtn.exists() == False and Zapros_TKP.exists() == False and Otvet_TKP.exists() == True and Pismo_Dogovor_TZ.exists() == False and Otvet_Pismo_Dogovor_TZ.exists() == False and zakl_dogovor.exists() == False and Proekt_normat.exists() == False and Expertn_zaklyuchenie.exists() == False and AKT.exists() == False:
                        znachenie = '5'
                        treb_deyst, title_treb = 'Загружен ответ на запрос ТКП, а самого запроса ТКП не было', 'Загружен ответ на запрос ТКП, а самого запроса ТКП не было'
                        srok_doc = '-'
                    else:
                        znachenie = '5'
                        treb_deyst, title_treb = 'Экспертиза заполнена неправильно', 'Экспертиза заполнена неправильно'
                        srok_doc = '-'

                row.append('<div>' + '1' + '</div>')
                row.append('<div name="'+str(znachenie)+'" style="text-align:left;"><a data-target="#myModal" data-toggle="modal" href="#id_modal_ex_info" onclick= "Inform_Ex_v_rabote(' +
                           str(id_exp) + ',' + str(treb_deyst.split()) + ','+str(znachenie) + ',' + str(srok_doc.split()) + ')"' + '>' + str(Nazvanie_org) + '</a></div>')
                row.append('<div data-placement="top" data-toggle="tooltip" title="' +
                           str(gos_title) + '">' + gos_usluga + '</div>')
                row.append('<div style="text-align:center;" data-placement="top" data-toggle="tooltip" title="' +
                           str(title_treb) + '" >' + treb_deyst + '</div>')
                row.append(srok_doc)
                if srok_main == 1 and znachenie == '1':
                    spisok_dannih2.append(row)
                elif srok_main == 2 and znachenie == '2':
                    spisok_dannih2.append(row)
                elif srok_main == 3 and znachenie == '3':
                    spisok_dannih2.append(row)
                elif srok_main == 'all':
                    spisok_dannih2.append(row)
                else:
                    continue

        if str(request.GET.get('v_rabote_zapros', False)) == 'active':
            data = {
                "recordsFiltered": 6,
                "recordsTotal": 6,
                "data": spisok_dannih1,
            }
        elif str(request.GET.get('v_rabote_otvet', False)) == 'active':
            data = {
                "recordsFiltered": 6,
                "recordsTotal": 6,
                "data": spisok_dannih2,
            }
        elif str(request.GET.get('vse_ex', False)) == 'active':
            spisod_dannih3 = spisok_dannih1+spisok_dannih2

            m = 0
            for k in spisod_dannih3:
                m = m+1
                spisod_dannih3[m-1][0] = '<div>' + str(m) + '</div>'
            data = {
                "recordsFiltered": 6,
                "recordsTotal": 6,
                "data": spisod_dannih3,
            }

    return JsonResponse(data)


@query_debugger
def get_table_archive_data(request):
    """ Функция по заполнению DataTable в Архиве """
    if request.GET:
        spisok_dannih3 = []
        DATA_DOCUMENT = JdataDocument.objects.select_related(
            'document', 'opisanie_data').all()
        Main_document = DtipDocument.objects.select_related('document__expertiza__organizaciya', 'document__expertiza__tip').order_by(
            'document__expertiza__organizaciya__nazvanie_korotkoe')
        Expertiza = Cexpertiza.objects.select_related(
            'organizaciya', 'tip').all()

        if request.GET.getlist('name_organ[]', False):
            Expertiza = Expertiza.filter(
                organizaciya__nazvanie_select__in=request.GET.getlist('name_organ[]'))
            Main_document = Main_document.filter(
                document__expertiza__organizaciya__nazvanie_select__in=request.GET.getlist('name_organ[]'))
        else:
            Expertiza = Expertiza
            Main_document = Main_document

        data_start_get = ''
        data_end_get = ''

        if request.GET.get('input_data_start_day') != '':
            data_start_get = datetime.strptime(request.GET.get(
                'input_data_start_day'), "%d.%m.%Y").date()


        elif request.GET.get('input_data_start_year') != '':
            data_start_get = datetime.strptime(
                request.GET.get('input_data_start_year'), "%Y").date()
        else:
            data_start_get = ''

        if request.GET.get('input_data_end_day') != '':
            data_end_get = datetime.strptime(request.GET.get(
                'input_data_end_day'), "%d.%m.%Y").date()
        elif request.GET.get('input_data_end_year') != '':
            data_end_get = datetime.strptime(
                request.GET.get('input_data_end_year'), "%Y").date()
            data_end_get = datetime.strptime(
                str(data_end_get.year + 1), "%Y").date()
        else:
            data_end_get = ''

        if str(request.GET.get('sbros_name')) == 'active':
            Expertiza = Expertiza.filter(tip__tip='Сброс')
        elif str(request.GET.get('vibros_name')) == 'active':
            Expertiza = Expertiza.filter(tip__tip='Выброс')
        else:
            Expertiza = Expertiza
        Main_document = Main_document.filter(tip__tip='Экспертное заключение')

        Expertiza = Expertiza.filter(
            pk__in=Main_document.values_list('document__expertiza', flat=True))

        index = 0
        for expertiza in Expertiza:
            if expertiza.is_deleted:
                if expertiza.kolichestvo_istochnikov == None or str(expertiza.kolichestvo_istochnikov)[0] == '0':
                    vse_istochiki = 0
                else:
                    vse_istochiki = expertiza.kolichestvo_istochnikov
                title_vse_istochniki = 'Полное число источников ' + str(vse_istochiki)
                if expertiza.neorganizovan_istochniki == None or str(expertiza.neorganizovan_istochniki)[0] == '0':
                    neorg_istochniki = 0
                    title_neorg_istochniki = 'Неорганизованные источники отсутствуют'
                else:
                    neorg_istochniki = expertiza.neorganizovan_istochniki
                    title_neorg_istochniki = 'Неорганизованные источники присутствуют в количестве ' + str(neorg_istochniki)
                row = []
                srok_doc = ''
                Nazvanie_org = expertiza.organizaciya.nazvanie_korotkoe
                index = index + 1
                try:
                    fayl_url_zakl = Main_document.get(
                        document__expertiza__id=expertiza.id).document.fayl.url
                except:
                    fayl_url_zakl = '//'
                try:
                    nomer_DNP = expertiza.nomer_expertizi
                    if 'дсп' in nomer_DNP:
                        nomer_DNP = nomer_DNP.replace('дсп', '')
                        if nomer_DNP[len(nomer_DNP)-1] == '-':
                            nomer_DNP = nomer_DNP[:len(nomer_DNP)-1]
                except:
                    nomer_DNP = 'Поле не заполнено'

                gos_usluga = expertiza.tip.tip
                if str(gos_usluga) == 'Выброс': 
                    title_gos_usluga = 'Выдача разрешения на выброс радиоактивных веществ в атмосферный воздух'
                elif str(gos_usluga) == 'Сброс': 
                    title_gos_usluga = 'Выдача разрешения на сброс радиоактивных веществ в водный объект'

                id_document = Main_document.get(
                    document__expertiza__id=expertiza.id).document.id
                srok_peredusloviem = DATA_DOCUMENT.filter(
                    opisanie_data__opisanie="Дата утверждения экспертного заключения")
                    
                if data_start_get != '':
                    try:
                        srok_doc = srok_peredusloviem.filter(
                            data__gte=data_start_get).get(document__id=id_document)
                    except:
                        continue
                if data_end_get != '':
                    try:
                        srok_doc = srok_peredusloviem.filter(
                            data__lte=data_end_get).get(document__id=id_document)
                    except:
                        continue
                try:
                    srok_doc = srok_peredusloviem.get(
                        document__id=id_document).data.strftime("%d.%m.%Y")
                except:
                    srok_doc = 'Отсутствует'

                row.append('<div style="text-align:center;">' +
                           str(index) + '</div>')
                row.append('<div style="text-align:left;"><a data-target="#myModal" data-toggle="modal" href="#id_modal_ex_info" onclick= "Inform_Ex_archive(' +
                           str(expertiza.id) + ')"' + '>' + str(Nazvanie_org) + '</a></div>')
                row.append('<div style="text-align:center;" ><a target="_blank" href="' +
                           fayl_url_zakl + '">'+'ДНП ' + nomer_DNP+'</a></div>')
                row.append('<div data-toggle="tooltip" title="' + str(title_gos_usluga) + '" style="text-align:center;" >' +
                           str(gos_usluga) + ' РВ' + '</div>')
                row.append('<div style="text-align:center;" data-toggle="tooltip" title="' + str(title_vse_istochniki) + '">' +
                           str(vse_istochiki) + '</div>')
                row.append('<div data-toggle="tooltip" title="' + str(title_neorg_istochniki) +'" style="text-align:center;">' +
                           str(neorg_istochniki) + '</div>')
                row.append(srok_doc)
                spisok_dannih3.append(row)

        data = {
            "data": spisok_dannih3,
        }
        return JsonResponse(data)


def get_inform_block_ex(request):
    """Функция по выводу информации по Экспертизе в работе в Модальном окне"""
    if request.GET:
        data = {}
        id_expertiza = int(request.GET.get('idd_ex'))

        Documenti_vse = DtipDocument.objects.select_related(
            'document__expertiza__organizaciya__tip', 'tip')

        Pismo_v_RTN = Documenti_vse.filter(document__expertiza__id=int(
            id_expertiza)).filter(tip__tip="Письмо в Ростехнадзор")
        Pismo_ot_organizacii = Documenti_vse.filter(document__expertiza__id=int(
            id_expertiza)).filter(tip__tip="Письмо из организации о проведении экспертизы")
        Pismo_v_organizaciu = Documenti_vse.filter(document__expertiza__id=int(
            id_expertiza)).filter(tip__tip="Письмо в организацию по договору")
        Pismo_v_organizaciuGarant = Documenti_vse.filter(document__expertiza__id=int(
            id_expertiza)).filter(tip__tip="Письмо в организацию по гарантийному письму")
        Pismo_RTN = Documenti_vse.filter(document__expertiza__id=int(id_expertiza)).filter(
            tip__tip="Письмо из Ростехнадзора/Территориального органа о проведении экспертизы")
        Zapros_TKP = Documenti_vse.filter(document__expertiza__id=int(
            id_expertiza)).filter(tip__tip="Запрос ТКП")
        Otvet_TKP = Documenti_vse.filter(document__expertiza__id=int(
            id_expertiza)).filter(tip__tip="Ответ на запрос ТКП")
        Pismo_Dogovor_TZ = Documenti_vse.filter(document__expertiza__id=int(
            id_expertiza)).filter(tip__tip="Письмо о проекте договора и ТЗ")
        Otvet_Pismo_Dogovor_TZ = Documenti_vse.filter(document__expertiza__id=int(
            id_expertiza)).filter(tip__tip="Ответ на письмо о проекте договора и ТЗ")
        Snigenie_cen = Documenti_vse.filter(
            document__expertiza__id=id_expertiza).filter(tip__tip="Запрос о снижении цены")
        Otvet_snigenie_cen = Documenti_vse.filter(
            document__expertiza__id=id_expertiza).filter(tip__tip="Ответ о снижении цены")
        Garant_pismo = Documenti_vse.filter(
            document__expertiza__id=id_expertiza).filter(tip__tip="Гарантийное письмо")
        Zakl_dogovor = Documenti_vse.filter(document__expertiza__id=int(
            id_expertiza)).filter(tip__tip="Договор заключенный")
        Proekt_normat = Documenti_vse.filter(document__expertiza__id=int(
            id_expertiza)).filter(tip__tip="Проект нормативов")
        ExpertZakluchenie = Documenti_vse.filter(document__expertiza__id=int(
            id_expertiza)).filter(tip__tip="Экспертное заключение")
        AKT = Documenti_vse.filter(document__expertiza__id=int(
            id_expertiza)).filter(tip__tip="Акт")
        Sluzhebki = Documenti_vse.filter(document__expertiza__id=int(
            id_expertiza)).filter(tip__tip="Служебная записка")

        # -----       срок предоставления любого документа ( в том числе утверждение экспертного заключение)--------
        Data_documenta = JdataDocument.objects.select_related('document')

        Expertiza = Cexpertiza.objects.select_related(
            'organizaciya__tip').get(id=id_expertiza)

        otraslevaya_prinad = Expertiza.organizaciya.tip.tip
        if request.user.groups.filter(name='Редакторы ПЭО').exists():
            redactor = 'есть'
        else:
            redactor = 'нет'

        nazvanie_polnoe = Expertiza.organizaciya.nazvanie_polnoe
        if Expertiza.tip.tip == 'Выброс':
            gos_usluga = 'Выдача разрешения на выброс радиоактивных веществ'
        elif Expertiza.tip.tip == 'Сброс':
            gos_usluga = 'Выдача разрешения на сброс радиоактивных веществ'
        vse_istochiki = Expertiza.kolichestvo_istochnikov

        if Expertiza.kolichestvo_istochnikov == None or str(Expertiza.kolichestvo_istochnikov)[0] == '0':
            vse_istochiki = 0
        else:
            vse_istochiki = Expertiza.kolichestvo_istochnikov
        if Expertiza.neorganizovan_istochniki == None or str(Expertiza.neorganizovan_istochniki)[0] == '0':
            neorg_istochniki = 0
        else:
            neorg_istochniki = Expertiza.neorganizovan_istochniki
        try:
            nomer_expertnogo_zaklucheniya = Expertiza.nomer_expertizi
        except:
            nomer_expertnogo_zaklucheniya = ''

        List_utvergdaet = []
        Personal_utvergdaet = JERPerson.objects.select_related('expertiza').filter(
            expertiza__id=id_expertiza).filter(rol__rol='Утверждает экспертизу')
        if Personal_utvergdaet.exists():
            for k in Personal_utvergdaet:
                utvergdaet_familiya = k.person.familiya
                utvergdaet_imya = k.person.imya
                utvergdaet_otchestvo = k.person.otchestvo
                List_utvergdaet.append(str(
                    utvergdaet_familiya) + ' ' + str(utvergdaet_imya) + ' ' + str(utvergdaet_otchestvo))
        else:
            List_utvergdaet.append('')

        Personal_expert = JERPerson.objects.select_related('expertiza').filter(
            expertiza__id=id_expertiza).filter(rol__rol='Эксперт')
        List_expert = []
        for k in Personal_expert:
            expert_familiya = k.person.familiya
            expert_imya = k.person.imya
            expert_otchestvo = k.person.otchestvo
            List_expert.append(str(expert_familiya) + ' ' +
                               str(expert_imya) + ' ' + str(expert_otchestvo))
            List_expert.append('</br>')

        Personal_rukovoditel = JERPerson.objects.select_related('expertiza').filter(
            expertiza__id=int(id_expertiza)).filter(rol__rol='Руководитель экспертизы')
        List_rukovoditel = []
        for k in Personal_rukovoditel:
            rukovoditel_familiya = k.person.familiya
            rukovoditel_imya = k.person.imya
            rukovoditel_otchestvo = k.person.otchestvo
            List_rukovoditel.append(str(rukovoditel_familiya) + ' ' +
                                    str(rukovoditel_imya) + ' ' + str(rukovoditel_otchestvo))

        Personal_rukovoditel_otdeleniya = JERPerson.objects.select_related('expertiza').filter(
            expertiza__id=int(id_expertiza)).filter(rol__rol='Руководитель ответственного подразделения')
        List_rukovoditel_otdeleniya = []
        for k in Personal_rukovoditel_otdeleniya:
            rukovoditel_familiya = k.person.familiya
            rukovoditel_imya = k.person.imya
            rukovoditel_otchestvo = k.person.otchestvo
            List_rukovoditel_otdeleniya.append(str(
                rukovoditel_familiya) + ' ' + str(rukovoditel_imya) + ' ' + str(rukovoditel_otchestvo))

        name_Ex_zakl = ''

        def output_data_file(QuerySet):
            """
            Функция по формирования списка файлов и их url
            """
            url = 'Отсутствует'
            list_= []
            if QuerySet.exists() == True:
                for obj in QuerySet:
                    dict_ = {}
                    dict_['url'] = obj.document.fayl.url
                    dict_['name'] = obj.document.fayl.name.replace("file/", "")
                    url = 'Присутствует'
                    list_.append(dict_)
                return (url,list_)
            else:
                return (url,list_)
        
        fayl_url_pismo_org, L_pismoOrganizacii = output_data_file(Pismo_ot_organizacii)
        fayl_url_pismo_v_org, L_pismovOrganizacii = output_data_file(Pismo_v_organizaciu)
        fayl_url_pismo_v_org_garant, L_pismovOrganizaciiGaranrt = output_data_file(Pismo_v_organizaciuGarant)
        fayl_url_pismo_rtn, L_pismoRTN = output_data_file(Pismo_RTN)
        fayl_url_v_pismo_rtn, L_pismovRTN = output_data_file(Pismo_v_RTN)
        fayl_url_zapros_tkp, L_zaprosTKP = output_data_file(Zapros_TKP)
        fayl_url_otvet_tkp, L_otvetTKP = output_data_file(Otvet_TKP)
        fayl_url_dogov_TZ, L_pismoDogovor = output_data_file(Pismo_Dogovor_TZ)
        fayl_url_otvet_dogov_TZ, L_otvetDogovor = output_data_file(Otvet_Pismo_Dogovor_TZ)
        fayl_url_zapros_ceni, L_zaprosCeni = output_data_file(Snigenie_cen)
        fayl_url_otvet_ceni, L_otvetCeni = output_data_file(Otvet_snigenie_cen)
        fayl_url_garant_pismo, L_garantPismo = output_data_file(Garant_pismo)
        fayl_url_proekt_norm, L_proektNormativov = output_data_file(Proekt_normat)
        fayl_url_akt, L_Akt = output_data_file(AKT)
        fayl_url_sluzhebki, L_Sluzhebki = output_data_file(Sluzhebki)

        L_zaklDogovor = []
        if Zakl_dogovor.exists() == True:
            for obj1 in Zakl_dogovor:
                C_zaklDogovor = {}
                C_zaklDogovor['url'] = obj1.document.fayl.url
                C_zaklDogovor['name'] = obj1.document.fayl.name.replace(
                    "file/", "")
                L_zaklDogovor.append(C_zaklDogovor)
                fayl_url_zakl_dogov = obj1.document.fayl.url
                id_zakl_dogov = obj1.document.id
            try:
                data_document = Data_documenta.filter(opisanie_data__opisanie="Срок подготовки ответа").get(
                    document__id=id_zakl_dogov).data.strftime("%d.%m.%Y")
            except:
                data_document = 'Не утверждено'
        else:
            data_document = ''
            fayl_url_zakl_dogov = 'Отсутствует'


        if ExpertZakluchenie.exists() == True:
            for obj1 in ExpertZakluchenie:
                fayl_url_Ex_zakl = obj1.document.fayl.url
                name_Ex_zakl = obj1.document.fayl.name.replace("file/", "")
                id_exp_zakl = obj1.document.id
                if nomer_expertnogo_zaklucheniya == '':
                    nomer_expertnogo_zaklucheniya = 'Номер не указан'
                try:
                    data_document = Data_documenta.filter(opisanie_data__opisanie="Дата утверждения экспертного заключения").get(
                    document__id=id_exp_zakl).data.strftime("%d.%m.%Y")
                except:
                    data_document = 'Нет даты утверждения'
                break
        else:
            fayl_url_Ex_zakl = 'Отсутствует'

 
        action_list = {}
        for action in LogEntry.objects.filter(object_id=id_expertiza).select_related().order_by('-action_time'):
            key = '+%s' % action.pk
            user = '%s %s' % (action.user.last_name, action.user.first_name) if action.user.first_name or action.user.last_name else '%s' % action.user.username
            action_time = localtime(action.action_time).strftime("%d.%m.%Y %H:%M")
            if get_change_message(action) != '':
                action_list[key] = user, action_time, get_change_message(action)

        data = {
            'otraslevaya_prinad': otraslevaya_prinad,
            'nazvanie_polnoe': nazvanie_polnoe,
            'gos_usluga': gos_usluga,
            'vse_istochiki': vse_istochiki,
            'neorg_istochniki': neorg_istochniki,

            'list_ot_organizacii': L_pismoOrganizacii,
            'list_v_organizacii': L_pismovOrganizacii,
            'list_v_organizacii_garant':L_pismovOrganizaciiGaranrt,
            'list_pismo_v_rtn': L_pismovRTN,
            'list_pismo_rtn': L_pismoRTN,
            'list_zapros_tkp': L_zaprosTKP,
            'list_otvet_tkp': L_otvetTKP,
            'list_pismo_dogovor': L_pismoDogovor,
            'list_otvet_dogovor': L_otvetDogovor,
            'list_zapros_ceni': L_zaprosCeni,
            'list_otvet_ceni': L_otvetCeni,
            'list_garant_pismo': L_garantPismo,
            'list_zakl_dogovor': L_zaklDogovor,
            'list_proekt_normativov': L_proektNormativov,
            'list_Akt': L_Akt,
            'list_sluzhebki': L_Sluzhebki,

            'url_pismo_org': fayl_url_pismo_org,
            'url_pismo_v_org': fayl_url_pismo_v_org,
            'url_pismo_v_org_garant':fayl_url_pismo_v_org_garant,
            'url_pismo_v_rtn': fayl_url_v_pismo_rtn,
            'url_pismo_rtn': fayl_url_pismo_rtn,
            'url_zapros_tkp1': fayl_url_zapros_tkp,
            'url_otvet_tkp': fayl_url_otvet_tkp,
            'url_dogov_TZ': fayl_url_dogov_TZ,
            'url_otvet_dogov_TZ': fayl_url_otvet_dogov_TZ,
            'url_zapros_ceni': fayl_url_zapros_ceni,
            'url_otvet_ceni': fayl_url_otvet_ceni,
            'url_garant_pismo': fayl_url_garant_pismo,
            'url_zakl_dogov': fayl_url_zakl_dogov,
            'url_proekt_norm': fayl_url_proekt_norm,
            'url_Ex_zakl': fayl_url_Ex_zakl,
            'url_akt': fayl_url_akt,
            'url_sluzhebki': fayl_url_sluzhebki,

            'name_Ex_zakl': name_Ex_zakl,

            'rukovoditel': List_rukovoditel,
            'utvergdaet': List_utvergdaet,
            'expert': List_expert,
            'rukovod_otdeleniya': List_rukovoditel_otdeleniya,

            'editor': redactor,
            'data_document': data_document,
            'nomer_expertnogo_zaklucheniya':nomer_expertnogo_zaklucheniya,

            'action_list': action_list,
        }

        return JsonResponse(data)
    else:
        data = {
            'response': 'Запрос не GET'
        }
        return JsonResponse(data)


def get_modal_table_archive(request):
    """Функция по выводу информации по экспертизе в Архиве через модальное окно """
    if request.GET:
        data = {}
        id_ytv_expertizi = int(request.GET.get('id_ex_arch'))
        Documenti_vse = DtipDocument.objects.select_related(
            'document__expertiza__organizaciya__tip')
        QS_Data_utvergdeniya = JdataDocument.objects.select_related('document').filter(
            opisanie_data__opisanie="Дата утверждения экспертного заключения")

        Expertiza = Cexpertiza.objects.select_related(
            'organizaciya__tip').get(id=id_ytv_expertizi)
        # ----
        if Expertiza.tip.tip == 'Выброс':
            gos_usluga = 'Разрешение на выброс радиоактивных веществ в атмосферу'
        elif Expertiza.tip.tip == 'Сброс':
            gos_usluga = 'Разрешение на сброс радиоактивных веществ в водный объект'

        if Expertiza.kolichestvo_istochnikov == None or str(Expertiza.kolichestvo_istochnikov)[0] == '0':
            vse_istochiki = 0
        else:
            vse_istochiki = Expertiza.kolichestvo_istochnikov
        if Expertiza.neorganizovan_istochniki == None or str(Expertiza.neorganizovan_istochniki)[0] == '0':
            neorg_istochniki = 0
        else:
            neorg_istochniki = Expertiza.neorganizovan_istochniki
        
        nazvanie_polnoe = Expertiza.organizaciya.nazvanie_polnoe
        nomer_DNP = str(Expertiza.nomer_expertizi)
        #-----       A
        Pismo_ot_organizacii = Documenti_vse.filter(document__expertiza__id=int(
            id_ytv_expertizi)).filter(tip__tip="Письмо из организации о проведении экспертизы")
        Pismo_v_organizaciu = Documenti_vse.filter(document__expertiza__id=int(
            id_ytv_expertizi)).filter(tip__tip="Письмо в организацию по договору")
        Pismo_RTN = Documenti_vse.filter(document__expertiza__id=int(id_ytv_expertizi)).filter(
            tip__tip="Письмо из Ростехнадзора/Территориального органа о проведении экспертизы")
        Pismo_v_RTN = Documenti_vse.filter(document__expertiza__id=int(
            id_ytv_expertizi)).filter(tip__tip="Письмо в Ростехнадзор")
        Zapros_TKP = Documenti_vse.filter(document__expertiza__id=int(
            id_ytv_expertizi)).filter(tip__tip="Запрос ТКП")
        Otvet_TKP = Documenti_vse.filter(document__expertiza__id=int(
            id_ytv_expertizi)).filter(tip__tip="Ответ на запрос ТКП")
        Zakl_dogovor = Documenti_vse.filter(document__expertiza__id=int(
            id_ytv_expertizi)).filter(tip__tip="Договор заключенный")
        Proekt_normat = Documenti_vse.filter(document__expertiza__id=int(
            id_ytv_expertizi)).filter(tip__tip="Проект нормативов")
        ExpertZakluchenie = Documenti_vse.filter(document__expertiza__id=int(
            id_ytv_expertizi)).filter(tip__tip="Экспертное заключение")
        Act = Documenti_vse.filter(document__expertiza__id=int(
            id_ytv_expertizi)).filter(tip__tip="Акт")

        #-----       B
        def output_data_file(QuerySet):
            """
            Функция по формирования списка файлов и их url
            """
            url = 'Отсутствует'
            list_= []
            if QuerySet.exists() == True:
                for obj in QuerySet:
                    dict_ = {}
                    dict_['url'] = obj.document.fayl.url
                    dict_['name'] = obj.document.fayl.name.replace("file/", "")
                    url = 'Присутствует'
                    list_.append(dict_)
                return (url,list_)
            else:
                return (url,list_)
        
        fayl_url_pismo_rtn, L_pismoRTN = output_data_file(Pismo_RTN)
        fayl_url_pismo_v_rtn, L_pismovRTN = output_data_file(Pismo_v_RTN)
        fayl_url_pismo_org, L_pismoOrganizacii = output_data_file(Pismo_ot_organizacii)
        fayl_url_pismo_v_org, L_pismovOrganizacii = output_data_file(Pismo_v_organizaciu)
        fayl_url_zapros_tkp, L_zaprosTKP = output_data_file(Zapros_TKP)
        fayl_url_otvet_tkp, L_otvetTKP = output_data_file(Otvet_TKP)
        fayl_url_zakl_dogov, L_zaklDogovor = output_data_file(Zakl_dogovor)
        fayl_url_proekt_norm, L_proektNormativov = output_data_file(Proekt_normat)
        fayl_url_act, L_Akt = output_data_file(Act)
        
        L_expertnZakluchenie = []
        try:
            for obj1 in ExpertZakluchenie:
                id_documentExpZaklucheniya = obj1.document.id
                C_expertnZakluchenie = {}
                C_expertnZakluchenie['url'] = obj1.document.fayl.url
                C_expertnZakluchenie['name'] = obj1.document.fayl.name
                L_expertnZakluchenie.append(C_expertnZakluchenie)
                fayl_url_Ex_zakl = obj1.document.fayl.url
        except:
            fayl_url_Ex_zakl = 'Отсутствует'

        Person_expertiz = JERPerson.objects.filter(
            rol__rol='Утверждает экспертизу').filter(expertiza__id=id_ytv_expertizi)
        Rukovoditel_expertiz = JERPerson.objects.filter(
            rol__rol='Руководитель экспертизы').filter(expertiza__id=id_ytv_expertizi)
        Experti_expertiz = JERPerson.objects.filter(
            rol__rol='Эксперт').filter(expertiza__id=id_ytv_expertizi)
        Rukovoditel_podrazdeleniya = JERPerson.objects.filter(
            rol__rol='Руководитель ответственного подразделения').filter(expertiza__id=id_ytv_expertizi)
        
        def output_data_human(QuerySet):
            """
            Функция по формирования списка имен людей
            """
            list_ = []
            try:
                for k in QuerySet:
                    list_.append(str(k.person.familiya)+' ' +
                                    str(k.person.imya)+' '+str(k.person.otchestvo))
                    list_.append('</br>')
                return list_
            except:
                return list_
        
        List_expert = output_data_human(Experti_expertiz)
        List_utv_exp = output_data_human(Person_expertiz)
        List_ruk_exp = output_data_human(Rukovoditel_expertiz)
        List_ruk_podrazd = output_data_human(Rukovoditel_podrazdeleniya)
        
        # ------------------------
        try:
            data_utvergdeniya = QS_Data_utvergdeniya.get(
                document__id=id_documentExpZaklucheniya).data.strftime("%d.%m.%Y")
        except:
            data_utvergdeniya = 'Не выставлена'

        action_list = {}
        for action in LogEntry.objects.filter(object_id=id_ytv_expertizi).select_related().order_by('-action_time'):
            key = '+%s' % action.pk
            user = '%s %s' % (action.user.last_name, action.user.first_name) if action.user.first_name or action.user.last_name else '%s' % action.user.username
            action_time = localtime(action.action_time).strftime("%d.%m.%Y %H:%M")
            if get_change_message(action) != '':
                action_list[key] = user, action_time, get_change_message(action)

        data = {
            'full_name_utvergd': List_utv_exp,
            'full_name_ruk': List_ruk_exp,
            'full_name_exp': List_expert,
            'full_name_ruk_podraz': List_ruk_podrazd,

            'list_pismo_rtn': L_pismoRTN,
            'list_pismo_v_rtn': L_pismovRTN,
            'list_pismo_ot_org': L_pismoOrganizacii,
            'list_pismo_v_org': L_pismovOrganizacii,
            'list_zapros_tkp': L_zaprosTKP,
            'list_otvet_tkp': L_otvetTKP,
            'list_zakl_dogovor': L_zaklDogovor,
            'list_expertn_zakl': L_expertnZakluchenie,
            'list_proekt_normat': L_proektNormativov,
            'list_akt': L_Akt,

            'nazvanie_polnoe': nazvanie_polnoe,
            'gos_usluga': gos_usluga,

            'url_pismo_org': fayl_url_pismo_org,
            'url_pismo_v_org': fayl_url_pismo_v_org,
            'url_pismo_rtn': fayl_url_pismo_rtn,
            'url_pismo_v_rtn': fayl_url_pismo_v_rtn,
            'url_zapros_tkp1': fayl_url_zapros_tkp,
            'url_otvet_tkp': fayl_url_otvet_tkp,
            'url_zakl_dogov': fayl_url_zakl_dogov,
            'url_proekt_norm': fayl_url_proekt_norm,
            'url_Ex_zakl': fayl_url_Ex_zakl,
            'url_act': fayl_url_act,
            'data_utvergd': data_utvergdeniya,

            'nomer_DNP': nomer_DNP,

            'vse_istochniki': vse_istochiki,
            'neorg_istochniki': neorg_istochniki,

            'action_list': action_list,
        }

        return JsonResponse(data)
    else:
        return JsonResponse({'data': 'beda'})


def get_change_message(obj):
    """
    If self.change_message is a JSON structure, interpret it as a change
    string, properly translated.
    """
    if obj.change_message and obj.change_message[0] == '[':
        try:
            change_message = json.loads(obj.change_message)
        except json.JSONDecodeError:
            return obj.change_message
        messages = []
        for sub_message in change_message:
            if 'added' in sub_message:
                if sub_message['added']:
                    sub_message['added']['name'] = gettext(sub_message['added']['name'])
                    messages.append(gettext('Added {name} “{object}”.').format(**sub_message['added']))
                else:
                    messages.append(gettext('Added.'))

            elif 'changed' in sub_message:
                sub_message['changed']['fields'] = get_text_list(
                    [gettext(field_name) for field_name in sub_message['changed']['fields']], gettext('and')
                )
                if 'name' in sub_message['changed']:
                    sub_message['changed']['name'] = gettext(sub_message['changed']['name'])
                    messages.append(gettext('Changed {fields} for {name} “{object}”.').format(**sub_message['changed']))
                else:
                    messages.append(gettext('Changed {fields}.').format(**sub_message['changed']))

            elif 'deleted' in sub_message:
                sub_message['deleted']['name'] = gettext(sub_message['deleted']['name'])
                messages.append(gettext('Deleted {name} “{object}”.').format(**sub_message['deleted']))

            messages.append('</br>')

        change_message = ' '.join(msg[0].upper() + msg[1:] for msg in messages)
        return change_message
    else:
        return obj.change_message
