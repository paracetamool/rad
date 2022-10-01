from django.db import models
from colorfield.fields import ColorField

# Create your models here.


class Dcolors(models.Model):
    color = ColorField(blank=True, default='#FF0000', verbose_name="Цвет")

    def __str__(self):
        return self.color

    class Meta:
        ordering = ('id',)
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'


class MainStatistics(models.Model):
    user = models.CharField(max_length=1000, null=True, verbose_name="Пользователь")
    url = models.URLField(null=True, verbose_name="URL")
    ip = models.GenericIPAddressField(null=True, verbose_name="IP пользователя")
    browser = models.CharField(max_length=1000, null=True, verbose_name="Браузер пользователя")
    session_key = models.CharField(max_length=1000, null=True, verbose_name="Ключ сессии")
    dactivity = models.DateTimeField(null=True, verbose_name="Время активности")

    def save(self):
        if ('ajax' in self.url) or ('get' in self.url) or ('update' in self.url) \
                or ('terms-and-conditions' in self.url) or ('summernote' in self.url) \
                or ('jsi18n' in self.url) or ('tableToExcel' in self.url) or ('favicon' in self.url) \
                or ('login' in self.url) or ('.js' in self.url) or ('.css' in self.url) or ('profile_info' in self.url):
            pass
        else:
            super(MainStatistics, self).save()

    class Meta:
        ordering = ('dactivity',)


class QueryStatistics(models.Model):
    app_stat = models.ForeignKey(MainStatistics, on_delete=models.CASCADE)
    filter = models.TextField(verbose_name="Фильтры")


# class DownloadStatistics(models.Model):
#     app_stat = models.ForeignKey(MainStatistics, on_delete=models.CASCADE)
#     name = models.CharField(max_length=5000, verbose_name="Скаченный файл")
