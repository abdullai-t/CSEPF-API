from django.apps import apps
from django.contrib import admin


def register_all_models():
    for model in apps.get_models():
        try:
            admin.site.register(model)
        except admin.sites.AlreadyRegistered:
            pass


register_all_models()
