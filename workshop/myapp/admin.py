from django.contrib import admin
from django.views.generic.edit import CreateView
from .models import Univalluno, ArticuloDeportivo, Prestamo, Multa
from datetime import datetime, time, timedelta

class UnivallunoAdmin(admin.ModelAdmin):
    list_display = ('tipo_documento', 'numero_documento', 'nombres', 'apellidos', 'codigo_estudiante', 'correo_electronico', 'tipo_univalluno')
    def get_readonly_fields(self, request, obj=None):
        if obj: # esto es cuando el objeto ya está creado es decir, estamos en el modo de edición
            return ['numero_documento', 'tipo_documento']
        else:
            return []

class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('id', 'univalluno', 'articulo_deportivo', 'fecha_hora_prestamo', 'fecha_hora_vencimiento', 'devuelto')
    exclude = ('fecha_hora_prestamo', 'fecha_hora_vencimiento')
    readonly_fields = ('fecha_hora_prestamo', 'fecha_hora_vencimiento')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "articulo_deportivo":
            kwargs["queryset"] = ArticuloDeportivo.objects.filter(disponible=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
class MultaAdmin(admin.ModelAdmin):
    list_display = ('prestamo', 'fecha_hora_generacion', 'fecha_hora_pago', 'monto', 'multa_pagada')
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:  # Verifica si el objeto está siendo cambiado y no creado
            obj.pagar_multa()

admin.site.register(Univalluno, UnivallunoAdmin)
admin.site.register(Prestamo, PrestamoAdmin)
admin.site.register(ArticuloDeportivo)
admin.site.register(Multa, MultaAdmin)
