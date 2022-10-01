from django.contrib import admin
from nested_admin import NestedModelAdmin, NestedStackedInline
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput
from colorfield.fields import ColorField
from django.contrib.auth.models import User
from .models import Dorg, Profile

# Register your models here.


class ProfileInline(NestedStackedInline):
    model = Profile
    exclude = ('is_online', 'last_activity')
    can_delete = False
    verbose_name_plural = 'Доп. информация'
    formfield_overrides = {
        ColorField: {'widget': TextInput(attrs={'type': 'color'})}
    }
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)


class MyUserAdmin(NestedModelAdmin, UserAdmin):
    def joined(self, obj):
        return obj.date_joined.strftime("%d.%m.%Y")

    joined.admin_order_field = 'date_joined'
    joined.short_description = 'Дата регистрации'

    def org(self, obj):
        return obj.profile.org

    org.admin_order_field = 'profile__org'
    org.short_description = 'Организация'

    def agreement(self, obj):
        return obj.profile.user_agreement

    agreement.admin_order_field = 'profile__user_agreement'
    agreement.short_description = 'Дата ознакомления'

    list_display = ('username', 'last_name', 'first_name', 'email', 'joined',
                    'org', 'is_superuser', 'is_staff', 'is_active', 'agreement')
    list_editable = ('is_active',)
    list_filter = ('is_staff', 'is_superuser',
                   'is_active', 'groups', 'profile__org')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('date_joined',)
    inlines = (ProfileInline,)
    save_on_top = True

    class Meta:
        model = User


admin.site.register(Dorg)
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
