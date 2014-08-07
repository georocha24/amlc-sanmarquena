#encoding:utf-8
from django.db import models
from datetime import datetime

# Create your models here.

class PEPSNAC(models.Model):
	"""docstring for pepsnac"""
	PEPSNAC_ID = models.CharField(max_length=20, help_text='Numero de Identidad', primary_key=True, verbose_name=u'Identidad')
	NombreCompleto = models.TextField(help_text='Nombre completo', verbose_name=u'Nombre')
	DescripcionPolitica = models.TextField(help_text='Descripcion Politica', verbose_name=u'Descripcion')

	def __unicode__(self):
		return self.nombrecompleto

class PEPSEXT(models.Model):
	"""docstring for pepsext"""
	PEPSEXT_ID = models.CharField(max_length=20, primary_key=True, help_text='Numero de Identidad')
	NombreCompleto = models.TextField(help_text='Nombre completo', verbose_name=u'Nombre')

	def __unicode__(self):
		return self.nombrecompleto

class Nacionalidades(models.Model):
	"""docstring for Nacionalidades"""
	Nacionalidad = models.CharField(max_length=50, help_text='Nacionalidad', verbose_name=u'Nacionalidad')

	def __unicode__(self):
		return self.Nacionalidad
		
class UIFRequerimientos(models.Model):
	UIF_FechaRequerimiento = models.DateField(auto_now_add=True, help_text='Fecha del Requerimiento', verbose_name=u'Fecha')
	UIF_PrimerNombre = models.CharField(max_length=100, help_text='Primer Nombre', verbose_name=u'Nombre1')	
	UIF_SegundoNombre = models.CharField(max_length=50, help_text='Segundo Nombre', verbose_name=u'Nombre2', null=True)
	UIF_PrimerApellido = models.CharField(max_length=50, help_text='Primer Apellido', verbose_name=u'Apellido1', null=True)
	UIF_SegundoApellido = models.CharField(max_length=50, help_text='Segundo Apellido', verbose_name=u'Apellido2', null=True)
	UIF_Identidad = models.CharField(max_length= 20, help_text='Numero de identidad', verbose_name=u'Identidad', null=True)
	UIF_NumRequerimiento = models.CharField(max_length=50, help_text='Numero de requerimiento', verbose_name=u'Requerimiento')
	UIF_Nac = models.CharField(max_length=50, help_text='Nacionalidades', verbose_name=u'Nacionalidad', null=True)

	def __unicode__(self):
		return (self.UIF_PrimerNombre).decode("utf-8")

class PorcentajeRiesgos(models.Model):
	Porcentajes = models.DecimalField(max_digits = 10, decimal_places=0)

	def __unicode__(self):
		return unicode(self.Porcentajes)

class RiesgosZonasGeo(models.Model):
	"""docstring for Riesgos_ZonasGeo"""
	RiesgoZonaGeo = models.CharField(max_length=50, help_text='Zona Geografica', verbose_name=u'Zona')
	RiesgosIdPorc = models.ForeignKey(PorcentajeRiesgos)

	def __unicode__(self):
		return self.RiesgoZonaGeo

class RiesgosPaises(models.Model):
	"""docstring for Riesgos_Paises"""
	RiesgoPais = models.CharField(max_length=50, help_text='Paises con riesgo', verbose_name=u'Pais')
	RiesgosIdPorc = models.ForeignKey(PorcentajeRiesgos)

	def __unicode__(self):
		return self.RiesgoPais

class TipoServicio(models.Model):
	TiposServicio = models.CharField(max_length=50, help_text='Tipos de servicio', verbose_name=u'Servicios')
	RiesgosIdPorc = models.ForeignKey(PorcentajeRiesgos)

	def __unicode__(self):
		return self.TiposServicio

class UbicacionesFiliales(models.Model):
	Ubicaciones = models.CharField(max_length=50, help_text='Ciudad en que se ubica', verbose_name=u'Ubicaciones')

	def __unicode__(self):
		return self.Ubicaciones
		
