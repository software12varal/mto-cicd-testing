from django.contrib import admin
from django.urls import path, include
from mto.views import verify


urlpatterns = [
    path('admin/', admin.site.urls),
    path('mto/', include(('mto.urls', 'mto'), namespace="mto")),
    path('', include(('jobs.urls', 'jobs'), namespace="jobs")),
    path('verify/<str:token>',verify,name='verify')

]
