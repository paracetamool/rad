from django.db import models
from datetime import datetime
import os
import re

def disch_doc_path(instance, filename):
    if instance.expertiza.tip.tip == 'Выброс':
        return os.path.join("ВиС/%s" % ('Выбросы/'+str(instance.expertiza.data.strftime ("%Y.%m.%d"))+'-ПДВ-'+str(instance.expertiza.organizaciya.nazvanie_korotkoe) ), filename)
    elif instance.expertiza.tip.tip == 'Сброс':
        return os.path.join("ВиС/%s" % ('Сбросы/'+str(instance.expertiza.data.strftime ("%Y.%m.%d"))+'-ДС-'+str(instance.expertiza.organizaciya.nazvanie_korotkoe) ), filename)
    

class DOtipObyect(models.Model):
    """" Класс - отраслевая принадлежность организации (ОИАЭ, Концерн Росэнергоатом) """
    tip = models.CharField(max_length=200, verbose_name='Тип объекта')

    def __str__(self):
        return self.tip

    class Meta:
        ordering = ('tip',)
        verbose_name = 'Тип объекта'
        verbose_name_plural = 'Типы объекта'



class Corganizaciya(models.Model):
    """" Класс - название организации """
    tip = models.ForeignKey(DOtipObyect, max_length=200, verbose_name='Тип объекта', on_delete=models.CASCADE)
    nazvanie_korotkoe = models.CharField(max_length=200, verbose_name='Название объекта короткое', null=True, blank=True)
    nazvanie_polnoe = models.CharField(max_length=200, verbose_name='Название объекта полное', null=True, blank=True)
    nazvanie_select = models.CharField(max_length=200, verbose_name='Название для Select', null=True, blank=True)
    opisanie = models.TextField(verbose_name='Описание объекта')

    def __str__(self):
        return self.nazvanie_korotkoe

    class Meta:
        ordering = ('nazvanie_korotkoe',)
        verbose_name = 'Название организации'
        verbose_name_plural = 'Названия организации'

    def save(self):
        QS = Corganizaciya.objects.all()
        # при помощи регулярных выражений заменяем простые кавы на "ёлочки"
        str_1_nazvanie_korotkoe = re.sub(r'^\"|(?<=[\s\(])"|"(?=\w+)',r'«',self.nazvanie_korotkoe)
        str_2_nazvanie_korotkoe = re.sub(r'\"$|(?=\))"|"(?=\s)',r'»',str_1_nazvanie_korotkoe)
        self.nazvanie_korotkoe = str_2_nazvanie_korotkoe

        str_1_nazvanie_polnoe = re.sub(r'^\"|(?<=[\s\(])"|"(?=\w+)',r'«',self.nazvanie_polnoe)
        str_2_nazvanie_polnoe = re.sub(r'\"$|(?=\))"|"(?=\s)',r'»',str_1_nazvanie_polnoe)
        self.nazvanie_polnoe = str_2_nazvanie_polnoe

        str_1_nazvanie_select = re.sub(r'^\"|(?<=[\s\(])"|"(?=\w+)',r'«',self.nazvanie_select)
        str_2_nazvanie_select = re.sub(r'\"$|(?=\))"|"(?=\s)',r'»',str_1_nazvanie_select)
        self.nazvanie_select = str_2_nazvanie_select

        str_1_opisanie = re.sub(r'^\"|(?<=[\s\(])"|"(?=\w+)',r'«',self.opisanie)
        str_2_opisanie = re.sub(r'\"$|(?=\))"|"(?=\s)',r'»',str_1_opisanie)
        self.opisanie = str_2_opisanie
        for organizacii in QS:
            if self.nazvanie_korotkoe == organizacii.nazvanie_korotkoe:
                break
            else:
                super(Corganizaciya, self).save()


class DEtipExperizi(models.Model):
    """" Класс - тип государственной услуги """
    tip = models.CharField(max_length=200, verbose_name='Тип государственной услуги (выброс / сброс)')
    opisanie = models.TextField(verbose_name='Описание типа Экспертизы')

    def __str__(self):
        return self.tip    

    class Meta:
        verbose_name = 'Тип экспертизы'
        verbose_name_plural = 'Типы экспертизы'


class Cexpertiza(models.Model):
    """" Класс - экспертиза проекта нормативов по государственной услуге """
    organizaciya = models.ForeignKey(Corganizaciya, max_length=200, verbose_name='Название объекта',
                                     on_delete=models.CASCADE)
    tip = models.ForeignKey(DEtipExperizi, max_length=200, verbose_name='Тип экспертизы', on_delete=models.CASCADE)
    kolichestvo_istochnikov = models.IntegerField(max_length=200, verbose_name='Количество источников', null=True,
                                                  blank=True)
    neorganizovan_istochniki = models.CharField(max_length=200, verbose_name='Количество неорганизованных источников',
                                                null=True,  blank=True)
    data = models.DateField(auto_now=False, verbose_name='Дата начала экспертизы', null=True, blank=True)
    # prochaya_inf = models.TextField(verbose_name='Прочая информация о Разрешении', blank=True)
    nomer_expertizi = models.CharField(max_length=100, verbose_name='Номер экспертизы', blank=True)
    # nomer = models.IntegerField(verbose_name='Число таких экспертиз в году', null=True, blank=True, default=1)
    is_deleted = models.BooleanField(verbose_name='Передана в архив', default=False, blank=True )

    def __str__(self):
        return ' %s' % (self.organizaciya.nazvanie_korotkoe)+ '. Экспертиза на ' + ' %s' % (self.tip.tip)

    class Meta:
        ordering = ('nomer_expertizi',)
        verbose_name = 'Экспертиза организации'
        verbose_name_plural = 'Экспертизы организации'

    def save(self):
        value1 = Cexpertiza.objects.select_related('expertiza__organizaciya__tip').filter(kolichestvo_istochnikov=self.kolichestvo_istochnikov, neorganizovan_istochniki = self.neorganizovan_istochniki,   tip__tip = self.tip.tip, organizaciya__nazvanie_korotkoe = self.organizaciya.nazvanie_korotkoe  ).count()
        self.nomer = value1 + 1
        data_seichas = datetime.now().date()
        if self.data == None:
            self.data = data_seichas
        super(Cexpertiza, self).save()



