from django.urls import path
from django.views import defaults as default_views
from.views.index import index


urlpatterns = [
  path('', index, name='home'),
]