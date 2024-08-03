from datetime import datetime
import json

from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from _main_.utils.constants import SCHOOLS
from database.forms import FellowForm
from database.models import Fellow


def fellow_list(request):
	fellow = Fellow.objects.all()
	paginator = Paginator(fellow, 10)  # Show 10 fellow members per page.
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	form = FellowForm()
	
	for f in page_obj:
		socials_str = "||".join([f"{key}#{value}" for key, value in f.info.get("socials", {}).items()])
		f.socials = socials_str
		f.user_image_url = f.picture.url if f.picture else ""
		f.resume_url = f.resume.url if f.resume else ""
		f.edit_fields = json.dumps({
			"full_name": f.full_name,
			"email": f.email,
			"phone_number": f.phone_number,
			"school": f.school,
			"program": f.program,
			"cohort": f.cohort,
			"has_completed": f.has_completed,
			"picture": f.picture.url if f.picture else "",
			"resume": f.resume.url if f.resume else "",
			"bio": f.bio,
			"address": f.address,
		})
		
	
	return render(request, 'fellows_list.html', {'page_obj': page_obj, "schools": SCHOOLS, "form": form})


def add_fellow(request):
	if request.method == "POST":
		if request.POST.get('has_completed') == 'on':
			request.POST._mutable = True
			request.POST['has_completed'] = True
		form = FellowForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			fellow = form.instance
			fellow.info = {
				"socials": {
					"facebook": request.POST.get('facebook'),
					"linkedin": request.POST.get('linkedin'),
					"twitter": request.POST.get('twitter')
				}}
			fellow.save()
			messages.success(request, 'Fellow member added successfully.')
		else:
			messages.error(request, 'Fellow member could not be added.')		
			
	return redirect('fellows')


def update_fellow(request, id):
	
	fellow = get_object_or_404(Fellow, pk=id)
	if request.method == "POST":
		if request.POST.get('has_completed'):
			request.POST._mutable = True
			request.POST['has_completed'] = True if request.POST.get('has_completed') == 'on' else False
		form = FellowForm(request.POST, request.FILES, instance=fellow)
		if form.is_valid():
			form.save()
			fellow = form.instance
			fellow.info = {
				"socials": {
					"facebook": request.POST.get('facebook'),
					"linkedin": request.POST.get('linkedin'),
					"twitter": request.POST.get('twitter')
				}}
			fellow.save()
			messages.success(request, 'Fellow member updated successfully.')
		else:
			messages.error(request, 'Fellow member could not be updated.')
		
		return redirect('fellows')


def delete_fellow(request, id):
    fellow = get_object_or_404(Fellow, pk=id)
    fellow.delete()
    return redirect("fellows")
