from django import forms
from django.forms import ModelForm, Textarea
from models import Cartera, Base, Gastos, Usuarios, Prestamos, Recaudos,Utilidades
from django.contrib.admin import widgets
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.template import RequestContext
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from models import User


class CarteraForm(forms.ModelForm):
	class Meta:
		model = Cartera
		fields = ('responsable','celular','direccion','ciudad')

class BaseAdminForm(forms.ModelForm):
	class Meta:
		model = Base
		fields = '__all__'
		widgets = {
 			'fecha_entrega':forms.DateInput(attrs={'id':'datepicker'})
  			}

class BaseForm(forms.ModelForm):
	class Meta:
		model = Base
		exclude = ('id_cartera',)


class UtilidadesAdminForm(forms.ModelForm):


	class Meta:

		model = Utilidades
		fields = '__all__'
		widgets = {
 			'fecha_entrega':forms.DateInput(attrs={'id':'datepicker'})
  			}
class UtilidadesForm(forms.ModelForm):
	class Meta:

		model = Utilidades
		exclude = ('id_cartera',)
		widgets = {
 			'fecha_entrega':forms.DateInput(attrs={'id':'datepicker'})
  			}




class GastosAdminForm(forms.ModelForm):


	class Meta:

		model = Gastos
		fields = ('fecha_gasto','tipo_gasto','fecha_gasto','valor','observaciones','id_cartera')
		widgets = {
 			'fecha_gasto':forms.DateInput(attrs={'id':'datepicker'})
  			}
class GastosForm(forms.ModelForm):
	class Meta:

		model = Gastos
		exclude = ('id_cartera',)
		widgets = {
 			'fecha_gasto':forms.DateInput(attrs={'id':'datepicker'})
  			}

class UsuariosAdminForm(forms.ModelForm):
	class Meta:
		model = Usuarios
		fields = '__all__'

class UsuariosForm(forms.ModelForm):
	class Meta:
		model = Usuarios
		exclude = ('id_cartera',)

class PrestamosAdminForm(forms.ModelForm):
	class Meta:
		model = Prestamos
		fields = ('fecha_prestamo','monto_inicial','interes', 'cuotas','plazos',
	'observaciones','estado_prestamo','id_cartera','id_usuarios')
		widgets = {
 			'fecha_prestamo':forms.DateInput(attrs={'id':'datepicker'})
  			}

class PrestamosForm(forms.ModelForm):
		
	class Meta:
		model = Prestamos
		exclude = ('id_cartera','valor_cuota','total_pagar','fecha_vencimiento','saldo_actual')
		widgets = {
 			'fecha_prestamo':forms.DateInput(attrs={'id':'datepicker'})
  			}	

class Close_PrestamosForm(forms.ModelForm):
	class Meta:
		model = Prestamos
		fields = ('observaciones','estado_prestamo')


class RecaudosAdminForm(forms.ModelForm):
	class Meta:
		model = Recaudos
		exclude = ('id_cartera','id_prestamo')
		widgets = {
 			'fecha_recaudo':forms.DateInput(attrs={'id':'datepicker'})
  			}
  			
class RecaudosForm(forms.ModelForm):
	class Meta:
		model = Recaudos
		exclude = ('id_cartera','id_prestamo')
		widgets = {
 			'fecha_recaudo':forms.DateInput(attrs={'id':'datepicker'})
  			}

class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput())
	password = forms.CharField(widget=forms.PasswordInput(render_value=False))


class fechaForm(forms.Form):
	fecha = forms.CharField(widget=forms.DateInput(format="%Y/%m/%d",attrs={'id':'datepicker'}))
	