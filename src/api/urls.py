from django.urls import path, include

from api.handler.applications import ApplicationsHandler
from api.handler.fellows import FellowsHandler
from api.handler.staff_handler import StaffHandler

ROUTE_HANDLERS = [ApplicationsHandler(),FellowsHandler(),StaffHandler(),]

urlpatterns = []
for handler in ROUTE_HANDLERS:
    urlpatterns.extend(handler.get_routes_to_views())
