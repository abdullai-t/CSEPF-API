from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from database.forms import ProjectForm
from database.models import Project


def projects_list(request):
	projects = Project.objects.all()
	paginator = Paginator(projects, 10)  # Show 10 projects per page.
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	form = ProjectForm()
	return render(request, 'projects_list.html', {'page_obj': page_obj, 'form': form})


def add_project(request):
	if request.method == "POST":
		form = ProjectForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('projects')
	else:
		form = ProjectForm()
	return render(request, 'add_project_modal.html', {'form': form})


def update_project(request, id):
	project = get_object_or_404(Project, pk=id)
	if request.method == "POST":
		form = ProjectForm(request.POST, instance=project)
		if form.is_valid():
			form.save()
			return redirect('projects')
	else:
		form = ProjectForm(instance=project)
	return render(request, 'update_project_modal.html', {'form': form})

@login_required
def delete_project(request, id):
	project = get_object_or_404(Project, pk=id)
	project.delete()
	return redirect('projects')
