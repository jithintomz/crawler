from django.conf.urls import url
from imagecrawl import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
]