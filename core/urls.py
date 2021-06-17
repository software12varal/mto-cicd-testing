from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mto/', include(('mto.urls', 'mto'), namespace="mto")),
    path('', include(('jobs.urls', 'jobs'), namespace="jobs")),
]
