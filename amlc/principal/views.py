from principal.models import UIFRequerimientos, Afiliado, Censo
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from django.shortcuts import render

# Create your views here.


#Vistas Individuales extrayendo todos los objetos
def Afiliados(request):
	afiliaditos = Afiliado.objects.all()
	return render_to_response('inicio.html', {'afiliaditos':afiliaditos})

#Vistas 
