from django.urls import path, include

from api.handler.applications import ApplicationsHandler

ROUTE_HANDLERS = [ApplicationsHandler()]

urlpatterns = []
for handler in ROUTE_HANDLERS:
    urlpatterns.extend(handler.get_routes_to_views())
