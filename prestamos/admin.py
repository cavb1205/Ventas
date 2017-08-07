from django.contrib import admin
from prestamos.models import Cartera,Utilidades, Usuarios, Base,Tipo_Gasto,Gastos,Plazos,Estado_Prestamo,Prestamos,Recaudos

admin.site.register(Cartera)
admin.site.register(Usuarios)
admin.site.register(Base)
admin.site.register(Tipo_Gasto)
admin.site.register(Gastos)
admin.site.register(Plazos)
admin.site.register(Estado_Prestamo)
admin.site.register(Prestamos)
admin.site.register(Recaudos)
admin.site.register(Utilidades)