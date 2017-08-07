# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.template import RequestContext
from django.contrib.admin import widgets
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from datetime import datetime,timedelta
from django.db.models import Count,Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.core.signals import request_finished


class Cartera(models.Model):
	responsable = models.ForeignKey(User,max_length=50,verbose_name='Responsable')
	celular = models.CharField(max_length=20,null=True,blank=True)
	direccion = models.CharField(max_length=50,null=True,blank=True)
	monto = models.DecimalField(max_digits=10,decimal_places=2,default=0)
	ciudad = models.CharField(max_length=20)	
 
	def __unicode__(self):
		mostrar="%s - %s  "%(self.id,self.responsable)
		return mostrar

class Dia(models.Model):
	fecha = models.DateField(auto_now=False)
	valor = models.DecimalField(max_digits=10,decimal_places=2)
	id_cartera = models.ForeignKey(Cartera)

	def __unicode__(self):
		mostrar="%s - %s  "%(self.fecha,self.valor)
		return mostrar


	
class Cobro(models.Model):
	fecha = models.DateField(auto_now=False)
	valor = models.DecimalField(max_digits=10,decimal_places=2)
	id_cartera = models.ForeignKey(Cartera)
		
		

class Base(models.Model):
	fecha_entrega = models.DateField(auto_now=False)
	valor = models.DecimalField( verbose_name='Valor',max_digits=10,decimal_places=2)
	observaciones = models.CharField(verbose_name='Observaciones',max_length=100)
	id_cartera = models.ForeignKey(Cartera, verbose_name='Almacen')

	def __unicode__(self):
		mostrar="%s "%(self.id_cartera)
		return mostrar

class Tipo_Gasto(models.Model):
	nombre = models.CharField(max_length=30)
	descripcion = models.CharField(max_length=50)

	def __unicode__(self):
		mostrar="%s "%(self.nombre)
		return mostrar	

class Gastos(models.Model):
	fecha_gasto = models.DateField(auto_now=False,verbose_name='Fecha del Gasto')
	tipo_gasto = models.ForeignKey(Tipo_Gasto)
	valor = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='Valor')
	observaciones = models.CharField(max_length=100,verbose_name='Observaciones')
	id_cartera = models.ForeignKey(Cartera,verbose_name='Almacen')

	def __unicode__(self):
		mostrar="%s - %s  "%(self.fecha_gasto,self.valor)
		return mostrar


class Utilidades(models.Model):
	fecha_entrega = models.DateField(auto_now=False,verbose_name='Fecha de Entrega')
	valor_utilidad = models.DecimalField(verbose_name='Valor de la Utilidad',max_digits=10,decimal_places=2)
	descripcion = models.CharField(verbose_name='Descripción',max_length=100)
	id_cartera = models.ForeignKey(Cartera,verbose_name='Almacen')

	def __unicode__(self):
		mostrar="%s - %s  "%(self.fecha_entrega,self.valor_utilidad)
		return mostrar


BOOL_CHOICES = ((True, 'Activo'),(False, 'Inactivo'))
class Usuarios(models.Model):
	documento = models.IntegerField(unique=True,verbose_name='Documento')
	nombres = models.CharField(max_length=30,verbose_name='Nombres')
	apellidos = models.CharField(max_length=30,verbose_name='Apellidos')
	telefono = models.CharField(max_length=20,null=True,blank=True)
	celular = models.CharField(max_length=20,null=True,blank=True)
	direccion = models.CharField(max_length=50,null=True,blank=True)
	ingreso_mensual = models.DecimalField(verbose_name='Ingresos Mensuales',max_digits=10,decimal_places=2,null=True,blank=True)
	id_cartera = models.ForeignKey(Cartera,verbose_name='Almacen')
	estado = models.BooleanField(default=True,choices=BOOL_CHOICES,verbose_name='Estado')
 

	def __unicode__(self):
		mostrar="%s - %s - %s "%(self.documento,self.nombres,self.apellidos)
		return mostrar

class Plazos(models.Model):
	nombre = models.CharField(max_length=20)

	def __unicode__(self):
		mostrar="%s"%(self.nombre)
		return mostrar
		
class Estado_Prestamo(models.Model):
	nombre = models.CharField(max_length=50)
	descripcion = models.CharField(max_length=50)

	def __unicode__(self):
		mostrar="%s"%(self.nombre)
		return mostrar

class Prestamos(models.Model):
	fecha_prestamo = models.DateField(auto_now=False,verbose_name='Fecha de Venta')
	monto_inicial = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='Monto Inicial')
	interes = models.IntegerField(default=20)
	cuotas = models.IntegerField(default=24)
	plazos = models.ForeignKey(Plazos,default='1')
	valor_cuota = models.DecimalField(verbose_name='Valor Cuota',max_digits=10,decimal_places=2)
	total_pagar = models.DecimalField(verbose_name='Total a Pagar',max_digits=10,decimal_places=2,blank=True,null=True)
	fecha_vencimiento = models.DateField(verbose_name='Fecha de Vencimiento')
	saldo_actual = models.DecimalField(max_digits=10,decimal_places=2)
	observaciones = models.CharField(max_length=100,null=True,blank=True)
	estado_prestamo = models.ForeignKey(Estado_Prestamo,default='1',verbose_name='Estado Venta')
	id_cartera = models.ForeignKey(Cartera,verbose_name='Almacen')
	id_usuarios = models.ForeignKey(Usuarios,verbose_name='Cliente')

	def __unicode__(self):
		mostrar="%s - %s"%(self.id,self.id_usuarios)
		return mostrar

	def dias_restantes(self):
		cuota=self.saldo_actual/self.valor_cuota
		return cuota
	
	def dias_pagos(self):
		dias_pagos = (self.total_pagar-self.saldo_actual)/self.valor_cuota
		return dias_pagos

	def total_pago(self):
		total_pago = (self.total_pagar-self.saldo_actual)
		return total_pago

class Recaudos(models.Model):
	fecha_recaudo = models.DateField(auto_now=False)
	valor = models.DecimalField(verbose_name='Valor del Abono',max_digits=10,decimal_places=2)
	id_cartera = models.ForeignKey(Cartera,verbose_name='Almacen')
	id_prestamo = models.ForeignKey(Prestamos,verbose_name='Abonar a Venta')

	def __unicode__(self):
		mostrar="%s - %s - %s "%(self.id_prestamo_id,self.fecha_recaudo, self.valor)
		return mostrar