class CanalesDistribucion(models.Model):
	NombreOficina = models.CharField(max_length=50, help_text='Canales de Distribucion', verbose_name=u'Oficina')
	RiesgosIdPorc = models.ForeignKey(PorcentajeRiesgos)
	UbicacionID = models.ForeignKey(UbicacionesFiliales)

	def __unicode__(self):
		return self.NombreOficina
		
class Afiliado(models.Model):
	NumIdentidad = models.CharField(primary_key=True, max_length=20, help_text='Numero de Identidad', verbose_name=u'Identidad')
	PrimerNombre = models.CharField(max_length=50, help_text='Primer Nombre', verbose_name=u'PrimerNombre')
	SegundoNombre = models.CharField(max_length=50, help_text='Segundo Nombre', verbose_name=u'SegundoNombre')
	PrimerApellido = models.CharField(max_length=50, help_text='Primer Apellido', verbose_name=u'PrimerApellido')
	SegundoApellido = models.CharField(max_length=50, help_text='Segundo Apellido', verbose_name=u'SegundoApellido')
	Nacionalidad = models.CharField(max_length=50, help_text='Nacionalidad', verbose_name=u'Nacionalidad')
	FechaNac = models.DateField(help_text='Fecha de nacimiento', verbose_name=u'FechaNacimiento')
	ActividadEconomica = models.CharField(max_length=50, help_text='Actividad Economica', verbose_name=u'ActividadEconomica')

	def __unicode__(self):
		return self.NumIdentidad

class ActividadEconomica(models.Model):
	ActividadEcon = models.CharField(max_length=50, help_text='Actividades Economicas', verbose_name=u'Actividad')
	RiesgosIdPorc = models.ForeignKey(PorcentajeRiesgos)

	def __unicode__(self):
		return self.ActividadEcon

class Censo(models.Model):
	CensoNumIdentidad = models.CharField(max_length=50, help_text='Numero de Identidad', verbose_name=u'Identidad', primary_key=True)
	CensoPrimerNombre = models.CharField(max_length=50, help_text='Primer Nombre', verbose_name=u'PrimerNombre', null=True)
	CensoSegundoNombre = models.CharField(max_length=50, help_text='Segundo Nombre', verbose_name=u'SegundoNombre', null=True)
	CensoPrimerApellido = models.CharField(max_length=50, help_text='Primer Apellido', verbose_name=u'PrimerApellido', null=True)
	CensoSEgundoApellido = models.CharField(max_length=50, help_text='Segundo Apellido', verbose_name=u'SegundoApellido', null=True)
	CensoFila = models.CharField(max_length= 50, help_text='Fila', verbose_name=u'Fila', null=True)
	CensoFechaNac = models.CharField(max_length=20, help_text='Fecha de Nacimiento', verbose_name=u'Fecha', null=True)

	def __unicode__(self):
		return self.CensoNumIdentidad + ' ' + self.CensoPrimerNombre + ' ' + self.CensoPrimerApellido

class ListaCautela(models.Model):
	NumIdentidad = models.CharField(max_length=20, help_text='Numero de Identidad', verbose_name=u'Identidad', primary_key=True)
	NombreCompleto = models.CharField(max_length=150, help_text='Nombre Completo', verbose_name=u'Nombre', null=True)
	FechaIngreso = models.DateField(help_text='Fecha de Ingreso', verbose_name=u'Fecha', null=True)
	Motivo = models.TextField(help_text='Descripcion del motivo', verbose_name=u'Motivos', null=True)
	Nacionalidad = models.CharField(max_length=50, help_text='Nacionalidad', verbose_name=u'Nacionalidad', null=True)

	def __unicode__(self):
		return self.NombreCompleto

#class ResultadosScore(models.Model):
	#AfiliadoNumIdentidad = models.ForeignKey(Afiliado)
	#TiposdeServicio = models.ManyToManyField(TipoServicio)
	#CanalesdeDistribucion = models.ManyToManyField(CanalesDistribucion)

	#def __unicode__(self):
		#return self.id
				