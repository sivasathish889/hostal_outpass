from django.contrib import admin
from django.urls import path,include
import student.urls
import warden.urls
import security.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(student.urls)),
    path("warden/", include(warden.urls)),
    path("security/", include(security.urls))

]
