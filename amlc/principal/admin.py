#endoding:utf-8
from django.contrib import admin
from principal.models import *
from actions import export_as_csv

# Register your models here.

class UIFRequerimientosAdmin(admin.ModelAdmin):
	list_display = ('UIF_NumRequerimiento','UIF_PrimerNombre','UIF_Identidad','UIF_FechaRequerimiento','UIF_Nac',)
	list_filter = ('UIF_Nac',)	
	search_fields = ('UIF_PrimerNombre', 'UIF_Identidad',)
	list_editable = ('UIF_Nac',)
	actions = [export_as_csv]

class AfiliadosAdmin(admin.ModelAdmin):
	list_display = ('NumIdentidad','NombreCompleto','LugarResidencia','Nacionalidad','ActividadEconomica',)
	search_fields = ('NumIdentidad', 'NombreCompleto',)
	list_filter = ('LugarResidencia', 'Nacionalidad',)
	fieldsets = (
		(('Datos Personales'), {'fields': ('NumIdentidad', 'NombreCompleto', 'LugarResidencia', 'Nacionalidad', 'ActividadEconomica', 'BeneficiarioFinal')}),
		(('Filiales'), {'fields': ('OF', 'FLG', 'FLK', 'FLC', 'FLD', 'FLDL')}),
		(('Tipos de Servicios'), {'fields': ('TipoServAhorro', 'TipoServPrestamo', 'TipoServUnired', 'TipoServAutoServ', 'TipoServRemesas')}),
		(('Autorizaciones'), {'fields': ('Revisado',)}),
	)

class RiesgosZonasGeoAdmin(admin.ModelAdmin):
	list_display = ('RiesgoZonaGeo','RiesgosIdPorc',)
	list_filter = ('RiesgosIdPorc',)
	search_fields = ('RiesgoZonaGeo',)

class CensosAdmin(admin.ModelAdmin):
	list_display = ('CensoNumIdentidad', 'CensoPrimerNombre', 'CensoSegundoNombre', 'CensoPrimerApellido', 'CensoSEgundoApellido', 'CensoFechaNac')
	search_fields = ('CensoNumIdentidad', 'CensoPrimerNombre', 'CensoSegundoNombre', 'CensoPrimerApellido', 'CensoSEgundoApellido','CensoFechaNac',)

class ListaCautelaAdmin(admin.ModelAdmin):
	list_display=('NumIdentidad', 'NombreCompleto', 'FechaIngreso', 'Nacionalidad')
	list_filter=('Nacionalidad',)
	search_fields=('NumIdentidad', 'NombreCompleto',)

class PEPSNACAdmin(admin.ModelAdmin):
	list_display=('NumIdentidad', 'NombreCompleto', 'DescripcionPolitica',)
	search_fields=('NombreCompleto', 'DescripcionPolitica')

class PEPSEXTAdmin(admin.ModelAdmin):
	list_display=('id','NombreCompleto', 'Descripcion',)
	search_fields=('NombreCompleto', 'Descripcion')

class CanalesDistribucionAdmin(admin.ModelAdmin):
	list_display=('NombreOficina', 'RiesgosIdPorc',)
				
		
#class ResultadosScoreAdmin(admin.ModelAdmin):
	#filter_horizontal = ('TiposdeServicio', 'CanalesdeDistribucion',)
		
				

admin.site.register(PEPSNAC, PEPSNACAdmin)
admin.site.register(PEPSEXT, PEPSEXTAdmin)
admin.site.register(Nacionalidades)
admin.site.register(UIFRequerimientos, UIFRequerimientosAdmin)
admin.site.register(PorcentajeRiesgos)
admin.site.register(RiesgosZonasGeo, RiesgosZonasGeoAdmin)
admin.site.register(RiesgosPaises)
admin.site.register(TipoServicio)
admin.site.register(UbicacionesFiliales)
admin.site.register(CanalesDistribucion, CanalesDistribucionAdmin)
admin.site.register(ActividadEconomica)
admin.site.register(Afiliado, AfiliadosAdmin)
admin.site.register(Censo, CensosAdmin)
admin.site.register(ListaCautela, ListaCautelaAdmin)
#admin.site.register(ResultadosScore, ResultadosScoreAdmin)