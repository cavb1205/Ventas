from django.shortcuts import render, redirect
from prestamos.models import Cobro,Dia,Usuarios,Cartera,Base,Gastos,Prestamos,Recaudos,Utilidades,Estado_Prestamo
from django.shortcuts import render_to_response, get_object_or_404, render
from prestamos.forms import CarteraForm, BaseForm,BaseAdminForm,Close_PrestamosForm,fechaForm, GastosForm, GastosAdminForm, UsuariosForm,UsuariosAdminForm, PrestamosForm,PrestamosAdminForm, RecaudosAdminForm,RecaudosForm,LoginForm,UtilidadesAdminForm,UtilidadesForm
from django.contrib.auth import authenticate, login as auth_login
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin import widgets
from datetime import datetime,timedelta,date
import json
from django.contrib.admin.models import LogEntry
from decimal import Decimal
from datetime import datetime
from django.core.urlresolvers import reverse


# Create your views here.
@login_required(login_url='/login/')
def inicio(request):
	return render_to_response('inicio.html',{'inicio':inicio},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def cerrar_dia(request,fecha):
	print 'ingresa a cerrar_dia'
	f = datetime.strptime(fecha, "%Y-%m-%d")
	print 'nueva fecha'
	print f
	dias = timedelta(days=1)
	print 'diasssssssssssssssssssssssssssssssssss'
	print dias
	sum_dia = f + dias
	print sum_dia
	cartera = Cartera.objects.get(responsable=request.user.id)
	registros = Dia.objects.filter(id_cartera=cartera).filter(fecha=sum_dia)
	cobros = Cobro.objects.filter(id_cartera=cartera).filter(fecha=f)
	prestamos = Prestamos.objects.filter(id_cartera=cartera).exclude(estado_prestamo=2).exclude(estado_prestamo=5)
	sum_prestamos = 0
	for prestamo in prestamos:
		sum_prestamos = sum_prestamos + prestamo.saldo_actual		

	if registros:
		print 'ingresa al if registros'
		print registros
		#for registro in registros:
		#	print 'registro viejo'
		#	print registro.valor
		#	print 'nuevo registro'
		#	registro.valor = cartera.monto
		#	print registro.valor
		#	registro.save()
		#	print 'guarda el registro'
		
	else:
		dia = Dia(fecha=sum_dia,valor=cartera.monto,id_cartera=cartera)
		dia.save()
		print 'guarda el dia'

	if cobros:
		print 'ingresa al if del cobro'
		print cobros
#		for cobro in cobros:
#			print 'cobro viejo'
#			print cobro.valor
#			print 'nuevo cobro'
#			cobro.valor = sum_prestamos
#			print cobro.valor
#			print 'pre save'
#			cobro.save()
#			print 'se guardo el cobro'			
	else:
		print 'ingresa al else del cobro'
		cobro = Cobro(fecha=f,valor=sum_prestamos,id_cartera=cartera)
		cobro.save()
		print 'guarda el cobro'


	return HttpResponseRedirect('/almacen/')


@login_required(login_url='/login/')
def bienvenido(request):
	if request.user.is_superuser:
		return render_to_response('bienvenido.html',context_instance=RequestContext(request))
	else:

		return render_to_response('bienvenido.html',context_instance=RequestContext(request))
	
@login_required(login_url='/login/')
def logs(request):
	logs = LogEntry.objects.all()
	print logs
	return render_to_response('logs.html',{'logs':logs},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def informes(request):
	return render_to_response('informes.html',context_instance=RequestContext(request))

@login_required(login_url='/login/')
def usuarios(request,pagina):
	if request.user.is_superuser:
		usuarios = Usuarios.objects.all().order_by('apellidos')
	else:
		cartera = Cartera.objects.filter(responsable_id=request.user.id)
		usuarios = Usuarios.objects.filter(id_cartera=cartera).order_by('apellidos')

	paginator = Paginator(usuarios,50)
	try:
		page = int(pagina)
	except:
		page = 1
	try:
		list_usuarios = paginator.page(page)
	except (EmptyPage, InvalidPage):
		list_usuarios = paginator.page(paginator.num_pages)

	return render_to_response('usuarios.html',{'usuarios':list_usuarios},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def usuarios_renovacion(request,pagina):
	cartera = Cartera.objects.filter(responsable_id=request.user.id)
	print 'consultamos prestamos'
	prestamos = Prestamos.objects.filter(id_cartera=cartera).exclude(estado_prestamo_id=2)
	lista = []
	for x in prestamos:
		print x.id_usuarios_id
		lista.append(x.id_usuarios_id)
	print 'imprime lista'
	print lista
	usuarios = Usuarios.objects.filter(id_cartera=cartera).filter(estado=True).exclude(id__in=lista)
	paginator = Paginator(usuarios,50)
	try:
		page = int(pagina)
	except:
		page = 1
	try:
		list_usuarios = paginator.page(page)
	except (EmptyPage, InvalidPage):
		list_usuarios = paginator.page(paginator.num_pages)
	return render_to_response('usuarios_renovacion.html',{'usuarios':list_usuarios},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def usuario_individual(request,id_usuario):	
	usuario = Usuarios.objects.get(id=id_usuario)
	return render_to_response('usuario_individual.html',{'usuario':usuario},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def usuario_prestamos(request,id_usuario):
	prestamos = Prestamos.objects.filter(id_usuarios=id_usuario).order_by('estado_prestamo')
	return render_to_response('usuario_prestamos.html',{'prestamos':prestamos},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def delete_usuario(request,id_usuario):	
	usuario = Usuarios.objects.get(id=id_usuario)
	prestamos = Prestamos.objects.filter(id_usuarios=id_usuario)
	if prestamos:
		return render_to_response('delete_usuario.html',{'usuario':usuario},context_instance=RequestContext(request))
	else:
		usuario.delete()
		return render_to_response('delete.html',{'usuario':usuario},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def carteras(request):
	if request.user.is_superuser:
		carteras = Cartera.objects.all()
	else:
		carteras = Cartera.objects.filter(responsable_id=request.user.id)
		
	return render_to_response('carteras.html',{'carteras':carteras},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def cartera_individual(request,id_cartera):
	cartera = Cartera.objects.get(id=id_cartera)
	bases = Base.objects.filter(id_cartera=id_cartera)
	gastos = Gastos.objects.filter(id_cartera=id_cartera)
	utilidades = Utilidades.objects.filter(id_cartera=id_cartera)
	prestamos = Prestamos.objects.filter(id_cartera=id_cartera).exclude(estado_prestamo=2).exclude(estado_prestamo=5)
	perdidas = Prestamos.objects.filter(id_cartera=id_cartera).filter(estado_prestamo=5)
	recaudos = Recaudos.objects.filter(id_cartera=id_cartera)
	finalizados = Prestamos.objects.filter(id_cartera=id_cartera)
	sum_utilidades = 0
	sum_perdidas = 0
	sum_bases = 0
	sum_gastos = 0
	sum_prestamos = 0
	sum_recaudos = 0
	sum_finalizados = 0
	parcial = 0
	ingresos_prestamo=0
	abono = 0
	sum_r = 0
	abono_perdida = 0
	faltante = 0
	sum_recaudo_perdidas = 0
	for base in bases:
		sum_bases = sum_bases + base.valor
	for gasto in gastos:
		sum_gastos = sum_gastos + gasto.valor
	for utilidad in utilidades:
		sum_utilidades = sum_utilidades + utilidad.valor_utilidad
	for prestamo in prestamos:
		sum_prestamos = sum_prestamos + prestamo.saldo_actual
	for perdida in perdidas:
		sum_perdidas=sum_perdidas + perdida.saldo_actual
		
	for recaudo in recaudos:
		sum_recaudos = sum_recaudos + recaudo.valor
	for finalizado in finalizados:
		sum_finalizados = sum_finalizados + ((finalizado.monto_inicial*finalizado.interes)/100)
		faltante = faltante + finalizado.saldo_actual
		
		
		
	ingresos_prestamo = sum_finalizados
	
	total = sum_bases + sum_finalizados - faltante -sum_gastos -sum_utilidades - sum_perdidas

	return render_to_response('cartera_individual.html',{'cartera':cartera,'sum_recaudo_perdidas':sum_recaudo_perdidas,'ingresos_prestamo':ingresos_prestamo,'total':total,'sum_recaudos':sum_recaudos,'sum_perdidas':sum_perdidas,'sum_prestamos':sum_prestamos,'sum_utilidades':sum_utilidades,'sum_bases':sum_bases,'sum_gastos':sum_gastos},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def delete_cartera(request,id_cartera):
	if request.user.is_superuser:
		cartera = Cartera.objects.get(id=id_cartera)
		prestamos = Prestamos.objects.filter(id_cartera=id_cartera).exclude(estado_prestamo_id=2)
		if prestamos:
			return render_to_response('delete_cartera.html',{'cartera':cartera},context_instance=RequestContext(request))
		else:
			cartera.delete()
			return render_to_response('delete.html',{'cartera':cartera},context_instance=RequestContext(request))
			
@login_required(login_url='/login/')			
def utilidades(request,pagina):
	if request.user.is_superuser:
		utilidades = Utilidades.objects.all().order_by('-id')
	else:
		cartera = Cartera.objects.filter(responsable_id=request.user.id)
		utilidades = Utilidades.objects.filter(id_cartera=cartera).order_by('-id')

	paginator = Paginator(utilidades,50)
	try:
		page = int(pagina)
	except:
		page = 1
	try:
		list_utilidades = paginator.page(page)
	except (EmptyPage, InvalidPage):
		list_utilidades = paginator.page(paginator.num_pages)

	return render_to_response('utilidades.html',{'utilidades':list_utilidades},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def utilidad_individual(request,id_utilidad):
	utilidad = Utilidades.objects.get(id=id_utilidad)
	return render_to_response('utilidad_individual.html',{'utilidad':utilidad},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def delete_utilidad(request,id_utilidad):
	utilidad = Utilidades.objects.get(id=id_utilidad)
	utilidad.delete()
	cartera = Cartera.objects.get(id=utilidad.id_cartera.id)
	cartera.monto = cartera.monto+utilidad.valor_utilidad
	cartera.save()
	return render_to_response('delete.html',{'utilidad':utilidad},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def cartera_base(request,id_cartera):
	bases = Base.objects.filter(id_cartera=id_cartera)
	return render_to_response('cartera_base.html',{'bases':bases,'id_cartera':id_cartera},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def cartera_gastos(request,id_cartera):
	gastos = Gastos.objects.filter(id_cartera=id_cartera)
	return render_to_response('cartera_gastos.html',{'gastos':gastos,'id_cartera':id_cartera},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def cartera_usuarios(request,id_cartera):
	usuarios = Usuarios.objects.filter(id_cartera=id_cartera)
	return render_to_response('cartera_usuarios.html',{'usuarios':usuarios,'id_cartera':id_cartera},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def cartera_utilidades(request,id_cartera):
	utilidades = Utilidades.objects.filter(id_cartera=id_cartera)
	return render_to_response('utilidades.html',{'utilidades':utilidades,'id_cartera':id_cartera},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def cartera_recaudos(request,id_cartera):
	print "ingresa a la funcion en el views.py"
	recaudos = Recaudos.objects.filter(id_cartera=id_cartera)
	paginator = Paginator(recaudos,100)
	try:
		page = int(pagina)
	except:
		page = 1
	try:
		list_recaudos = paginator.page(page)
	except (EmptyPage, InvalidPage):
		list_recaudos = paginator.page(paginator.num_pages)
	return render_to_response('cartera_recaudos.html',{'recaudos':list_recaudos,'id_cartera':id_cartera},context_instance=RequestContext(request))

	#return render_to_response('cartera_recaudos.html',{'recaudos':recaudos,'id_cartera':id_cartera},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def cartera_prestamos_finalizados(request,id_cartera):
	prestamos = Prestamos.objects.filter(id_cartera=id_cartera).filter(estado_prestamo=2)
	return render_to_response('cartera_prestamos.html',{'prestamos':prestamos,'id_cartera':id_cartera},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def cartera_prestamos_vigentes(request,id_cartera):
	prestamos = Prestamos.objects.filter(id_cartera=id_cartera).exclude(estado_prestamo=2).exclude(estado_prestamo=5)
	return render_to_response('cartera_prestamos.html',{'prestamos':prestamos,'id_cartera':id_cartera},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def cartera_prestamos_vencidos(request,id_cartera):
	prestamos = Prestamos.objects.filter(id_cartera=id_cartera).filter(estado_prestamo=4)
	return render_to_response('cartera_prestamos.html',{'prestamos':prestamos},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def cartera_prestamos_perdidas(request,id_cartera):
	prestamos = Prestamos.objects.filter(id_cartera=id_cartera).filter(estado_prestamo=5)
	return render_to_response('cartera_prestamos.html',{'prestamos':prestamos,'id_cartera':id_cartera},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def cartera_informe_recaudos_hoy(request,id_cartera):
	hoy = date.today()
	total = 0
	print id_cartera
	filtro = Recaudos.objects.filter(id_cartera=id_cartera).filter(fecha_recaudo=hoy)
	for x in filtro:
		total = total + x.valor
	return render_to_response('informe_recaudos_fecha.html',{'filtro':filtro,'total':total},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def bases(request,pagina):
	if request.user.is_superuser:
		bases = Base.objects.all().order_by('-id')
	else:
		cartera = Cartera.objects.filter(responsable_id=request.user.id)
		bases = Base.objects.filter(id_cartera=cartera).order_by('-id')
	
	paginator = Paginator(bases,50)
	try:
		page = int(pagina)
	except:
		page = 1
	try:
		list_bases = paginator.page(page)
	except (EmptyPage, InvalidPage):
		list_bases = paginator.page(paginator.num_pages)
	
	return render_to_response('bases.html',{'bases':list_bases},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def base_individual(request,id_base):
	base = Base.objects.get(id=id_base)
	return render_to_response('base_individual.html',{'base':base},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def delete_base(request,id_base):
	if request.user.is_superuser:
		base = Base.objects.get(id=id_base)
		base.delete()
		cartera = Cartera.objects.get(id=base.id_cartera.id)
		cartera.monto = cartera.monto-base.valor
		cartera.save()
		return render_to_response('delete.html',{'base':base},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def gastos(request,pagina):
	if request.user.is_superuser:
		gastos = Gastos.objects.all().order_by('-id')
	else:
		cartera = Cartera.objects.filter(responsable_id=request.user.id)
		gastos = Gastos.objects.filter(id_cartera=cartera).order_by('-id')

	paginator = Paginator(gastos,50)
	try:
		page = int(pagina)
	except:
		page = 1
	try:
		list_gastos = paginator.page(page)
	except (EmptyPage, InvalidPage):
		list_gastos = paginator.page(paginator.num_pages)

	return render_to_response('gastos.html',{'gastos':list_gastos},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def gasto_individual(request,id_gasto):
	gasto = Gastos.objects.get(id=id_gasto)
	return render_to_response('gasto_individual.html',{'gasto':gasto},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def delete_gasto(request,id_gasto):
	gasto = Gastos.objects.get(id=id_gasto)
	gasto.delete()
	cartera = Cartera.objects.get(id=gasto.id_cartera.id)
	cartera.monto = cartera.monto+gasto.valor
	cartera.save()
	return render_to_response('delete.html',{'gasto':gasto},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def historial_prestamos(request,pagina):
	if request.user.is_superuser:
		prestamos = Prestamos.objects.all().order_by('-id')
	else:
		cartera = Cartera.objects.filter(responsable_id=request.user.id)
		prestamos = Prestamos.objects.filter(id_cartera=cartera).order_by('-id')


	paginator = Paginator(prestamos,50)
	try:
		page = int(pagina)
	except:
		page = 1
	try:
		list_prestamos = paginator.page(page)
	except (EmptyPage, InvalidPage):
		list_prestamos = paginator.page(paginator.num_pages)
	return render_to_response('historial_prestamos.html',{'prestamos':list_prestamos},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def prestamo_individual(request,id_prestamo):
	prestamo = Prestamos.objects.get(id=id_prestamo)
	recaudos = Recaudos.objects.filter(id_prestamo=id_prestamo).order_by('-id')
	return render_to_response('prestamo_individual.html',{'prestamo':prestamo,'recaudos':recaudos},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def prestamos_vigentes(request,pagina):
	if request.user.is_superuser:
		prestamos = Prestamos.objects.exclude(estado_prestamo_id='2').order_by('-id').exclude(estado_prestamo=5)
	else:
		cartera = Cartera.objects.filter(responsable_id=request.user.id)
		prestamos = Prestamos.objects.filter(id_cartera=cartera).exclude(estado_prestamo=2).exclude(estado_prestamo=5)


	paginator = Paginator(prestamos,50)
	try:
		page = int(pagina)
	except:
		page = 1
	try:
		list_prestamos = paginator.page(page)
	except (EmptyPage, InvalidPage):
		list_prestamos = paginator.page(paginator.num_pages)
	return render_to_response('prestamos_vigentes.html',{'prestamos':list_prestamos},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def prestamo_vigente_individual(request,id_prestamo):
	prestamo = Prestamos.objects.get(id=id_prestamo)
	recaudos = Recaudos.objects.filter(id_prestamo=id_prestamo).order_by('-id')
	return render_to_response('prestamo_vigente_individual.html',{'prestamo':prestamo,'recaudos':recaudos},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def recaudos(request,pagina):
	if request.user.is_superuser:
		recaudos = Recaudos.objects.all().order_by('-id')
	

	else:
		cartera = Cartera.objects.filter(responsable_id=request.user.id)
		recaudos = Recaudos.objects.filter(id_cartera=cartera).order_by('-id')

	paginator = Paginator(recaudos,50)
	try:
		page = int(pagina)
	except:
		page = 1
	try:
		list_recaudos = paginator.page(page)
	except (EmptyPage, InvalidPage):
		list_recaudos = paginator.page(paginator.num_pages)

	return render_to_response('recaudos.html',{'recaudos':list_recaudos},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def informe_recaudos_hoy_admin(request,id_cartera):
	if request.user.is_superuser:
		hoy = date.today()
		total = 0
		cartera = Cartera.objects.filter(id=id_cartera)
		filtro = Recaudos.objects.filter(id_cartera=cartera).filter(fecha_recaudo=hoy)
		for x in filtro:
			total = total + x.valor
		return render_to_response('informe_recaudos_fecha.html',{'filtro':filtro,'total':total,'id_cartera':id_cartera},context_instance=RequestContext(request))
	
@login_required(login_url='/login/')
def informe_recaudos_hoy(request):
	print 'ingresa al else'
	hoy = date.today()
	total = 0
	cartera = Cartera.objects.filter(responsable_id=request.user.id)
	filtro = Recaudos.objects.filter(id_cartera=cartera).filter(fecha_recaudo=hoy)
	print cartera
	for x in filtro:
		total = total + x.valor
	return render_to_response('informe_recaudos_fecha.html',{'filtro':filtro,'total':total},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def liquidar_prestamos(request,pagina):
	if request.user.is_superuser:
		prestamos = Prestamos.objects.exclude(estado_prestamo_id='2').order_by('-id').exclude(estado_prestamo=5)
	#	return render_to_response('liquidar_prestamos.html',{'prestamos':list_prestamos},context_instance=RequestContext(request))
	else:
		print 'estamos en el else de liquidar_prestamos'
		cartera = Cartera.objects.filter(responsable_id=request.user.id)
		prestamos = Prestamos.objects.filter(id_cartera=cartera).exclude(estado_prestamo=2).exclude(estado_prestamo=5)
		

	paginator = Paginator(prestamos,50)
	try:
		page = int(pagina)
	except:
		page = 1
	try:
		list_prestamos = paginator.page(page)
	except (EmptyPage, InvalidPage):
		list_prestamos = paginator.page(paginator.num_pages)

	return render_to_response('liquidar_prestamos.html',{'prestamos':list_prestamos},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def liquidar_prestamos_fecha(request,pagina):
	if request.user.is_superuser:
		prestamos = Prestamos.objects.exclude(estado_prestamo_id='2').order_by('-id').exclude(estado_prestamo=5)
	#	return render_to_response('liquidar_prestamos.html',{'prestamos':list_prestamos},context_instance=RequestContext(request))
	else:
		print 'estamos en el else de liquidar_prestamos'
		cartera = Cartera.objects.filter(responsable_id=request.user.id)
		prestamos = Prestamos.objects.filter(id_cartera=cartera).exclude(estado_prestamo=2).exclude(estado_prestamo=5)
		

	paginator = Paginator(prestamos,50)
	try:
		page = int(pagina)
	except:
		page = 1
	try:
		list_prestamos = paginator.page(page)
	except (EmptyPage, InvalidPage):
		list_prestamos = paginator.page(paginator.num_pages)

	return render_to_response('liquidar_prestamos.html',{'prestamos':list_prestamos},context_instance=RequestContext(request))



@login_required(login_url='/login/')		
def recaudo_individual(request,id_recaudo):
	
	recaudos = Recaudos.objects.get(id=id_recaudo)
	return render_to_response('recaudo_individual.html',{'recaudos':recaudos},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def delete_recaudo(request,id_recaudo):
	recaudo = Recaudos.objects.get(id=id_recaudo)
	recaudo.delete()
	prestamo = Prestamos.objects.get(id=recaudo.id_prestamo.id)
	prestamo.saldo_actual = prestamo.saldo_actual + recaudo.valor
	if prestamo.saldo_actual > 0:
		prestamo.estado_prestamo_id = 1
	prestamo.save()
	cartera = Cartera.objects.get(id=recaudo.id_cartera.id)
	cartera.monto = cartera.monto-recaudo.valor
	cartera.save()
	return render_to_response('delete.html',{'recaudo':recaudo},context_instance=RequestContext(request))

## vistas formularios ##
@login_required(login_url='/login/')
def add_cartera(request):
	if request.method=='POST':
		formulario = CarteraForm(request.POST)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/almacen/')
	else:
		formulario = CarteraForm()
	return render_to_response('carteraform.html',{'formulario':formulario},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def edit_cartera(request,id_cartera):
	cartera = Cartera.objects.get(id=id_cartera)
	
	if request.method == 'POST':
		formulario = CarteraForm(request.POST,instance=cartera)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/almacen/%s/'%cartera.id)
	else:
		formulario = CarteraForm(instance=cartera)
	

	return render_to_response('edit_carteraform.html',{'formulario':formulario},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def add_base(request):
	if request.user.is_superuser:
		if request.method=='POST':
			formulario = BaseAdminForm(request.POST)
			
			if formulario.is_valid():
				base = formulario.save(commit=False)
				print 'obtengo el valor de la base que se agrego is_superuser'	
				print base.valor
				print base.id_cartera
				print 'obtengo la cartera que va a ser modificada'
				base.save()
				cartera = Cartera.objects.get(id=base.id_cartera.id)
				print cartera.monto
				cartera.monto = cartera.monto+base.valor
				cartera.save()
				print cartera.monto
				return HttpResponseRedirect('/bases/page/1')
		else:
			formulario = BaseAdminForm(initial={'fecha_entrega':date.today()})
		return render_to_response('baseform.html',{'formulario':formulario},context_instance=RequestContext(request))
	else:
		if request.method=='POST':
			formulario = BaseForm(request.POST)
			
			if formulario.is_valid():
				base = formulario.save(commit=False)
				print 'obtengo el valor de la base que se agrego  cobrador'	
				print base.valor
				usuario = request.user
				print 'obtengo la cartera que va a ser modificada'
				responsable = Cartera.objects.get(responsable=usuario.id)
				print 'responsable'
				print responsable
				print 'guardar el usuario en el id_cartera'
				base.id_cartera = responsable
				base.save()
				cartera = Cartera.objects.get(id=base.id_cartera.id)
				print cartera.monto
				cartera.monto = cartera.monto+base.valor
				cartera.save()
				print cartera.monto
				return HttpResponseRedirect('/bases/page/1')
		else:
			formulario = BaseForm(initial={'fecha_entrega':date.today()})
		return render_to_response('baseform.html',{'formulario':formulario},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def edit_base(request,id_base):
  
	base = Base.objects.get(id=id_base)
	viejo = base.valor
	if request.method == 'POST':
		formulario = BaseForm(request.POST,instance=base)
		if formulario.is_valid():
			formulario.save()
			cartera = Cartera.objects.get(id=base.id_cartera.id)
			print 'nuevo'
			print base.valor
			if viejo < base.valor:
				diferencia = base.valor - viejo
				print 'diferencia'
				print diferencia
				cartera.monto = cartera.monto+diferencia
			else:
				diferencia = viejo - base.valor
				print 'diferencia else'
				print diferencia
				cartera.monto = cartera.monto-diferencia
			cartera.save()

			return HttpResponseRedirect('/base/%s/'%base.id)
	else:
		print 'viejo'
		viejo = base.valor
		print viejo
		formulario = BaseForm(instance=base)
	

	return render_to_response('edit_baseform.html',{'formulario':formulario},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def add_utilidad(request):
	
	if request.user.is_superuser:

		if request.method=='POST':	
			formulario = UtilidadesAdminForm( request.POST)
			if formulario.is_valid():
				utilidad = formulario.save(commit=False)
				print 'obtengo el valor de la utilidad que se agrego is_superuser'	
				print utilidad.valor_utilidad
				
				utilidad.save()
				print 'obtengo la cartera que va a ser modificada'
				cartera = Cartera.objects.get(id=utilidad.id_cartera.id)
				print cartera.monto
				cartera.monto = cartera.monto-utilidad.valor_utilidad
				cartera.save()
				print cartera.monto
				return HttpResponseRedirect('/utilidades/page/1')
		else:
			formulario = UtilidadesAdminForm(initial={'fecha_entrega':date.today()})
		return render_to_response('utilidadesform.html',{'formulario':formulario},context_instance=RequestContext(request))


	else:
		if request.method=='POST':	
			formulario = UtilidadesForm( request.POST)
			if formulario.is_valid():
				utilidad = formulario.save(commit=False)
				
				usuario = request.user
				responsable = Cartera.objects.get(responsable=usuario.id)
				print 'responsable'
				print responsable
				print 'guardar el usuario en el id_cartera'
				utilidad.id_cartera = responsable
				print utilidad.id_cartera
				utilidad.save()
				print 'obtengo la cartera que va a ser modificada'
				cartera = Cartera.objects.get(id=utilidad.id_cartera.id)
				print cartera.monto
				cartera.monto = cartera.monto-utilidad.valor_utilidad
				cartera.save()
				print cartera.monto
				return HttpResponseRedirect('/utilidades/page/1')
					

		else:
			formulario = UtilidadesForm(initial={'fecha_entrega':date.today()})
		return render_to_response('utilidadesform.html',{'formulario':formulario},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def edit_utilidad(request,id_utilidad):
	utilidad = Utilidades.objects.get(id=id_utilidad)
	viejo = utilidad.valor_utilidad

	if request.user.is_superuser:
		if request.method == 'POST':
			formulario = UtilidadesAdminForm(request.POST,instance=utilidad)
			if formulario.is_valid():	
				formulario.save()
				cartera = Cartera.objects.get(id=utilidad.id_cartera.id)
				print 'nuevo'
				print utilidad.valor_utilidad
				if viejo < utilidad.valor_utilidad:
					diferencia = utilidad.valor_utilidad - viejo
					print 'diferencia'
					print diferencia
					cartera.monto = cartera.monto-diferencia
				else:
					diferencia = viejo - utilidad.valor_utilidad
					print 'diferencia else'
					print diferencia
					cartera.monto = cartera.monto+diferencia
				cartera.save()
				return HttpResponseRedirect('/utilidad/%s/'%utilidad.id)
		else:
			print 'viejo'
			viejo = utilidad.valor_utilidad
			print viejo
			formulario = UtilidadesAdminForm(instance=utilidad)
		return render_to_response('edit_utilidadform.html',{'formulario':formulario},context_instance=RequestContext(request))

	else:
		if request.method == 'POST':
			formulario = UtilidadesForm(request.POST,instance=utilidad)
			if formulario.is_valid():
				
				formulario.save()
				cartera = Cartera.objects.get(id=utilidad.id_cartera.id)
				print 'nuevo'
				print utilidad.valor_utilidad
				if viejo < utilidad.valor_utilidad:
					diferencia = utilidad.valor_utilidad - viejo
					print 'diferencia'
					print diferencia
					cartera.monto = cartera.monto-diferencia
				else:
					diferencia = viejo - utilidad.valor_utilidad
					print 'diferencia else'
					print diferencia
					cartera.monto = cartera.monto+diferencia
				cartera.save()
				return HttpResponseRedirect('/utilidad/%s/'%utilidad.id)
		else:
			print 'viejo'
			viejo = utilidad.valor_utilidad
			print viejo
			formulario = UtilidadesForm(instance=utilidad)
		return render_to_response('edit_utilidadform.html',{'formulario':formulario},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def add_gasto(request):
	
	if request.user.is_superuser:

		if request.method=='POST':	
			formulario = GastosAdminForm( request.POST)
			if formulario.is_valid():
				gasto = formulario.save(commit=False)
				print 'obtengo el valor del gasto que se agrego is_superuser'	
				print gasto.valor
				print gasto.id_cartera
				gasto.save()
				print 'obtengo la cartera que va a ser modificada'
				cartera = Cartera.objects.get(id=gasto.id_cartera.id)
				print cartera.monto
				cartera.monto = cartera.monto-gasto.valor
				cartera.save()
				print cartera.monto
				return HttpResponseRedirect('/gastos/page/1')
		else:
			formulario = GastosAdminForm(initial={'fecha_gasto':date.today()})
		return render_to_response('gastosform.html',{'formulario':formulario},context_instance=RequestContext(request))


	else:
		if request.method=='POST':	
			formulario = GastosForm( request.POST)
			if formulario.is_valid():
				gasto = formulario.save(commit=False)
				print 'obtengo el valor del gasto que se agrego cobrador---'	
				print gasto.valor
				usuario = request.user
				print 'mostramos el usuario logueado'
				print usuario
				responsable = Cartera.objects.get(responsable=usuario.id)
				print 'responsable'
				print responsable
				print 'guardar el usuario en el id_cartera'
				gasto.id_cartera = responsable
				print gasto.id_cartera
				gasto.save()
				print 'obtengo la cartera que va a ser modificada'
				cartera = Cartera.objects.get(id=gasto.id_cartera.id)
				print cartera.monto
				cartera.monto = cartera.monto-gasto.valor
				cartera.save()
				print cartera.monto
				return HttpResponseRedirect('/gastos/page/1')
					

		else:
			formulario = GastosForm(initial={'fecha_gasto':date.today()})
		return render_to_response('gastosform.html',{'formulario':formulario},context_instance=RequestContext(request))		

@login_required(login_url='/login/')
def edit_gasto(request,id_gasto):
	gasto = Gastos.objects.get(id=id_gasto)
	viejo = gasto.valor

	if request.user.is_superuser:
		if request.method == 'POST':
			formulario = GastosAdminForm(request.POST,instance=gasto)
			if formulario.is_valid():	
				formulario.save()
				cartera = Cartera.objects.get(id=gasto.id_cartera.id)
				print 'nuevo'
				print gasto.valor
				if viejo < gasto.valor:
					diferencia = gasto.valor - viejo
					print 'diferencia'
					print diferencia
					cartera.monto = cartera.monto-diferencia
				else:
					diferencia = viejo - gasto.valor
					print 'diferencia else'
					print diferencia
					cartera.monto = cartera.monto+diferencia
				cartera.save()
				return HttpResponseRedirect('/gasto/%s/'%gasto.id)
		else:
			print 'viejo'
			viejo = gasto.valor
			print viejo
			formulario = GastosAdminForm(instance=gasto)
		return render_to_response('edit_gastoform.html',{'formulario':formulario},context_instance=RequestContext(request))

	else:
		if request.method == 'POST':
			formulario = GastosForm(request.POST,instance=gasto)
			if formulario.is_valid():
				
				formulario.save()
				cartera = Cartera.objects.get(id=gasto.id_cartera.id)
				print 'nuevo'
				print gasto.valor
				if viejo < gasto.valor:
					diferencia = gasto.valor - viejo
					print 'diferencia'
					print diferencia
					cartera.monto = cartera.monto-diferencia
				else:
					diferencia = viejo - gasto.valor
					print 'diferencia else'
					print diferencia
					cartera.monto = cartera.monto+diferencia
				cartera.save()
				return HttpResponseRedirect('/gasto/%s/'%gasto.id)
		else:
			print 'viejo'
			viejo = gasto.valor
			print viejo
			formulario = GastosForm(instance=gasto)
		return render_to_response('edit_gastoform.html',{'formulario':formulario},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def add_usuario(request):

	if request.user.is_superuser:
		if request.method=='POST':
			formulario = UsuariosAdminForm(request.POST)
			if formulario.is_valid():
				formulario.save()
				return HttpResponseRedirect('/usuarios/')
		else:
			formulario = UsuariosAdminForm()
		return render_to_response('usuariosform.html',{'formulario':formulario},context_instance=RequestContext(request))
	else:
		if request.method=='POST':
			formulario = UsuariosForm(request.POST)
			if formulario.is_valid():
				usuario=formulario.save(commit=False)
				usua = request.user
				responsable = Cartera.objects.get(responsable=usua.id)
				usuario.id_cartera = responsable
				usuario.save()
				return HttpResponseRedirect('/usuarios/page/1')
		else:
			formulario = UsuariosForm()
		return render_to_response('usuariosform.html',{'formulario':formulario},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def edit_usuario(request,id_usuario):

	usuario = Usuarios.objects.get(id=id_usuario)
	
	if request.method == 'POST':
		formulario = UsuariosForm(request.POST,instance=usuario)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/usuarios/%s/'%usuario.id)
	else:
		formulario = UsuariosForm(instance=usuario)
	

	return render_to_response('edit_usuarioform.html',{'formulario':formulario},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def add_prestamo(request):
	#the_cartera = get_object_or_404(Cartera, id=id_cartera)
	if request.user.is_superuser:
		if request.method=='POST':
			formulario = PrestamosAdminForm(request.POST)
			if formulario.is_valid():
				prestamo = formulario.save(commit=False)
				prestamo.total_pagar = ((prestamo.monto_inicial * prestamo.interes)/100) + prestamo.monto_inicial
				prestamo.valor_cuota = prestamo.total_pagar / prestamo.cuotas
				prestamo.saldo_actual = prestamo.total_pagar 
				dias = timedelta(days=prestamo.cuotas)
				prestamo.fecha_vencimiento = dias + prestamo.fecha_prestamo
				prestamo.save()
		####restamos de la cartera el monto inicial######
				cartera = Cartera.objects.get(id=prestamo.id_cartera.id)
				print cartera
				cartera.monto = cartera.monto - prestamo.monto_inicial
				cartera.save()
				print cartera.monto	
				return HttpResponseRedirect('/ventas_vigentes/page/1/')
		else:
			formulario = PrestamosAdminForm(initial={'fecha_prestamo':date.today()})
		return render_to_response('prestamosform.html',{'formulario':formulario},context_instance=RequestContext(request))
	else:
		q = Cartera.objects.get(responsable=request.user.id)
		if request.method=='POST':
			formulario = PrestamosForm(request.POST )
			if formulario.is_valid():
				prestamo = formulario.save(commit=False)
				usuario = request.user
				prestamo.total_pagar = ((prestamo.monto_inicial * prestamo.interes)/100) + prestamo.monto_inicial
				prestamo.valor_cuota = prestamo.total_pagar / prestamo.cuotas
				prestamo.saldo_actual = prestamo.total_pagar 
				dias = timedelta(days=prestamo.cuotas)
				prestamo.fecha_vencimiento = dias + prestamo.fecha_prestamo
				responsable = Cartera.objects.get(responsable=usuario.id)
				prestamo.id_cartera = responsable
				print 'consulto si el cliente tiene ventas vigentes'
				prestamos_vigentes = Prestamos.objects.exclude(estado_prestamo=2).exclude(estado_prestamo=5).filter(id_usuarios=prestamo.id_usuarios_id)
				prestamos_perdidas = Prestamos.objects.filter(estado_prestamo=5).filter(id_usuarios=prestamo.id_usuarios_id)
				if prestamos_vigentes:
					return render_to_response('alerta_prestamos.html',{'formulario':formulario,'prestamo':prestamo},context_instance=RequestContext(request))
				elif prestamos_perdidas:
					return render_to_response('alerta_perdidas.html',{'formulario':formulario,'prestamo':prestamo},context_instance=RequestContext(request))
				else:
					print 'nada en perdidas'
				prestamo.save()
		####restamos de la cartera el monto inicial######
				cartera = Cartera.objects.get(id=prestamo.id_cartera.id)
				print cartera
				cartera.monto = cartera.monto - prestamo.monto_inicial
				cartera.save()
				print cartera.monto	
				return HttpResponseRedirect('/ventas_vigentes/page/1/')
		else:
			print q.id
			formulario = PrestamosForm(initial={'fecha_prestamo':date.today()})
			formulario.fields['id_usuarios'].queryset = Usuarios.objects.filter(id_cartera=q.id)
		return render_to_response('prestamosform.html',{'formulario':formulario,'q':q},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def add_prestamo_confirm(request):
	print 'ingresa a la confirmacion de la venta'
	q = Cartera.objects.get(responsable=request.user.id)
	if request.method=='POST':
		formulario = PrestamosForm(request.POST )
		if formulario.is_valid():
			prestamo = formulario.save(commit=False)
			usuario = request.user
			prestamo.total_pagar = ((prestamo.monto_inicial * prestamo.interes)/100) + prestamo.monto_inicial
			prestamo.valor_cuota = prestamo.total_pagar / prestamo.cuotas
			prestamo.saldo_actual = prestamo.total_pagar 
			dias = timedelta(days=prestamo.cuotas)
			prestamo.fecha_vencimiento = dias + prestamo.fecha_prestamo
			responsable = Cartera.objects.get(responsable=usuario.id)
			prestamo.id_cartera = responsable
			
			prestamo.save()
	####restamos de la cartera el monto inicial######
			cartera = Cartera.objects.get(id=prestamo.id_cartera.id)
			print cartera
			cartera.monto = cartera.monto - prestamo.monto_inicial
			cartera.save()
			print cartera.monto	
			return HttpResponseRedirect('/ventas_vigentes/page/1/')
	else:
		print q.id
		formulario = PrestamosForm(initial={'fecha_prestamo':date.today()})
		formulario.fields['id_usuarios'].queryset = Usuarios.objects.filter(id_cartera=q.id)
	return render_to_response('prestamosform.html',{'formulario':formulario,'q':q},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def close_prestamo_vigente(request,id_prestamo):

	prestamo = Prestamos.objects.get(id=id_prestamo)
	
	if request.method == 'POST':
		formulario = Close_PrestamosForm(request.POST,instance=prestamo)
		if formulario.is_valid():
			close = formulario.save(commit=False)
			close.save()
			print prestamo.estado_prestamo
			if prestamo.estado_prestamo_id == 5:

				cartera = Cartera.objects.get(id=prestamo.id_cartera.id)
				cartera.monto = cartera.monto - prestamo.saldo_actual
				cartera.save()
			else:
				cartera = Cartera.objects.get(id=prestamo.id_cartera.id)
				cartera.monto = cartera.monto + prestamo.saldo_actual
				cartera.save()

			return HttpResponseRedirect('/ventas_vigentes/%s/'%prestamo.id)
	else:
		formulario = Close_PrestamosForm(instance=prestamo)
		formulario.fields['estado_prestamo'].queryset = Estado_Prestamo.objects.exclude(id=2).exclude(id=3).exclude(id=4)

	return render_to_response('close_prestamoform.html',{'formulario':formulario},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def edit_prestamo(request,id_prestamo):
	prestamo = Prestamos.objects.get(id=id_prestamo)
	abonos = Recaudos.objects.filter(id_prestamo=id_prestamo)
	sum_abonos=0
	viejo = prestamo.monto_inicial
	if request.method == 'POST':
		formulario = PrestamosForm(request.POST,instance=prestamo)
		if formulario.is_valid():
			prestamo=formulario.save(commit=False)
			prestamo.total_pagar = ((prestamo.monto_inicial * prestamo.interes)/100) + prestamo.monto_inicial
			prestamo.valor_cuota = prestamo.total_pagar / prestamo.cuotas
			if abonos:
				for abono in abonos:
					sum_abonos = sum_abonos+abono.valor
			else:
				print 'no hay abonos en el prestamo'
			prestamo.saldo_actual = prestamo.total_pagar - sum_abonos 
			dias = timedelta(days=prestamo.cuotas)
			prestamo.fecha_vencimiento = dias + prestamo.fecha_prestamo
			prestamo.save()
	####restamos de la cartera el monto inicial######
			cartera = Cartera.objects.get(id=prestamo.id_cartera.id)
			print cartera
			print 'nuevo'
			if viejo < prestamo.monto_inicial:
				diferencia = prestamo.monto_inicial - viejo
				print 'diferencia'
				print diferencia
				cartera.monto = cartera.monto-diferencia
			else:
				diferencia = viejo - prestamo.monto_inicial
				print 'diferencia else'
				print diferencia
				cartera.monto = cartera.monto+diferencia
			cartera.save()
			print cartera.monto	
			return HttpResponseRedirect('/ventas_vigentes/%s/'%prestamo.id)
	else:
		viejo = prestamo.monto_inicial
		formulario = PrestamosForm(instance=prestamo)
	return render_to_response('edit_prestamoform.html',{'formulario':formulario},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def delete_prestamo(request,id_prestamo):
	prestamo = Prestamos.objects.get(id=id_prestamo)
	abonos = Recaudos.objects.filter(id_prestamo=id_prestamo)
	if abonos:
		return render_to_response('delete_prestamo.html',{'prestamo':prestamo},context_instance=RequestContext(request))
	else:
		prestamo.delete()
		print 'elimina el prestamo'
		cartera = Cartera.objects.get(id=prestamo.id_cartera.id)
		print cartera
		cartera = Cartera.objects.get(id=prestamo.id_cartera.id)
		cartera.monto = cartera.monto+prestamo.monto_inicial
		cartera.save()
		return render_to_response('delete.html',{'prestamo':prestamo},context_instance=RequestContext(request))


@login_required(login_url='/login/')
def add_recaudo(request):
	prestamo = Prestamos.objects.get(id=id_prestamo)
	if request.user.is_superuser:
		if request.method=='POST':
			formulario = RecaudosAdminForm(request.POST)
			if formulario.is_valid():
				recaudo = formulario.save(commit=False)
				print 'obtengo el valor del recaudo que se agrega'
				print recaudo.valor
				recaudo.save()
				print 'obtengo el prestamo al cual se le aplica el abono'
				prestamo = Prestamos.objects.get(id=recaudo.id_prestamo.id)
				print prestamo
				print 'muestro saldo actual del prestamo'
				print prestamo.saldo_actual
				print 'muestro el saldo actual aplicando el recaudo'
				prestamo.saldo_actual = prestamo.saldo_actual - recaudo.valor
				hoy = date.today()
				print hoy
				if prestamo.saldo_actual <= 0:
					print 'pregunta si saldo_actual es menor a 0'
					prestamo.estado_prestamo_id = 2
					print prestamo.estado_prestamo
				elif hoy > prestamo.fecha_vencimiento:
					print 'ingresa al if hoy>fecha vencimiento'
					prestamo.estado_prestamo_id = 4
					print prestamo.estado_prestamo					
				else:
					print 'else'
					prestamo.estado_prestamo_id = 1 
					print prestamo.estado_prestamo
				
				print 'finalizan las condiciones'
				print prestamo.estado_prestamo

				prestamo.save()
				cartera = Cartera.objects.get(id=recaudo.id_cartera.id)
				cartera.monto = cartera.monto + recaudo.valor
				cartera.save()
				print cartera.monto
				return HttpResponseRedirect('/liquidar_ventas/page/1')
		else:
			formulario = RecaudosAdminForm()
			formulario.fields['id_prestamo'].queryset = Prestamos.objects.exclude(estado_prestamo=2)
		return render_to_response('recaudosform.html',{'formulario':formulario},context_instance=RequestContext(request))
	else:
		q = Cartera.objects.get(responsable=request.user.id)
		if request.method=='POST':
			formulario = RecaudosForm(request.POST)
			if formulario.is_valid():
				recaudo = formulario.save(commit=False)
				print 'obtengo el valor del recaudo que se agrega'
				
				usuario = request.user
				responsable = Cartera.objects.get(responsable=usuario.id)
				recaudo.id_cartera = responsable
				print prestamo
				recaudo.id_prestamo = prestamo
				print recaudo.valor
				recaudo.save()
				print 'obtengo el prestamo al cual se le aplica el abono'
				prestamo = Prestamos.objects.get(id=recaudo.id_prestamo.id)
				print prestamo
				print 'muestro saldo actual del prestamo'
				print prestamo.saldo_actual
				print 'muestro el saldo actual aplicando el recaudo'
				prestamo.saldo_actual = prestamo.saldo_actual - recaudo.valor
				hoy = date.today()
				print hoy
				if prestamo.saldo_actual <= 0:
					print 'pregunta si saldo_actual es menor a 0'
					prestamo.estado_prestamo_id = 2
					print prestamo.estado_prestamo
				elif hoy > prestamo.fecha_vencimiento:
					print 'ingresa al if hoy>fecha vencimiento'
					prestamo.estado_prestamo_id = 4
					print prestamo.estado_prestamo					
				else:
					print 'else'
					prestamo.estado_prestamo_id = 1 
					print prestamo.estado_prestamo
				
				print 'finalizan las condiciones'
				print prestamo.estado_prestamo
				prestamo.save()
				print prestamo.saldo_actual
				cartera = Cartera.objects.get(id=recaudo.id_cartera.id)
				cartera.monto = cartera.monto + recaudo.valor
				cartera.save()
				print cartera.monto
				return HttpResponseRedirect('/liquidar_ventas/page/1')
		else:
			print q
			print prestamo
			formulario = RecaudosForm(initial={'fecha_recaudo':date.today(),'valor':prestamo.valor_cuota})
			formulario.fields['id_prestamo'].queryset = Prestamos.objects.filter(id_cartera=q.id).exclude(estado_prestamo=2).exclude(estado_prestamo=5)
		return render_to_response('recaudosform.html',{'formulario':formulario},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def add_recaudo_confirm(request,id_prestamo):
	prestamo = Prestamos.objects.get(id=id_prestamo)
	print prestamo
	if request.method=='POST':
		formulario = RecaudosForm(request.POST)
		if formulario.is_valid():
			recaudo = formulario.save(commit=False)
			print 'obtengo el valor del recaudo que se agrega'
			usuario = request.user
			responsable = Cartera.objects.get(responsable=usuario.id)
			recaudo.id_cartera = responsable
			print prestamo
			recaudo.id_prestamo = prestamo
			print recaudo.valor
			print 'imprimo la fecha de recaudo que se va a guardar'
			print recaudo.fecha_recaudo
			recaudo.save()
		#	print 'obtengo el prestamo al cual se le aplica el abono'
		#	prestamo = Prestamos.objects.get(id=recaudo.id_prestamo.id)
			print prestamo
			print 'muestro saldo actual del prestamo'
			print prestamo.saldo_actual
			print 'muestro el saldo actual aplicando el recaudo'
			prestamo.saldo_actual = prestamo.saldo_actual - recaudo.valor
			hoy = date.today()
			print hoy
			if prestamo.saldo_actual <= 0:
				print 'pregunta si saldo_actual es menor a 0'
				prestamo.estado_prestamo_id = 2
				print prestamo.estado_prestamo
			elif hoy > prestamo.fecha_vencimiento:
				print 'ingresa al if hoy>fecha vencimiento'
				prestamo.estado_prestamo_id = 4
				print prestamo.estado_prestamo					
			else:
				print 'else'
				prestamo.estado_prestamo_id = 1 
				print prestamo.estado_prestamo
			
			print 'finalizan las condiciones'
			print prestamo.estado_prestamo
			prestamo.save()
			print prestamo.saldo_actual
			cartera = Cartera.objects.get(id=recaudo.id_cartera.id)
			cartera.monto = cartera.monto + recaudo.valor
			cartera.save()
			print cartera.monto
			return HttpResponseRedirect('/liquidar_ventas/page/1')
	else:
		print q
		print prestamo
		formulario = RecaudosForm(initial={'fecha_recaudo':date.today(),'valor':prestamo.valor_cuota})
		#formulario.fields['id_prestamo'].queryset = Prestamos.objects.filter(id_cartera=q.id).exclude(estado_prestamo=2).exclude(estado_prestamo=5)
	return render_to_response('recaudosform.html',{'formulario':formulario},context_instance=RequestContext(request))

####liquidar ventas#########	
@login_required(login_url='/login/')
def add_abono(request,id_prestamo):
	prestamo = Prestamos.objects.get(id=id_prestamo)
	recaudos = Recaudos.objects.filter(id_prestamo=id_prestamo)
	print 'imprime prestamo a abonar'
	print prestamo
	print 'imprime el id del usuario de ese prestamo'
	print prestamo.id_usuarios_id
	if request.user.is_superuser:
		if request.method=='POST':
			formulario = RecaudosAdminForm(request.POST)
			if formulario.is_valid():
				recaudo = formulario.save(commit=False)
				print 'obtengo el valor del recaudo que se agrega'
				print recaudo.valor
				recaudo.id_prestamo = prestamo
				recaudo.id_cartera = prestamo.id_cartera
				recaudo.save()
				print 'obtengo el prestamo al cual se le aplica el abono'
				prestamo = Prestamos.objects.get(id=recaudo.id_prestamo.id)
				print prestamo
				print 'muestro saldo actual del prestamo'
				print prestamo.saldo_actual
				print 'muestro el saldo actual aplicando el recaudo'
				prestamo.saldo_actual = prestamo.saldo_actual - recaudo.valor
				hoy = date.today()
				print hoy
				if prestamo.saldo_actual <= 0:
					print 'pregunta si saldo_actual es menor a 0'
					prestamo.estado_prestamo_id = 2
					print prestamo.estado_prestamo
				elif hoy > prestamo.fecha_vencimiento:
					print 'ingresa al if hoy>fecha vencimiento'
					prestamo.estado_prestamo_id = 4
					print prestamo.estado_prestamo					
				else:
					print 'else'
					prestamo.estado_prestamo_id = 1 
					print prestamo.estado_prestamo
				
				print 'finalizan las condiciones'
				print prestamo.estado_prestamo

				prestamo.save()
				cartera = Cartera.objects.get(id=recaudo.id_cartera.id)
				cartera.monto = cartera.monto + recaudo.valor
				cartera.save()
				print cartera.monto
				return HttpResponseRedirect('/liquidar_ventas/page/1')
		else:
			formulario = RecaudosAdminForm(initial={'fecha_recaudo':date.today(),'valor':prestamo.valor_cuota,'id_cartera':prestamo.id_cartera})
			#formulario.fields['id_prestamo'].queryset = Prestamos.objects.exclude(estado_prestamo=2)
		return render_to_response('recaudosform.html',{'formulario':formulario},context_instance=RequestContext(request))
	else:
		q = Cartera.objects.get(responsable=request.user.id)

		if request.method=='POST':
			formulario = RecaudosForm(request.POST)
			if formulario.is_valid():
				recaudo = formulario.save(commit=False)
				print 'obtengo el valor del recaudo que se agrega'
				
				usuario = request.user
				responsable = Cartera.objects.get(responsable=usuario.id)
				recaudo.id_cartera = responsable
				print prestamo
				recaudo.id_prestamo = prestamo
				print recaudo.valor


				
				print 'consulto que no exista un recaudo para ese prestamo con la misma fecha'
				recau = Recaudos.objects.filter(id_prestamo=id_prestamo).filter(fecha_recaudo=recaudo.fecha_recaudo)
				
				if recau:
					formulario = RecaudosForm(initial={'fecha_recaudo':recaudo.fecha_recaudo,'valor':recaudo.valor})
					return render_to_response('alerta_abono.html',{'formulario':formulario,'recaudo':recaudo},context_instance=RequestContext(request))
				else:
					print 'No existen recaudos en esta fecha, puede continuar'
				print 'imprimo la fecha de recaudo que se va a guardar'
				print recaudo.fecha_recaudo
				recaudo.save()
			#	print 'obtengo el prestamo al cual se le aplica el abono'
			#	prestamo = Prestamos.objects.get(id=recaudo.id_prestamo.id)
				print prestamo
				print 'muestro saldo actual del prestamo'
				print prestamo.saldo_actual
				print 'muestro el saldo actual aplicando el recaudo'
				prestamo.saldo_actual = prestamo.saldo_actual - recaudo.valor
				hoy = date.today()
				print hoy
				if prestamo.saldo_actual <= 0:
					print 'pregunta si saldo_actual es menor a 0'
					prestamo.estado_prestamo_id = 2
					print prestamo.estado_prestamo
				elif hoy > prestamo.fecha_vencimiento:
					print 'ingresa al if hoy>fecha vencimiento'
					prestamo.estado_prestamo_id = 4
					print prestamo.estado_prestamo					
				else:
					print 'else'
					prestamo.estado_prestamo_id = 1 
					print prestamo.estado_prestamo
				
				print 'finalizan las condiciones'
				print prestamo.estado_prestamo
				prestamo.save()
				print prestamo.saldo_actual
				cartera = Cartera.objects.get(id=recaudo.id_cartera.id)
				cartera.monto = cartera.monto + recaudo.valor
				cartera.save()
				print cartera.monto
				return HttpResponseRedirect('/liquidar_ventas/page/1')
		else:
			print 'llama al formulario con los datos del abono'
			print q
			print prestamo
			##comparamos que el valor de la cuota no sea mayor al saldo actual##
			if prestamo.saldo_actual < prestamo.valor_cuota:
				formulario = RecaudosForm(initial={'fecha_recaudo':date.today(),'valor':prestamo.saldo_actual})
			else:	
				formulario = RecaudosForm(initial={'fecha_recaudo':date.today(),'valor':prestamo.valor_cuota})
			
		return render_to_response('recaudosform.html',{'formulario':formulario},context_instance=RequestContext(request))


####liquidar ventas * fecha #########	
@login_required(login_url='/login/')
def add_abono_x_fecha(request,id_prestamo,fecha):
	print 'la fecha de add_abono_x_fecha es:'
	print fecha
	prestamo = Prestamos.objects.get(id=id_prestamo)
	print 'imprime prestamo a abonar'
	print prestamo
	print 'imprime el id del usuario de ese prestamo'
	print prestamo.id_usuarios_id

	q = Cartera.objects.get(responsable=request.user.id)

	if request.method=='POST':
		formulario = RecaudosForm(request.POST)
		if formulario.is_valid():
			recaudo = formulario.save(commit=False)
			print 'obtengo el valor del recaudo que se agrega'
			
			usuario = request.user
			responsable = Cartera.objects.get(responsable=usuario.id)
			recaudo.id_cartera = responsable
			print prestamo
			recaudo.id_prestamo = prestamo
			print recaudo.valor


				
			print 'consulto que no exista un recaudo para ese prestamo con la misma fecha'
			recau = Recaudos.objects.filter(id_prestamo=id_prestamo).filter(fecha_recaudo=recaudo.fecha_recaudo)
				
			if recau:
				formulario = RecaudosForm(initial={'fecha_recaudo':recaudo.fecha_recaudo,'valor':recaudo.valor})
				return render_to_response('alerta_abono.html',{'formulario':formulario,'recaudo':recaudo},context_instance=RequestContext(request))
			else:
				print 'No existen recaudos en esta fecha, puede continuar'
			print 'imprimo la fecha de recaudo que se va a guardar'
			print recaudo.fecha_recaudo
			recaudo.save()
		
			print prestamo
			print 'muestro saldo actual del prestamo'
			print prestamo.saldo_actual
			print 'muestro el saldo actual aplicando el recaudo'
			prestamo.saldo_actual = prestamo.saldo_actual - recaudo.valor
			hoy = date.today()
			print hoy
			if prestamo.saldo_actual <= 0:
				print 'pregunta si saldo_actual es menor a 0'
				prestamo.estado_prestamo_id = 2
				print prestamo.estado_prestamo
			elif hoy > prestamo.fecha_vencimiento:
				print 'ingresa al if hoy>fecha vencimiento'
				prestamo.estado_prestamo_id = 4
				print prestamo.estado_prestamo					
			else:
				print 'else'
				prestamo.estado_prestamo_id = 1 
				print prestamo.estado_prestamo
			
			print 'finalizan las condiciones'
			print prestamo.estado_prestamo
			prestamo.save()
			print prestamo.saldo_actual
			cartera = Cartera.objects.get(id=recaudo.id_cartera.id)
			cartera.monto = cartera.monto + recaudo.valor
			cartera.save()
			print cartera.monto
		return HttpResponseRedirect('/fecha_liq_ventas_fecha/%s/' %fecha)
	else:
		print 'llama al formulario con los datos del abono'
		print q
		print prestamo
		##comparamos que el valor de la cuota no sea mayor al saldo actual##
		if prestamo.saldo_actual < prestamo.valor_cuota:
			formulario = RecaudosForm(initial={'fecha_recaudo':fecha,'valor':prestamo.saldo_actual})
		else:	
			formulario = RecaudosForm(initial={'fecha_recaudo':fecha,'valor':prestamo.valor_cuota})
			
	return render_to_response('recaudosform.html',{'formulario':formulario},context_instance=RequestContext(request))




@login_required(login_url='/login/')
def edit_recaudo(request,id_recaudo):
	recaudo = Recaudos.objects.get(id=id_recaudo)
	viejo = recaudo.valor
	if request.user.is_superuser:
		if request.method=='POST':
			formulario = RecaudosAdminForm(request.POST,instance=recaudo)
			if formulario.is_valid():
				recaudo = formulario.save(commit=False)
				print 'obtengo el valor del recaudo que se agrega'
				print recaudo.valor
				recaudo.save()
				print 'obtengo el prestamo al cual se le aplica el abono'
				prestamo = Prestamos.objects.get(id=recaudo.id_prestamo.id)
				cartera = Cartera.objects.get(id=recaudo.id_cartera.id)
				print prestamo
				print 'muestro saldo actual del prestamo'
				print prestamo.saldo_actual
				print 'muestro el saldo actual aplicando el recaudo'
				print 'ingreso a la condicion de editar valores IF'
				if viejo < recaudo.valor:
					diferencia = recaudo.valor - viejo
					print 'diferencia'
					print diferencia
					prestamo.saldo_actual = prestamo.saldo_actual - diferencia	
					cartera.monto = cartera.monto+diferencia
				else:
					diferencia = viejo - recaudo.valor
					print 'diferencia else'
					print diferencia
					prestamo.saldo_actual = prestamo.saldo_actual + diferencia
					cartera.monto = cartera.monto-diferencia
				cartera.save()

				print 'ingreso a las condiciones para modificar los estados del prestamo'	
				
				hoy = date.today()
				print hoy
				if prestamo.saldo_actual <= 0:
					print 'pregunta si saldo_actual es menor a 0'
					prestamo.estado_prestamo_id = 2
					print prestamo.estado_prestamo
				elif hoy > prestamo.fecha_vencimiento:
					print 'ingresa al if hoy>fecha vencimiento'
					prestamo.estado_prestamo_id = 4
					print prestamo.estado_prestamo					
				else:
					print 'else'
					prestamo.estado_prestamo_id = 1 
					print prestamo.estado_prestamo
				
				print 'finalizan las condiciones'
				print prestamo.estado_prestamo

				prestamo.save()
				
				print 'se guarda el prestamo y se muestra el monto de la cartera'
				
				print cartera.monto
				return HttpResponseRedirect('/recaudos/page/1')
		else:
			viejo = recaudo.valor
			formulario = RecaudosAdminForm(instance=recaudo)
			#formulario.fields['id_prestamo'].queryset = Prestamos.objects.exclude(estado_prestamo=2)
		return render_to_response('recaudosform.html',{'formulario':formulario},context_instance=RequestContext(request))
	else:
		q = Cartera.objects.get(responsable=request.user.id)
		if request.method=='POST':
			formulario = RecaudosForm(request.POST,instance=recaudo)
			if formulario.is_valid():
				recaudo = formulario.save(commit=False)
				print 'obtengo el valor del recaudo que se agrega'
				print recaudo.valor
				usuario = request.user
				responsable = Cartera.objects.get(responsable=usuario.id)
				recaudo.id_cartera = responsable
				recaudo.save()
				print 'obtengo el prestamo al cual se le aplica el abono'
				prestamo = Prestamos.objects.get(id=recaudo.id_prestamo.id)
				cartera = Cartera.objects.get(id=recaudo.id_cartera.id)
				print prestamo
				print 'muestro saldo actual del prestamo'
				print prestamo.saldo_actual
				print 'muestro el saldo actual aplicando el recaudo'
				if viejo < recaudo.valor:
					diferencia = recaudo.valor - viejo
					print 'diferencia'
					print diferencia
					prestamo.saldo_actual = prestamo.saldo_actual - diferencia	
					cartera.monto = cartera.monto+diferencia
				else:
					diferencia = viejo - recaudo.valor
					print 'diferencia else'
					print diferencia
					prestamo.saldo_actual = prestamo.saldo_actual + diferencia
					cartera.monto = cartera.monto-diferencia
				cartera.save()
				print 'ingreso a las condiciones para modificar los estados del prestamo'	
				hoy = date.today()
				print hoy
				if prestamo.saldo_actual <= 0:
					print 'pregunta si saldo_actual es menor a 0'
					prestamo.estado_prestamo_id = 2
					print prestamo.estado_prestamo
				elif hoy > prestamo.fecha_vencimiento:
					print 'ingresa al if hoy>fecha vencimiento'
					prestamo.estado_prestamo_id = 4
					print prestamo.estado_prestamo					
				else:
					print 'else'
					prestamo.estado_prestamo_id = 1 
					print prestamo.estado_prestamo
				
				print 'finalizan las condiciones'
				print prestamo.estado_prestamo
				prestamo.save()
				print prestamo.saldo_actual
				
				
				print cartera.monto
				return HttpResponseRedirect('/recaudos/page/1')
		else:
			print q
			formulario = RecaudosForm(instance=recaudo)
			#formulario.fields['id_prestamo'].queryset = Prestamos.objects.filter(id_cartera=q.id).exclude(estado_prestamo=2)
		return render_to_response('recaudosform.html',{'formulario':formulario},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def fecha_admin(request,id_cartera):
	if request.method == "POST":
		formulario = fechaForm(request.POST)
		if formulario.is_valid():
			fecha = request.POST['fecha']
			print 'la fecha seleccionada es:'
			print fecha
			total = 0
			print total
			print 'inegresa al filtro'
			cartera = Cartera.objects.filter(id=id_cartera)
			filtro = Recaudos.objects.filter(id_cartera=cartera).filter(fecha_recaudo=fecha) 
			
			print filtro
			for x in filtro:
				total = total + x.valor
			return render_to_response('informe_recaudos_fecha.html',{'filtro':filtro,'total':total,'id_cartera':id_cartera},context_instance=RequestContext(request))
	else:
		formulario = fechaForm(initial={'fecha':date.today()})
		return render_to_response('auditar_abonos_fecha.html',{'formulario':formulario},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def fecha(request):
	if request.method == "POST":
		formulario = fechaForm(request.POST)
		if formulario.is_valid():
			fecha = request.POST['fecha']
			print 'la fecha seleccionada es:'
			print fecha
			total = 0
			print total
			print 'inegresa al filtro'
			cartera = Cartera.objects.filter(responsable_id=request.user.id)
			filtro = Recaudos.objects.filter(id_cartera=cartera).filter(fecha_recaudo=fecha) 
			
			print filtro
			for x in filtro:
				total = total + x.valor
			return render_to_response('informe_recaudos_fecha.html',{'filtro':filtro,'total':total},context_instance=RequestContext(request))
	else:
		formulario = fechaForm(initial={'fecha':date.today()})
		return render_to_response('auditar_abonos_fecha.html',{'formulario':formulario},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def fecha_liq_ventas(request):
	if request.method == "POST":
		formulario = fechaForm(request.POST)
		if formulario.is_valid():
			fecha = request.POST['fecha']
			print 'la fecha seleccionada es:'
			print fecha
			print 'ingresa al filtro'
			cartera = Cartera.objects.filter(responsable_id=request.user.id)
			print 'muestra el almacen'
			print cartera
			filtro = Recaudos.objects.filter(id_cartera=cartera).filter(fecha_recaudo=fecha) 
			print 'muestra los recaudos de esa fecha'
			print filtro
			if filtro:
				print 'ingresa al if de filtro'	
				prestamos = Prestamos.objects.filter(id_cartera=cartera).exclude(estado_prestamo=2).exclude(estado_prestamo=5).exclude(recaudos__in=filtro)
				print 'muestra los prestamos activos filtrados con los abonos del if'

				print prestamos

			else:		
				print 'ingresa al else'	
				prestamos = Prestamos.objects.filter(id_cartera=cartera).exclude(estado_prestamo=2).exclude(estado_prestamo=5)
				print 'muestra los prestamos activos filtrados con los abonos del else'
				print prestamos
			
			paginator = Paginator(prestamos,50)
			try:
				page = int(pagina)

			except:
				page = 1
			try:
				list_prestamos = paginator.page(page)
			except (EmptyPage, InvalidPage):
				list_prestamos = paginator.page(paginator.num_pages)
		
			
			return render_to_response('fecha_liq_ventas.html',{'prestamos':list_prestamos,'fecha':fecha},context_instance=RequestContext(request))
	else:
		print date.today()
		formulario = fechaForm(initial={'fecha':date.today()})
		return render_to_response('auditar_abonos_fecha.html',{'formulario':formulario},context_instance=RequestContext(request))


@login_required(login_url='/login/')
def fecha_liq_ventas_fecha(request,fecha):
	
	
	print 'la fecha seleccionada esssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss:'
	print fecha
	print 'ingresa al filtro'
	cartera = Cartera.objects.filter(responsable_id=request.user.id)
	print 'muestra el almacen'
	print cartera
	filtro = Recaudos.objects.filter(id_cartera=cartera).filter(fecha_recaudo=fecha) 
	print 'muestra los recaudos de esa fecha'
	print filtro
	if filtro:
		print 'ingresa al if de filtro'	
		prestamos = Prestamos.objects.filter(id_cartera=cartera).exclude(estado_prestamo=2).exclude(estado_prestamo=5).exclude(recaudos__in=filtro)
		print 'muestra los prestamos activos filtrados con los abonos del if'
		print prestamos

	else:		
		print 'ingresa al else'	
		prestamos = Prestamos.objects.filter(id_cartera=cartera).exclude(estado_prestamo=2).exclude(estado_prestamo=5)
		print 'muestra los prestamos activos filtrados con los abonos del else'
		print prestamos
			
		
			
	return render_to_response('fecha_liq_ventas.html',{'prestamos':prestamos,'fecha':fecha},context_instance=RequestContext(request))
	



@login_required(login_url='/login/')
def liquidar_cartera_admin(request,id_cartera):
	if request.user.is_superuser:
		if request.method == "POST":
			formulario = fechaForm(request.POST)
			if formulario.is_valid():
				fecha = request.POST['fecha']
				print 'la fecha seleccionada es:'
				print fecha
				print 'inegresa al filtro'
				cartera = Cartera.objects.get(id=id_cartera)
				print cartera
				dia = Dia.objects.get(id_cartera=cartera,fecha=fecha)
				print 'el registro del dia es:'
				print dia.fecha
				print dia.valor
				caja_anterior=dia.valor

				#calculamos los ingresos por base al almacen
				total_base = 0
				bases = Base.objects.filter(id_cartera=cartera).filter(fecha_entrega=fecha)
				for base in bases:
					total_base = total_base + base.valor 
				sum_bases=caja_anterior+total_base
				total_ingresos = 0
				ingresos = Recaudos.objects.filter(id_cartera=cartera).filter(fecha_recaudo=fecha) 
				for ingreso in ingresos:
					total_ingresos = total_ingresos + ingreso.valor
				sum_monto_cobro = total_ingresos + sum_bases
				#calculamos los egresos de los prestamos
				total_prestamos=0
				total_cobrar_dia=0
				prestamos_vigentes = Prestamos.objects.filter(id_cartera=cartera).exclude(estado_prestamo=2).exclude(estado_prestamo=5)
				print 'consulta prestamos vigentes'
				cobros = Cobro.objects.filter(id_cartera=cartera).filter(fecha=fecha)
				prestamos = Prestamos.objects.filter(id_cartera=cartera).exclude(estado_prestamo=2).exclude(estado_prestamo=5)
				sum_prestamos = 0
				for prestamo in prestamos:
					sum_prestamos = sum_prestamos + prestamo.saldo_actual
		
				if cobros:
					print 'ingresa al if del cobro'
					print cobros
					for cobro in cobros:
						print 'cobro viejo'
						print cobro.valor
						print 'nuevo cobro'
						cobro.valor = sum_prestamos
						print cobro.valor
						print 'pre save'
						#cobro.save()
						print 'se guardo el cobro'			
				else:
					print 'ingresa al else del cobro'
					cobro = Cobro(fecha=fecha,valor=sum_prestamos,id_cartera=cartera)
					#cobro.save()
					print 'guarda el cobro'				
				print prestamos_vigentes
				for prestamo_vigente in prestamos_vigentes:
					total_cobrar_dia = total_cobrar_dia + prestamo_vigente.valor_cuota
				print 'total_cobrar_dia'
				print total_cobrar_dia
				prestamos = Prestamos.objects.filter(id_cartera=cartera).filter(fecha_prestamo=fecha)
				for prestamo in prestamos:
					total_prestamos = total_prestamos + prestamo.monto_inicial
				rest_prestamos = sum_monto_cobro - total_prestamos
				total_gastos=0
				gastos = Gastos.objects.filter(id_cartera=cartera).filter(fecha_gasto=fecha)
				for gasto in gastos:
					total_gastos = total_gastos+gasto.valor
				rest_gastos = rest_prestamos - total_gastos
				total_utilidades=0
				utilidades = Utilidades.objects.filter(id_cartera=cartera).filter(fecha_entrega=fecha)
				for utilidad in utilidades:
					total_utilidades = total_utilidades+utilidad.valor_utilidad
				rest_utilidades = rest_gastos-total_utilidades
				total_cobro=0
				cobros = Cobro.objects.filter(id_cartera=cartera).filter(fecha=fecha)
				for cobro in cobros:
					total_cobro = total_cobro + cobro.valor
				print 'cobrosssssssssssssssssssssssssssssssssssss'
				print cobro
				return render_to_response('liquidacion_cobrador.html',{'sum_bases':sum_bases,'total_base':total_base,'sum_prestamos':sum_prestamos,'total_cobro':total_cobro,'cartera':cartera,'fecha':fecha,'caja_anterior':caja_anterior,'total_ingresos':total_ingresos,'sum_monto_cobro':sum_monto_cobro,'total_prestamos':total_prestamos,'rest_prestamos':rest_prestamos,'total_gastos':total_gastos,'rest_gastos':rest_gastos,'total_cobrar_dia':total_cobrar_dia,'id_cartera':id_cartera,'total_utilidades':total_utilidades,'rest_utilidades':rest_utilidades},context_instance=RequestContext(request))
		else:
			formulario = fechaForm(initial={'fecha':date.today()})
			return render_to_response('auditar_abonos_fecha.html',{'formulario':formulario},context_instance=RequestContext(request))

@login_required(login_url='/login/')
def liquidar_cartera(request):
	if request.method == "POST":
		formulario = fechaForm(request.POST)
		if formulario.is_valid():
			fecha = request.POST['fecha']
			print 'la fecha seleccionada es:'
			print fecha
			print 'inegresa al filtro'
			cartera = Cartera.objects.get(responsable=request.user.id)
			print cartera.responsable
			dia = Dia.objects.get(id_cartera=cartera,fecha=fecha)
			print 'el registro del dia es:'
			print dia.fecha
			print dia.valor
			caja_anterior=dia.valor
			#calculamos los ingresos por base al almacen
			total_base = 0
			bases = Base.objects.filter(id_cartera=cartera).filter(fecha_entrega=fecha)
			for base in bases:
				total_base = total_base + base.valor 
			sum_bases=caja_anterior+total_base
			#calculamos los ingresos diarios
			total_ingresos = 0
			ingresos = Recaudos.objects.filter(id_cartera=cartera).filter(fecha_recaudo=fecha) 
			for ingreso in ingresos:
				total_ingresos = total_ingresos + ingreso.valor
			sum_monto_cobro = total_ingresos + sum_bases
			#calculamos los egresos de los prestamos
			total_prestamos=0
			total_cobrar_dia=0
			prestamos_vigentes = Prestamos.objects.filter(id_cartera=cartera).exclude(estado_prestamo=2).exclude(estado_prestamo=5)
			print 'consulta prestamos vigentes'
			cobros = Cobro.objects.filter(id_cartera=cartera).filter(fecha=fecha)
			prestamos = Prestamos.objects.filter(id_cartera=cartera).exclude(estado_prestamo=2).exclude(estado_prestamo=5)
			sum_prestamos = 0
			for prestamo in prestamos:
				sum_prestamos = sum_prestamos + prestamo.saldo_actual
		
			if cobros:
				print 'ingresa al if del cobro'
				print cobros
				for cobro in cobros:
					print 'cobro viejo'
					print cobro.valor
					print 'nuevo cobro'
					cobro.valor = sum_prestamos
					print cobro.valor
					print 'pre save'
					#cobro.save()
					print 'se guardo el cobro'			
			else:
				print 'ingresa al else del cobro'
				cobro = Cobro(fecha=fecha,valor=sum_prestamos,id_cartera=cartera)
				#cobro.save()
				print 'guarda el cobro'

			print prestamos_vigentes
			for prestamo_vigente in prestamos_vigentes:
				total_cobrar_dia = total_cobrar_dia + prestamo_vigente.valor_cuota
			print 'total_cobrar_dia'
			print total_cobrar_dia
			prestamos = Prestamos.objects.filter(id_cartera=cartera).filter(fecha_prestamo=fecha)
			for prestamo in prestamos:
				total_prestamos = total_prestamos + prestamo.monto_inicial
			rest_prestamos = sum_monto_cobro - total_prestamos
			total_gastos=0
			gastos = Gastos.objects.filter(id_cartera=cartera).filter(fecha_gasto=fecha)
			for gasto in gastos:
				total_gastos = total_gastos+gasto.valor
			rest_gastos = rest_prestamos - total_gastos
			total_utilidades=0
			utilidades = Utilidades.objects.filter(id_cartera=cartera).filter(fecha_entrega=fecha)
			for utilidad in utilidades:
				total_utilidades = total_utilidades+utilidad.valor_utilidad
			rest_utilidades = rest_gastos-total_utilidades

			total_cobro=0
			cobros = Cobro.objects.filter(id_cartera=cartera).filter(fecha=fecha)
			for cobro in cobros:
				total_cobro = total_cobro + cobro.valor
			print 'cobrosssssssssssssssssssssssssssssssssssss'
			print cobro
			return render_to_response('liquidacion_cobrador.html',{'sum_bases':sum_bases,'total_base':total_base,'sum_prestamos':sum_prestamos,'rest_utilidades':rest_utilidades,'total_utilidades':total_utilidades,'total_cobro':total_cobro,'cartera':cartera,'fecha':fecha,'caja_anterior':caja_anterior,'total_ingresos':total_ingresos,'sum_monto_cobro':sum_monto_cobro,'total_prestamos':total_prestamos,'rest_prestamos':rest_prestamos,'total_gastos':total_gastos,'rest_gastos':rest_gastos,'total_cobrar_dia':total_cobrar_dia},context_instance=RequestContext(request))
	else:
		formulario = fechaForm(initial={'fecha':date.today()})
		return render_to_response('auditar_abonos_fecha.html',{'formulario':formulario},context_instance=RequestContext(request))

def login_view(request):
	mensaje = ""
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username = username, password = password)
			if user is not None:
				if user.is_active:
					login(request,user)
					return HttpResponseRedirect('/bienvenido')
				else:
					mensaje = 'El usuario no se encuentra activo en el sistema'
			else:
				mensaje = "Usuario y/o Password incorrecto"
		else:
			mensaje = "Usuario y/o Password incorrecto"
	else:
		form = LoginForm()
	ctx = {'form':form,'mensaje':mensaje}
	return render_to_response('login.html',ctx,context_instance=RequestContext(request))

def logout_view(request):
	logout(request)
	return 	HttpResponseRedirect('/login')
