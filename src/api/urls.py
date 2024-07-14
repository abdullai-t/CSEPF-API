from django.urls import path, include



ROUTE_HANDLERS = [
]

urlpatterns = [
]
for handler in ROUTE_HANDLERS:
    urlpatterns.extend(handler.get_routes_to_views())
