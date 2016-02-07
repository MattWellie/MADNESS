from django.conf.urls import include, url
from .views import index, upload_file, download

appname = 'web_interface'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^upload/$', upload_file, name='upload'),
    url(r'^download/$', download, name='download'),

]