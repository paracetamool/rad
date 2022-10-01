from django.contrib import admin
from django.db.models import ForeignKey, Q
from django.http import HttpResponseRedirect
from nested_admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline
from .models import DOtipObyect, Corganizaciya, DEtipExperizi, Cexpertiza, CEdocument, DProli, DannieCheloveka, \
    JERPerson, DTipData, JdataDocument, Dtip, DtipDocument, DDmtu, JDDrazr


# Register your models here.


class JERPersonInline(NestedTabularInline):
    model = JERPerson
    fields = ('person', 'rol')
    min_num = 1
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)
    formfield_overrides = {
        ForeignKey: {'empty_label': 'Выберите...'},
    }

    def get_extra(self, request, obj=None, **kwargs):
        return 0 if obj and obj.jerperson_set.exists() else 0


class JDDrazrInline(NestedTabularInline):
    model = JDDrazr
    min_num = 1
    max_num = 1
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)
    formfield_overrides = {
        ForeignKey: {'empty_label': 'Выберите...'},
    }

    # def has_change_permission(self, request, obj=None):
    #     return False
    #
    # def has_add_permission(self, request, obj=None):
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False


class ExistDtipDocumentInline(NestedTabularInline):
    model = DtipDocument
    extra = 0
    readonly_fields = ('tip',)
    inlines = (JDDrazrInline,)

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False if request.user.groups.filter(name='Редакторы ПЭО').exists() else True


class AddDtipDocumentInline(NestedTabularInline):
    model = DtipDocument
    min_num = 1
    inlines = (JDDrazrInline,)
    inline_classes = ('grp-collapse grp-open',)
    formfield_overrides = {
        ForeignKey: {'empty_label': 'Выберите...'},
    }

    def get_extra(self, request, obj=None, **kwargs):
        return 0 if obj and obj.dtipdocument_set.exists() else 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        query, EXCLUDE_MARK = Q(), ('Разрешен', 'норматив', 'заключен')
        if db_field.name == "tip":
            for entry in EXCLUDE_MARK:
                query = query | Q(tip__icontains=entry)
            kwargs["queryset"] = Dtip.objects.exclude(query) if \
                request.user.groups.filter(name='Редакторы ПЭО').exists() else Dtip.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return False


class JdataDocumentInline(NestedTabularInline):
    model = JdataDocument
    min_num = 3
    inline_classes = ('grp-collapse grp-open',)
    formfield_overrides = {
        ForeignKey: {'empty_label': 'Выберите...'},
    }

    def get_extra(self, request, obj=None, **kwargs):
        return 0 if obj and obj.jdatadocument_set.exists() else 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "opisanie_data":
            kwargs["queryset"] = DTipData.objects.exclude(opisanie__icontains='разрешен') if \
                request.user.groups.filter(name='Редакторы ПЭО').exists() else DTipData.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        return False if request.user.groups.filter(name='Редакторы ПЭО').exists() else True

    def has_delete_permission(self, request, obj=None):
        return False if request.user.groups.filter(name='Редакторы ПЭО').exists() else True


class CEdocumentInline(NestedStackedInline):
    model = CEdocument
    min_num = 1
    fields = ('fayl',)
    inlines = (ExistDtipDocumentInline, AddDtipDocumentInline, JdataDocumentInline)
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-closed',)

    def get_extra(self, request, obj=None, **kwargs):
        return 0 if obj and obj.cedocument_set.exists() else 0

    def has_change_permission(self, request, obj=None):
        return False if request.user.groups.filter(name='Редакторы ПЭО').exists() else True

    def has_delete_permission(self, request, obj=None):
        return False if request.user.groups.filter(name='Редакторы ПЭО').exists() else True


class CexpertizaAdmin(NestedModelAdmin):
    list_display = ('organizaciya', 'tip', 'data_1', 'kolichestvo_istochnikov', 'nomer_expertizi', 'is_deleted')
    list_filter = ('organizaciya', 'tip', 'is_deleted')
    search_fields = ('organizaciya__nazvanie_korotkoe', 'tip__tip')
    ordering = ('-data',)
    list_per_page = 50
    fields = (('organizaciya', 'tip', 'is_deleted'), ('kolichestvo_istochnikov', 'neorganizovan_istochniki'),
              'nomer_expertizi')
    inlines = (JERPersonInline, CEdocumentInline)
    formfield_overrides = {
        ForeignKey: {'empty_label': 'Выберите...'},
    }

    def data_1(self, obj):
        return obj.data.strftime("%d.%m.%Y")

    data_1.admin_order_field = 'data'
    data_1.short_description = 'Дата начала экспертизы'

    def get_form(self, request, obj=None, **kwargs):
        form = super(CexpertizaAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.groups.filter(name='Редакторы ПЭО').exists():
            form.base_fields['nomer_expertizi'].widget.attrs['style'] = 'width: 118px;'
            form.base_fields['is_deleted'].help_text = '<p style="color:red;">Нажимаем на данное поле при передачи Экспертного заключения архив</p>'
        return form

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='Редакторы ПЭО').exists():
            return ('organizaciya', 'tip', 'is_deleted', 'nomer_expertizi', 'kolichestvo_istochnikov',
                    'neorganizovan_istochniki', 'data', 'prochaya_inf')
        else:
            return super(CexpertizaAdmin, self).get_readonly_fields(request, obj)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if not request.user.is_superuser:
            extra_context['show_save'] = True
            extra_context['show_save_and_continue'] = True
            extra_context['show_save_and_add_another'] = False
        else:
            pass
        return super(CexpertizaAdmin, self).changeform_view(request, object_id, extra_context=extra_context)

    def response_add(self, request, obj, post_url_continue="../%s/"):
        if not request.user.is_superuser and '_continue' not in request.POST:
            return HttpResponseRedirect('/')
        else:
            return super(CexpertizaAdmin, self).response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        if not request.user.is_superuser and '_continue' not in request.POST:
            return HttpResponseRedirect('/')
        else:
            return super(CexpertizaAdmin, self).response_change(request, obj)

    class Meta:
        model = Cexpertiza

    class Media:
        js = ('js/admin/admin.js',)
        css = {
            'all': ('css/admin/admin.css',)
        }


admin.site.register(Cexpertiza, CexpertizaAdmin)
admin.site.register(DOtipObyect)
admin.site.register(Corganizaciya)
admin.site.register(DEtipExperizi)
admin.site.register(DProli)
admin.site.register(DannieCheloveka)
admin.site.register(DTipData)
admin.site.register(Dtip)
admin.site.register(DDmtu)
admin.site.register(DtipDocument)
