from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from database.forms import StaffForm, UserProfileForm
from database.models import Staff, UserProfile



def staff_list(request):
    staff = Staff.objects.all()
    paginator = Paginator(staff, 10)  # Show 10 staff members per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    for s in page_obj:
        socials_str = "||".join([f"{key}#{value}" for key, value in s.user.info.get("socials", {}).items()])
        s.socials = socials_str
    
    return render(request, 'staffs_list.html', {'page_obj': page_obj,})


def add_staff(request):
    if request.method == "POST":
        role = request.POST.get('role')
        facebook = request.POST.get('facebook')
        linkedin = request.POST.get('linkedin')
        twitter = request.POST.get('twitter')
        bio = request.POST.get('bio')
        is_featured = request.POST.get('is_featured')
        
        user = UserProfileForm(request.POST, request.FILES)
        if user.is_valid():
            user.info = {
                "socials": {
                    "facebook": facebook,
                    "linkedin": linkedin,
                    "twitter": twitter
                }}
            
            user = user.save()
            
        else:
            messages.error(request, 'Error adding staff member.')
            return redirect('staff')
            
        staff = Staff(user=user, role=role, bio=bio, is_featured=True if is_featured == 'on' else False)
        staff.save()
        messages.success(request, 'Staff member added successfully.')

        
    return redirect('staff')


def update_staff(request, id):
    staff_member = get_object_or_404(Staff, pk=id)
    if request.method == "POST":
        role = request.POST.get('role', staff_member.role)
        facebook = request.POST.get('facebook', staff_member.user.info.get("socials", {}).get("facebook"))
        linkedin = request.POST.get('linkedin', staff_member.user.info.get("socials", {}).get("linkedin"))
        twitter = request.POST.get('twitter', staff_member.user.info.get("socials", {}).get("twitter"))
        bio = request.POST.get('bio', staff_member.bio)
        is_featured = request.POST.get('is_featured',staff_member.is_featured)
        
        user = staff_member.user
        user.full_name = request.POST.get('full_name', user.full_name)
        user.email = request.POST.get('email', user.email)
        if request.FILES.get('picture'):
            user.picture = request.FILES.get('picture')
        user.info = {
            "socials": {
                "facebook": facebook,
                "linkedin": linkedin,
                "twitter": twitter
            }}
        
        user.save()
        
        staff_member.role = role
        staff_member.bio = bio
        staff_member.is_featured = True if is_featured == 'on' else False
        staff_member.save()
        messages.success(request, 'Staff member updated successfully.')
    
    return redirect('staff')


def delete_staff(request, id):
    staff_member = get_object_or_404(Staff, pk=id)
    staff_member.delete()
    return redirect('staff')