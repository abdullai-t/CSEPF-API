from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns(
    "",
    host(r"api", "api.urls", name="api"),
    host(r"admin.csepf", "admin_site.urls", name="admin-site"),
    host(r"su", "_main_.su_urls", name="mission-control"),
    host("", settings.ROOT_URLCONF, name="default"),
)
