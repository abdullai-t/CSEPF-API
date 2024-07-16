from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from database.models import Application, Fellow, Presentation
from django.contrib.auth.decorators import login_required


@login_required(login_url="/login/")
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


def login_view(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		next_url = request.POST.get('next', 'home')
		
		user = authenticate(request, username=username, password=password)
		
		if user is not None:
			login(request, user)
			return redirect("home")
		else:
			return render(request, 'login.html', {'error': 'Invalid username or password'})
		
	return render(request, 'login.html')


def logout_view(request):
	logout(request)
	return redirect('login')


def handler404(request, exception):
	return render(request, '404.html', status=404)

def handler500(request):
	return render(request, '500.html', status=500)

def handler403(request, exception):
	return render(request, '403.html', status=403)

def handler400(request, exception):
	return render(request, '400.html', status=400)
	

