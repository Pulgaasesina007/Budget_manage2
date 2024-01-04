from django.contrib import admin
from .models import user_perfil,Gastos,Tipo_Gasto,Tipo_Ingreso,Ingresos

admin.site.register(user_perfil)
admin.site.register(Gastos)
admin.site.register(Tipo_Gasto)
admin.site.register(Tipo_Ingreso)
admin.site.register(Ingresos)
