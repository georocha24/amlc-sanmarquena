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
from principal.forms import *

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

@login_required(login_url='/ingresar/')
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

	#Comparaciones de lugar de residencia del afiliado
	if RiesgosZonasGeo.objects.filter(RiesgoZonaGeo__icontains=cooperativista.LugarResidencia).exists():
		porzonageo = RiesgosZonasGeo.objects.get(RiesgoZonaGeo__icontains=cooperativista.LugarResidencia).RiesgosIdPorc.Porcentajes
	else:
		porzonageo = 0

	#Comparaciones del listado UIF
	uif = UIFRequerimientos.objects.filter(UIF_PrimerNombre = cooperativista.NombreCompleto).count()
	if uif > 0:
		datouif = 10
	else:
		datouif = 0

	#Comparaciones del listado de cautela
	cautela = ListaCautela.objects.filter(NombreCompleto = cooperativista.NombreCompleto).count()
	if cautela > 0:
		datocautela = 10
	else:
		datocautela = 0

	#Comparaciones del Listado PEPSNAC
	pepnac = PEPSNAC.objects.filter(NombreCompleto = cooperativista.NombreCompleto).count()
	if pepnac > 0:
		datopepsnac = 10
	else:
		datopepsnac = 0

	#Comparaciones del Listado PEPSEXT
	pepext = PEPSEXT.objects.filter(NombreCompleto=cooperativista.NombreCompleto).count()
	if pepext > 0:
		datopepsext = 10
	else:
		datopepsext = 0

	#Comparaciones si es beneficiario final de la cuenta
	bene = cooperativista.BeneficiarioFinal
	if bene == True:
		bene1 = 10
	else:
		bene1 = 0

	#Resultados del muestreo de las filiales a la que el cooperativista asiste
	#--> filial Oficina Principal
	op = cooperativista.OF
	if op == True:
		porfilial1 = CanalesDistribucion.objects.get(NombreOficina__icontains='Oficina Principal').RiesgosIdPorc.Porcentajes
	else:
		porfilial1 = 0

	#--> Filial Choluteca
	fc = cooperativista.FLC 
	if fc == True:
		porfilial2 = CanalesDistribucion.objects.get(NombreOficina__icontains='Filial Choluteca').RiesgosIdPorc.Porcentajes
	else:
		porfilial2 = 0

	#--> Filial Danli
	fdl = cooperativista.FLDL
	if fc == True:
		porfilial3 = CanalesDistribucion.objects.get(NombreOficina__icontains='Filial Danli').RiesgosIdPorc.Porcentajes
	else:
		porfilial3 = 0

	#--> Filial Duyure
	fd = cooperativista.FLD
	if fd == True:
		porfilial4 = CanalesDistribucion.objects.get(NombreOficina__icontains='Filial Duyure').RiesgosIdPorc.Porcentajes
	else:
		porfilial4 = 0

	#--> Filial Duyure
	fd = cooperativista.FLD
	if fd == True:
		porfilial4 = CanalesDistribucion.objects.get(NombreOficina__icontains='Filial Duyure').RiesgosIdPorc.Porcentajes
	else:
		porfilial4 = 0

	#--> Filial Granjas
	fg = cooperativista.FLG
	if fg == True:
		porfilial5 = CanalesDistribucion.objects.get(NombreOficina__icontains='Filial Granjas').RiesgosIdPorc.Porcentajes
	else:
		porfilial5 = 0

	#--> Filial Kennedy
	fkn = cooperativista.FLK
	if fkn == True:
		porfilial6 = CanalesDistribucion.objects.get(NombreOficina__icontains='Filial Kennedy').RiesgosIdPorc.Porcentajes
	else:
		porfilial6 = 0

	#diccionario que me devuelve la suma y promedio de los puntajes de las filiales
	promediofiliales = (porfilial1 + porfilial2 + porfilial3 + porfilial4 + porfilial5 + porfilial6) / 6

	diccionario['PorcNacion']= poractividad 
	diccionario['PorcActividad'] = poractividadecon 
	diccionario['uif'] = datouif
	diccionario['cautela'] = datocautela
	diccionario['pepnac'] = datopepsnac
	diccionario['pepext'] = datopepsext
	diccionario['zonageo'] = porzonageo
	diccionario['beneficiario'] = bene1
	diccionario['filiales'] = promediofiliales 
	diccionario['total'] = poractividad + poractividadecon + datouif + datocautela + datopepsnac + datopepsext + porzonageo + promediofiliales
	
	if not request.user.is_anonymous():
		diccionario['usuario'] = request.user
		diccionario['validador'] = True
	return render_to_response('resultadosscore.html',diccionario, context_instance=RequestContext(request))

@login_required(login_url="/ingresar/")
def perfilusuario(request):
	diccionario={}
	if not request.user.is_anonymous():
		diccionario['usuario'] = request.user 
		diccionario['validador'] = True 
		diccionario['Perfil'] = User.objects.get(id=request.user.id)
	return render_to_response('perfiluser.html', diccionario, context_instance=RequestContext(request))

@login_required(login_url='/ingresar/')
def editarusuario(request):
	diccionario={}
	if not request.user.is_anonymous():
		diccionario['usuario']=request.user 
		diccionario['validador'] = True 
		diccionario['Perfil'] = User.objects.get(id=request.user.id)
	return render_to_response('editaruser.html', diccionario, context_instance=RequestContext(request))

@login_required(login_url='/ingresar/')
def actualizarusuario(request):
	if not request.user.is_anonymous():
		if request.method=='POST':
			nombre = request.POST['Nombre']
			apellido = request.POST['Apellido']
			email = request.POST['Correo']
			usuario = request.POST['Usuario']

			u=User.objects.get(pk=request.user.id)

			u.first_name = nombre
			u.last_name = apellido
			u.email = email 
			u.username = usuario
			u.save()
			return HttpResponseRedirect('/perfil-user/')
		else:
			raise Http404
	else:
		return HttpResponseRedirect('/ingresar/')

def registrar(request):
	if request.method=='POST':
		usuario = NuevoUserForm(request.POST)
		if usuario.is_valid():
			usuarios = usuario.cleaned_data["username"]
			contrasena = usuario.cleaned_data["password"]
			email = usuario.cleaned_data["email"]
			nombres = usuario.cleaned_data["first_name"]
			apellidos = usuario.cleaned_data["last_name"]

			user = User.objects.create_user(usuarios, email, contrasena)
			user.first_name = nombres
			user.last_name = apellidos

			user.save()

			acceso = authenticate(username=usuarios, password=contrasena)
			login(request, acceso)
			return HttpResponseRedirect('/')
	else:
		usuario = NuevoUserForm()
		return render_to_response('registrar.html', context_instance=RequestContext(request))
