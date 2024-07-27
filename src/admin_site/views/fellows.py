from datetime import datetime

from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from database.forms import UserProfileForm
from database.models import Fellow

SCHOOLS = ["University of Colorado Boulder",
           "Colorado State University",
           "University of Denver",
           "Colorado College",
           "Metropolitan State University of Denver",
           "Colorado School of Mines",
           "Regis University",
           "Adams State University",
           "Fort Lewis College",
           "Colorado Mesa University",
           "Western Colorado University",
           "University of Colorado Colorado Springs",
           "University of Northern Colorado",
           "Colorado Christian University",
           "Colorado Mountain College"
           ]


def fellow_list(request):
	fellow = Fellow.objects.all()
	paginator = Paginator(fellow, 10)  # Show 10 fellow members per page.
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	
	for f in page_obj:
		socials_str = "||".join([f"{key}#{value}" for key, value in f.info.get("socials", {}).items()])
		f.socials = socials_str
		f.user_image_url = f.user.picture.url if f.user.picture else ""
	
	return render(request, 'fellows_list.html', {'page_obj': page_obj, "schools": SCHOOLS})


def add_fellow(request):
	if request.method == "POST":
		bio = request.POST.get('bio')
		facebook = request.POST.get('facebook')
		linkedin = request.POST.get('linkedin')
		twitter = request.POST.get('twitter')
		is_completed = request.POST.get('is_completed')
		school = request.POST.get('school')
		program = request.POST.get('program')
		cohort = request.POST.get('cohort', datetime.now().year)
		
		print(request.POST)
		
		user = UserProfileForm(request.POST, request.FILES)
		if user.is_valid():
			user = user.save()
		
		else:
			messages.error(request, 'Error adding fellow member.')
			return redirect('fellows')
		
		
		
		fellow = Fellow(user=user, bio=bio, is_completed=True if is_completed == 'on' else False, school=school, program=program, cohort=cohort)
		fellow.info = {
			"socials": {
				"facebook": facebook,
				"linkedin": linkedin,
				"twitter": twitter
			}}
		fellow.save()
		messages.success(request, 'Fellow member added successfully.')
	
	return redirect('fellows')


def update_fellow(request, id):
	
	fellow = get_object_or_404(Fellow, pk=id)
	if request.method == "POST":
		facebook = request.POST.get('facebook', fellow.info.get("socials", {}).get("facebook"))
		linkedin = request.POST.get('linkedin', fellow.info.get("socials", {}).get("linkedin"))
		twitter = request.POST.get('twitter', fellow.info.get("socials", {}).get("twitter"))
		bio = request.POST.get('bio', fellow.bio)
		is_completed = request.POST.get('is_completed', fellow.is_completed)		
		
		applicant = fellow.user
		if request.FILES.get('picture'):
			applicant.picture = request.FILES.get('picture')
			applicant.save()

		fellow.info = {
			"socials": {
				"facebook": facebook,
				"linkedin": linkedin,
				"twitter": twitter
			}}
		
		fellow.bio = bio
	
		fellow.is_completed = True if is_completed == 'on' else False
		fellow.save()
		messages.success(request, 'Fellow member updated successfully.')
	
	return redirect('fellows')


def delete_fellow(request, id):
	fellow = get_object_or_404(Fellow, pk=id)
	fellow.delete()
	return redirect('fellows')
