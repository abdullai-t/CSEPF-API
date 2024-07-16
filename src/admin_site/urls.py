from django.urls import path

from .views.applications import applications_list, delete_application, update_status
from .views.index import index, login_view, logout_view
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
]
