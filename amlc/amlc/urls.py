from principal.models import *
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.views import login, logout
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'amlc.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^$', 'principal.views.inicio', name='inicio'),
    url(r'^formcenso/$', 'principal.views.formcenso', name='formcenso'),
    url(r'^afiliados/$', 'principal.views.Afiliados', name='afiliados'),
    url(r'^buscar/$', 'principal.views.busquedacenso', name='busquedacenso'),
    url(r'^resultados-score/(?P<NumIdentidad>\w+)/$', 'principal.views.resultados_score', name='resultados_score'),
    url(r'^ingresar/$', login, {'template_name': 'ingresar.html',}, name='login'),
    url(r'^salir/$', logout, {'template_name': 'cerrarsesion.html',}, name='logout'),
    url(r'^perfil-user/$', 'principal.views.perfilusuario', name='perfilusuario'),
    url(r'^editar-user/$', 'principal.views.editarusuario', name='editarusuario'),
    url(r'^actualizar-user/$', 'principal.views.actualizarusuario', name='actualizarusuario'),
    url(r'^registro/$', 'principal.views.registrar', name='registrar'),
    #url(r'^Buscar/$', 'principal.views.BuscarPersonas', name='BuscarPersonas')
)
#url(r'^receta/(?P<id_receta>\d+)$','principal.views.detalle_receta'),