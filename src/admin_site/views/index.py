from django.http import HttpResponse
from django.shortcuts import render


def index(request):
	# this is the simplest view possible in Django
	return HttpResponse("Hello, world!")


def handler404(request, exception):
	return render(request, '404.html', status=404)

def handler500(request):
	return render(request, '500.html', status=500)

def handler403(request, exception):
	return render(request, '403.html', status=403)

def handler400(request, exception):
	return render(request, '400.html', status=400)
	

