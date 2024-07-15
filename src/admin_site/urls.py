from django.urls import path
from django.views import defaults as default_views

from .views.applications import applications_list, delete_application, update_status
from.views.index import index, login_view,logout_view


urlpatterns = [
  path('', index, name='home'),
    path('login/', login_view, name='login'),
    path("logout/", logout_view, name="logout"),
    path("applicantions/", applications_list, name="applications"),
  path('update_status/', update_status, name='update_status'),
  path('delete-application/', delete_application , name='delete_application'),
  
]