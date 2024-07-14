from django.http import HttpResponse
from django.shortcuts import render

from database.models import Application, Fellow, Presentation


def index(request):
	num_applications = Application.objects.count()
	num_presentations = Presentation.objects.count()
	num_fellows = Fellow.objects.count()
	
	context = {
		'num_applications': num_applications,
		'num_presentations': num_presentations,
		'num_fellows': num_fellows
	}
	return render(request, 'home.html', context)


def handler404(request, exception):
	return render(request, '404.html', status=404)

def handler500(request):
	return render(request, '500.html', status=500)

def handler403(request, exception):
	return render(request, '403.html', status=403)

def handler400(request, exception):
	return render(request, '400.html', status=400)
	

