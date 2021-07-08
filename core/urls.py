from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from mto.views import verify

urlpatterns = [
    path('verify/<str:token>', verify, name='verify'),
    path('super-admin/', include(('super_admin.urls', 'super_admin'), namespace="super_admin")),

    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('mto/', include(('mto.urls', 'mto'), namespace="mto")),
    path('', include(('jobs.urls', 'jobs'), namespace="jobs")),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
