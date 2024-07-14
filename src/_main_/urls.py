from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('su/', admin.site.urls),
    path('mc/',include('_main_.su_urls')),
    path('api/', include('api.urls')),
    path('', include('admin_site.urls')),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#set error handling views
handler400 = 'admin_site.views.index.handler400'
handler403 = 'admin_site.views.index.handler403'
handler404 = 'admin_site.views.index.handler404'
handler500 = 'admin_site.views.index.handler500'