class CEdocument(models.Model):
    """" Класс - документы по экспертизе """
    expertiza = models.ForeignKey(Cexpertiza, max_length=200, verbose_name='Выбор необходимой экспертизы',
                                  on_delete=models.CASCADE)
    fayl = models.FileField(upload_to=disch_doc_path, blank=True, verbose_name='Загружаемый документ', max_length=500)

    def __str__(self):
        return '%s' % self.fayl.name.split('/')[-1]


    class Meta:
        verbose_name = 'Документ экспертизы'
        verbose_name_plural = 'Документы экспертизы'


class DProli(models.Model):
    """" Класс - роль произвольного человека (эксперт, руководитель работы) """
    rol = models.CharField(max_length=200, verbose_name='Роль человека')

    def __str__(self):
        return self.rol    	

    class Meta:
        ordering = ('rol',)
        verbose_name = 'Роль человека'
        verbose_name_plural = 'Роли человека'


class DannieCheloveka(models.Model):
    """" Класс - основная информация по человеку """
    imya = models.CharField(max_length=200, verbose_name='Имя человека')
    familiya = models.CharField(max_length=200, verbose_name='Фамилия человека')
    otchestvo = models.CharField(max_length=200, verbose_name='Отчество человека')
    pochta = models.CharField(max_length=200, verbose_name='Почта человека')

    def __str__(self):
        return '%s %s %s' % (self.familiya, self.imya, self.otchestvo)

    class Meta:
        ordering = ('familiya',)
        verbose_name = 'Данные человека'
        verbose_name_plural = 'Данные людей'


class JERPerson(models.Model):
    """" Класс - информация по участнику экспертизы (связь данных ченловека с экспертизой) """
    expertiza = models.ForeignKey(Cexpertiza,  max_length=200, verbose_name='Выбор необходимой экспертизы',
                                  on_delete=models.CASCADE)
    rol = models.ForeignKey(DProli, blank=True, max_length=200, verbose_name='Выбор необходимой роли', on_delete=models.CASCADE)
    person = models.ForeignKey(DannieCheloveka, blank=True, max_length=2000, verbose_name='Выбор необходимого человека',
                               on_delete=models.CASCADE)


    def __str__(self):
        return self.person.imya + ' ' + self.person.familiya

    class Meta:
        verbose_name = 'Участник экспертизы'
        verbose_name_plural = 'Участники экспертизы'



class DTipData(models.Model):
    """" Класс - типы дат """
    opisanie = models.TextField(verbose_name='Описание даты')

    def __str__(self):
        return self.opisanie  

    class Meta:
        ordering = ('opisanie',)
        verbose_name = 'Тип даты'
        verbose_name_plural = 'Типы даты'



class JdataDocument(models.Model):
    """" Класс - связь дат с документом """
    document = models.ForeignKey(CEdocument, max_length=200, verbose_name='Выбор необходимого документа',
                                 on_delete=models.CASCADE)
    data = models.DateField(auto_now=False, blank=True, verbose_name='Дата выдачи / получения документа')
    opisanie_data = models.ForeignKey(DTipData, blank=True, max_length=200, verbose_name='Тип даты',
                                      on_delete=models.CASCADE)

    def __str__(self):
        return str(self.document.expertiza.organizaciya.nazvanie_korotkoe) + ' - ' +   self.opisanie_data.opisanie 


    class Meta:
        verbose_name = 'Дата документов'
        verbose_name_plural = 'Даты документов'


class Dtip(models.Model):
    """" Класс - типы документов """
    tip = models.TextField(verbose_name='Тип документа')

    def __str__(self):
        return self.tip  

    class Meta:
        ordering = ('tip',)
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class DtipDocument(models.Model):
    """" Класс - связь типов документов с документами """
    document = models.ForeignKey(CEdocument, max_length=200, verbose_name='Выбор необходимого документа',
                                 on_delete=models.CASCADE)
    tip = models.ForeignKey(Dtip, blank=True, max_length=200, verbose_name='Выбор необходимого типа документа',
                            on_delete=models.CASCADE)

    def __str__(self):
        return self.tip.tip

    class Meta:
        verbose_name = 'Тип документа'
        verbose_name_plural = 'Типы документа'


class DDmtu(models.Model):
    """" Класс - название Ростехнадзора или его территориального органа """
    krat = models.CharField(max_length=50, verbose_name="Краткое название МТУ")
    poln = models.CharField(blank=True, max_length=500, verbose_name="Полное название МТУ")

    def __str__(self):
        return self.krat

    class Meta:
        ordering = ('krat',)
        verbose_name = 'МТУ'
        verbose_name_plural = 'МТУ'


class JDDrazr(models.Model):
    """" Класс - связь документа (разрешения) с РТН или ТО """
    document = models.ForeignKey(DtipDocument, verbose_name='Тип документа', on_delete=models.CASCADE)
    nomer = models.CharField(max_length=100, blank=True, verbose_name='Номер разрешения')
    kem_vidano = models.ForeignKey(DDmtu, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Кем выдано')
    opisanie = models.TextField(blank=True, verbose_name='Дополнительные сведения')

    def __str__(self):
        return self.nomer

    class Meta:
        verbose_name = 'Разрешение'
        verbose_name_plural = 'Разрешения'
