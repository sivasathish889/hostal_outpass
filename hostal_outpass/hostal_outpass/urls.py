from django.contrib import admin
from django.urls import path,include
import student.urls
import warden.urls
import security.urls
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(student.urls)),
    path("warden/", include(warden.urls)),
    path("security/", include(security.urls)),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'security.views.error_404'

