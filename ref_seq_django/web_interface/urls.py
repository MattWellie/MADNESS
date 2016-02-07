from django.conf.urls import include, url
from .views import index, upload_file, download

appname = 'web_interface'
urlpatterns = [
    url(r'^$', upload_file, name='index'),
    url(r'^upload/$', upload_file, name='upload'),
    url(r'^download/(?P<document_id>[0-9]+)$', download, name='download'),

]