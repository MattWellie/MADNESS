
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^web_interface/', include('web_interface.urls', namespace='web_interface')),
]
