from django.shortcuts import render, redirect, get_object_or_404
from database.forms import SiteTripForm, SiteTripImageForm
from database.models import SiteTrip, SiteTripImage


def create_site_trip(request):
	if request.method == 'POST':
		form = SiteTripForm(request.POST)
		if form.is_valid():
			form.save()
	
	return redirect('site_trips')


def delete_site_trip(request, id):
	trip = get_object_or_404(SiteTrip, pk=id)
	trip.delete()
	return redirect('site_trips')


def update_site_trip(request, id):
	trip = get_object_or_404(SiteTrip, pk=id)
	if request.method == 'POST':
		form = SiteTripForm(request.POST, instance=trip)
		if form.is_valid():
			form.save()
	
	return redirect('site_trips')


def add_image_to_site_trip(request):
	if request.method == 'POST':
		trip_id = request.POST.get('trip')
		trip = SiteTrip.objects.get(pk=trip_id)
		site_trip_image = SiteTripImage(trip=trip, image=request.FILES['image'])
		site_trip_image.save()

	return redirect(f'/site_trip/{trip_id}/images')


def remove_image_from_site_trip(request, image_id):
	image = SiteTripImage.objects.get(pk=image_id)
	trip = image.trip.id
	if image:
		image.delete()
	return redirect(f'/site_trip/{trip}/images')


def site_trips_list(request):
	trips = SiteTrip.objects.all()
	trip_form = SiteTripForm()
	image_form = SiteTripImageForm()
	
	return render(request, 'site_trips_list.html', {'trips': trips, 'trip_form': trip_form, 'image_form': image_form})


def site_trip_images(request, id):
	trip = get_object_or_404(SiteTrip, pk=id)
	images = trip.images.all()
	return render(request, 'site_trip_images.html', {'trip': trip, 'images': images})
