from django.shortcuts import render
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out

# Create your views here.

@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):
    user.profile.is_online = True
    user.profile.save()


@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):
    user.profile.is_online = False
    user.profile.save()
