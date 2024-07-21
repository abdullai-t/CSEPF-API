from django.urls import path

from .views.applications import applications_list, delete_application, update_status
from .views.fellows import add_fellow, delete_fellow, fellow_list, update_fellow
from .views.index import index, login_view, logout_view
from .views.presentations import add_presentation, delete_presentation, presentations_list, update_presentation
from .views.projects import delete_project,update_project, projects_list, add_project
from .views.site_trips import add_image_to_site_trip, create_site_trip, delete_site_trip, remove_image_from_site_trip, \
    site_trip_images, site_trips_list, update_site_trip
from .views.staff import add_staff, delete_staff, staff_list, update_staff
from .views.testimonials import add_testimonial, delete_testimonial, list_testimonials, \
    update_testimonial

urlpatterns = [
    path("", index, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("applications/", applications_list, name="applications"),
    path("applications/update/", update_status, name="update_status"),
    path("applications/delete/<str:id>", delete_application, name="delete_application"),
    
    path("testimonials/", list_testimonials, name="testimonials"),
    path("testimonials/add/", add_testimonial, name="add_testimonial"),
    path("testimonials/update/<str:id>", update_testimonial, name="update_testimonial"),
    path("testimonials/delete/<str:id>", delete_testimonial, name="delete_testimonial"),
    
    #     projects
    path("projects/", projects_list, name="projects"),
    path("projects/add/", add_project, name="add_project"),
    path("projects/update/<str:id>", update_project, name="update_project"),
    path("projects/delete/<str:id>", delete_project, name="delete_project"),
    
    #     staff
    path('staff/', staff_list, name='staff'),
    path('staff/add/', add_staff, name='add_staff'),
    path('staff/update/<str:id>', update_staff, name='update_staff'),
    path('staff/delete/<str:id>', delete_staff, name='delete_staff'),
    
    #     fellow
    path('fellows/', fellow_list, name='fellows'),
    path('fellows/add/', add_fellow, name='add_fellow'),
    path('fellows/update/<str:id>', update_fellow, name='update_fellow'),
    path('fellows/delete/<str:id>', delete_fellow, name='delete_fellow'),
    
    #     presentations
    path('presentations/', presentations_list, name='presentations'),
    path('presentations/add/', add_presentation, name='add_presentation'),
    path('presentations/update/<str:id>', update_presentation, name='update_presentation'),
    path('presentations/delete/<str:id>', delete_presentation, name='delete_presentation'),
    
    #     site trips
    path('site_trips/', site_trips_list, name='site_trips'),
    path('site_trips/add/', create_site_trip, name='add_site_trip'),
    path('site_trips/update/<str:id>', update_site_trip, name='update_site_trip'),
    path('site_trips/delete/<str:id>', delete_site_trip, name='delete_site_trip'),
    path('site_trips/add_image', add_image_to_site_trip, name='add_image_to_site_trip'),
    path('site_trips/remove_image/<str:image_id>', remove_image_from_site_trip, name='remove_image_from_site_trip'),
    path('site_trip/<str:id>/images', site_trip_images, name='site_trip_images'),
]

