from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect

from database.forms import TestimonialForm
from database.models import Fellow, Testimonial, UserProfile


def add_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
     
    return redirect('testimonials')  # Adjust the redirect as necessary


def update_testimonial(request, id):
    if request.method == 'POST':
        testimonial = Testimonial.objects.get(id=id)
        form = TestimonialForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
    
    return redirect('testimonials')  # Adjust the redirect as necessary


def delete_testimonial(request, id):
    testimonial = Testimonial.objects.get(id=id)
    testimonial.delete()
    
    return redirect('testimonials')  # Adjust the redirect as necessary


def list_testimonials(request):
    query = request.GET.get('q')
    if query:
        testimonials = Testimonial.objects.filter(Q(user__full_name__icontains=query))
    else:
        testimonials = Testimonial.objects.all()
        
    fellows = Fellow.objects.filter(cohort= datetime.now().year)
    
    paginator = Paginator(testimonials, 15)  # Show 10 applications per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    for t in page_obj:
        t.tag_ids = ','.join([str(id) for id in t.tags.all().values_list('id', flat=True)])
        
    
    form = TestimonialForm()
    
    return render(request, 'testimonials_list.html', {'page_obj': page_obj, 'query': query, 'fellows': fellows, "form": form})


