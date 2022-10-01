from phonenumber_field.modelfields import PhoneNumberField
from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

# Create your models here.


class Dorg(models.Model):
    krat = models.CharField(max_length=50, verbose_name="Краткое название организации")
    poln = models.CharField(blank=True, max_length=500, verbose_name="Полное название организации")
    tel1 = PhoneNumberField(blank=True, null=True, verbose_name="Номер телефона секретариата")
    tel2 = PhoneNumberField(blank=True, null=True, verbose_name="Номер телефона приемной")
    email = models.EmailField(blank=True, null=True, max_length=100, verbose_name="Электронная почта")
    url = models.URLField(blank=True, null=True, max_length=1000, verbose_name="Электронный адрес")
    adr = models.CharField(blank=True, null=True, max_length=1000, verbose_name="Почтовый адрес")

    def __str__(self):
        return self.krat

    class Meta:
        ordering = ('krat',)
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class Profile(models.Model):
    CHOISE_STATUS = [
        (False, 'Вне сети'),
        (True, 'В сети'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="Имя пользователя")
    org = models.ForeignKey(Dorg, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Организация")
    is_online = models.BooleanField(blank=True, default=False, choices=CHOISE_STATUS, verbose_name="Статус")
    last_activity = models.DateTimeField(blank=True, default=timezone.now, verbose_name="Время последней активности")
    color = ColorField(blank=True, default='#FF0000', verbose_name="Цвет профиля")
    user_agreement = models.DateField(null=True, blank=True, verbose_name="Дата ознакомления с пользовательским соглашением и согласием на обработку персональных данных")

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ('-last_activity',)
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
