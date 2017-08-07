"""cartera URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from prestamos import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.inicio),
    url(r'^bienvenido/$',views.bienvenido),
    url(r'^logs/$',views.logs),
    url(r'^informes/$',views.informes),
    url(r'^usuarios/page/(?P<pagina>.*)/$',views.usuarios),
    url(r'^add_usuario/$',views.add_usuario),
    url(r'^edit_usuario/(?P<id_usuario>.*)/$',views.edit_usuario),
    url(r'^delete_usuario/(?P<id_usuario>.*)/$',views.delete_usuario),
    url(r'^usuarios/(?P<id_usuario>.*)/$',views.usuario_individual),
    url(r'^usuario_prestamos/(?P<id_usuario>.*)/$',views.usuario_prestamos),
    url(r'^almacen/$',views.carteras),
    url(r'^add_almacen/$',views.add_cartera),
    url(r'^edit_almacen/(?P<id_cartera>.*)/$',views.edit_cartera),
    url(r'^delete_almacen/(?P<id_cartera>.*)/$',views.delete_cartera),
    url(r'^almacen/(?P<id_cartera>.*)/$',views.cartera_individual),
    url(r'^almacen_base/(?P<id_cartera>.*)/$',views.cartera_base),
    url(r'^almacen_gastos/(?P<id_cartera>.*)/$',views.cartera_gastos),
    url(r'^almacen_usuarios/(?P<id_cartera>.*)/$',views.cartera_usuarios),
    url(r'^almacen_ventas_finalizados/(?P<id_cartera>.*)/$',views.cartera_prestamos_finalizados),
    url(r'^almacen_ventas_vigentes/(?P<id_cartera>.*)/$',views.cartera_prestamos_vigentes),
    url(r'^almacen_ventas_vencidos/(?P<id_cartera>.*)/$',views.cartera_prestamos_vencidos),
    url(r'^almacen_ventas_perdidas/(?P<id_cartera>.*)/$',views.cartera_prestamos_perdidas),
    url(r'^almacen_utilidades/(?P<id_cartera>.*)/$',views.cartera_utilidades),
    url(r'^almacen_recaudos/(?P<id_cartera>.*)/$',views.cartera_recaudos),
    url(r'^almacen_recaudos/(?P<id_cartera>)/page/(?P<pagina>.*)/$',views.cartera_recaudos),
    url(r'^bases/page/(?P<pagina>.*)/$',views.bases),
    url(r'^add_base/$',views.add_base),
    url(r'^edit_base/(?P<id_base>.*)/$',views.edit_base),
    url(r'^delete_base/(?P<id_base>.*)/$',views.delete_base),
    url(r'^base/(?P<id_base>.*)/$',views.base_individual),
    url(r'^utilidades/page/(?P<pagina>.*)/$',views.utilidades),
    url(r'^utilidad/(?P<id_utilidad>.*)/$',views.utilidad_individual),
    url(r'^add_utilidad/$',views.add_utilidad),
    url(r'^edit_utilidad/(?P<id_utilidad>.*)/$',views.edit_utilidad),
    url(r'^delete_utilidad/(?P<id_utilidad>.*)/$',views.delete_utilidad),
    url(r'^gastos/page/(?P<pagina>.*)/$',views.gastos),
    url(r'^add_gasto/$',views.add_gasto),
    url(r'^delete_gasto/(?P<id_gasto>.*)/$',views.delete_gasto),
    url(r'^edit_gasto/(?P<id_gasto>.*)/$',views.edit_gasto),
    url(r'^gasto/(?P<id_gasto>.*)/$',views.gasto_individual),
    url(r'^ventas/page/(?P<pagina>.*)/$',views.historial_prestamos),
    url(r'^ventas/(?P<id_prestamo>.*)/$',views.prestamo_individual),
    url(r'^ventas_vigentes/page/(?P<pagina>.*)/$',views.prestamos_vigentes),
    url(r'^ventas_vigentes/(?P<id_prestamo>.*)/$',views.prestamo_vigente_individual),
    url(r'^add_venta/$',views.add_prestamo),
    url(r'^edit_ventas_vigentes/(?P<id_prestamo>.*)/$',views.edit_prestamo),
    url(r'^delete_venta/(?P<id_prestamo>.*)/$',views.delete_prestamo),
    url(r'^close_venta_vigente/(?P<id_prestamo>.*)/$',views.close_prestamo_vigente),
    url(r'^fecha/$',views.fecha),
    
    url(r'^fecha_liq_ventas/$',views.fecha_liq_ventas),
    url(r'^fecha_liq_ventas_fecha/(?P<fecha>.*)/$',views.fecha_liq_ventas_fecha),
    
    
    url(r'^fecha_admin/(?P<id_cartera>.*)/$',views.fecha_admin),
    url(r'^liquidar_almacen/$',views.liquidar_cartera),
    url(r'^liquidar_almacen_admin/(?P<id_cartera>.*)/$',views.liquidar_cartera_admin),
    url(r'^liquidar_ventas/page/(?P<pagina>.*)/$',views.liquidar_prestamos),
    url(r'^liquidar_ventas_x_fecha/page/(?P<pagina>.*)/$',views.liquidar_prestamos_fecha),
    url(r'^recaudos/page/(?P<pagina>.*)/$',views.recaudos),
    url(r'^informe_recaudos_hoy_admin/(?P<id_cartera>.*)/$',views.informe_recaudos_hoy_admin),
    url(r'^informe_recaudos_hoy/$',views.informe_recaudos_hoy),
    url(r'^almacen_informe_recaudos_hoy/(?P<id_cartera>.*)/$',views.cartera_informe_recaudos_hoy),
    url(r'^add_recaudo/$',views.add_recaudo),
    url(r'^add_recaudo/(?P<id_prestamo>.*)/$',views.add_abono),
    
    
    url(r'^add_recaudo_x_fecha/(?P<id_prestamo>.*)/(?P<fecha>.*)/$',views.add_abono_x_fecha),
    url(r'^edit_recaudo/(?P<id_recaudo>.*)/$',views.edit_recaudo),
    url(r'^delete_recaudo/(?P<id_recaudo>.*)/$',views.delete_recaudo),
    url(r'^recaudo/(?P<id_recaudo>.*)/$',views.recaudo_individual),
    url(r'^add_recaudo_confirm/(?P<id_prestamo>.*)/$',views.add_recaudo_confirm),
    url(r'^add_venta_confirm/$',views.add_prestamo_confirm),
    url(r'^cerrar_dia/(?P<fecha>.*)/$',views.cerrar_dia),
    url(r'^login/$',views.login_view),
    url(r'^logout/$',views.logout_view),


]
