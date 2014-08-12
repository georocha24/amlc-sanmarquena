from principal.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from django.shortcuts import render
from django.db.models import Q, Count
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage

validador = False
# Create your views here.


#Vistas Individuales extrayendo todos los objetos
def inicio(request):
	diccionario={}
	if not request.user.is_anonymous():
		diccionario['usuario'] = request.user
		diccionario['validador'] = True
	return render_to_response('inicio.html', diccionario, context_instance=RequestContext(request))

def formcenso(request):
	diccionario={}
	if not request.user.is_anonymous():
		diccionario['usuario'] = request.user
		diccionario['validador'] = True
	return render_to_response('formcenso.html', diccionario, context_instance=RequestContext(request))

@login_required(login_url='/ingresar/')
def Afiliados(request):
	diccionario={}
	diccionario['afiliado'] = Afiliado.objects.all()
	if not request.user.is_anonymous():
		diccionario['usuario'] = request.user
		diccionario['validador'] = True
	return render_to_response('afiliados.html', diccionario, context_instance=RequestContext(request))

#Seguridad
def ingresar(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/')
	if request.method == 'POST':
		formulario = AuthenticationForm(request.POST)
		if formulario.is_valid():
			usuario = request.POST['username']
			clave = request.POST['password']
			acceso = authenticate(username=usuario, password=clave)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return HttpResponseRedirect('/')
				else:
					return render_to_response('noactivo.html', context_instance=RequestContext(request))
			else:
				return render_to_response('nousuario.html', context_instance=RequestContext(request))
	else:
		formulario = AuthenticationForm()
	return render_to_response('ingresar.html', context_instance=RequestContext(request))


def busquedacenso(request):
	buscar = request.GET.get("buscaditas")
	buscar2 = request.GET.get("buscaditas1")
	buscar3 = request.GET.get("buscaditas2")
	buscar4 = request.GET.get("buscaditas3")
	pagina = request.GET.get("pagina")

	diccionario = {}

	resultado = Censo.objects.filter(CensoPrimerNombre__icontains=buscar, CensoSegundoNombre__icontains=buscar2, CensoPrimerApellido__icontains=buscar3, CensoSEgundoApellido__icontains=buscar4).distinct()
	num = Censo.objects.filter(CensoPrimerNombre__icontains=buscar, CensoSegundoNombre__icontains=buscar2, CensoPrimerApellido__icontains=buscar3, CensoSEgundoApellido__icontains=buscar4).count()

	diccionario['num'] = num

	diccionario['dato1'] = buscar
	diccionario['dato2'] = buscar2
	diccionario['dato3'] = buscar3
	diccionario['dato4'] = buscar4
 
	paginador = Paginator(resultado, 10)
	try:
		pagina = int(request.GET.get('pagina','1'))
		resultado = paginador.page(pagina)
	except PageNotAnInteger:
		pagina = 1
	except EmptyPage:
		resultado = paginador.page(paginador.num_pages)

	startPage = max(pagina - 2, 1)
	if startPage <= 3:
		startPage = 1

	endPage = pagina + 2 + 1
	if endPage >= paginador.num_pages - 1:
		endPage = paginador.num_pages + 1

	page_number = []

	for n in range(startPage, endPage):
		if n > 0 and n <= paginador.num_pages:
			page_number.append(n)
	diccionario['page_number'] = page_number
	diccionario['resultado'] = resultado

	if not request.user.is_anonymous():
		diccionario['usuario'] = request.user
		diccionario['validador'] = True
	return render_to_response('busquedacenso.html',diccionario, context_instance=RequestContext(request))

#Vista que devuelve los valores de cada comparacion
def resultados_score(request, NumIdentidad):
	diccionario={}
	cooperativista = get_object_or_404(Afiliado, pk=NumIdentidad)
	
	#Comparaciones de paises de riesgo
	if RiesgosPaises.objects.filter(RiesgoPais__icontains=cooperativista.Nacionalidad).exists():
		poractividad = RiesgosPaises.objects.get(RiesgoPais__icontains=cooperativista.Nacionalidad).RiesgosIdPorc.Porcentajes
	else:
		poractividad = 0

	#Comparaciones de actividades economicas
	if ActividadEconomica.objects.filter(ActividadEcon__icontains=cooperativista.ActividadEconomica).exists():
		poractividadecon = ActividadEconomica.objects.get(ActividadEcon__icontains=cooperativista.ActividadEconomica).RiesgosIdPorc.Porcentajes
	else:
		poractividadecon = 0

	#Comparaciones del listado UIF
	uif = UIFRequerimientos.objects.filter(UIF_PrimerNombre = cooperativista.PrimerNombre + cooperativista.SegundoNombre +" "+ cooperativista.PrimerApellido +" "+ cooperativista.SegundoApellido).count()
	if uif > 0:
		datouif = 10
	else:
		datouif = 0

	#Comparaciones del listado de cautela
	cautela = ListaCautela.objects.filter(NombreCompleto = cooperativista.PrimerNombre + cooperativista.SegundoNombre +" "+ cooperativista.PrimerApellido +" "+ cooperativista.SegundoApellido).count()
	if cautela > 0:
		datocautela = 10
	else:
		datocautela = 0

	#Comparaciones del Listado PEPSNAC
	pepnac = PEPSNAC.objects.filter(NombreCompleto = cooperativista.PrimerNombre + cooperativista.SegundoNombre +" "+ cooperativista.PrimerApellido +" "+ cooperativista.SegundoApellido).count()
	if pepnac > 0:
		datopepsnac = 10
	else:
		datopepsnac = 0

	#Comparaciones del Listado PEPSEXT
	pepext = PEPSEXT.objects.filter(NombreCompleto=cooperativista.PrimerNombre + cooperativista.SegundoNombre +" "+ cooperativista.PrimerApellido +" "+ cooperativista.SegundoApellido).count()
	if pepext > 0:
		datopepsext = 10
	else:
		datopepsext = 0

	diccionario['PorcNacion']= poractividad 
	diccionario['PorcActividad'] = poractividadecon 
	diccionario['uif'] = datouif
	diccionario['cautela'] = datocautela
	diccionario['pepnac'] = datopepsnac
	diccionario['pepext'] = datopepsext
	
	if not request.user.is_anonymous():
		diccionario['usuario'] = request.user
		diccionario['validador'] = True
	return render_to_response('resultadosscore.html',diccionario, context_instance=RequestContext(request))