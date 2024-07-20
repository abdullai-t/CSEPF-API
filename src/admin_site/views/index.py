from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from database.models import Application, Fellow, Presentation, Project, Staff, Testimonial
from django.contrib.auth.decorators import login_required


@login_required(login_url="/login/")
def index(request):
	num_applications = Application.objects.count()
	num_presentations = Presentation.objects.count()
	num_fellows = Fellow.objects.count()
	num_testimonials = Testimonial.objects.count()
	num_staff = Staff.objects.count()
	num_projects = Project.objects.count()
	
	
	user = request.user
	
	data = {
		'Applications': num_applications,
		'Presentations': num_presentations,
		'Fellows': num_fellows,
		'Testimonials': num_testimonials,
		'Staff': num_staff,
		'Projects': num_projects,
		
	}
	
	
	return render(request, 'home.html', {'data': [(key, value) for key, value in data.items()], 'user': user})


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
	

