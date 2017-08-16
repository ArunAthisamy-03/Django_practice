from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^retrieve/$', views.Retrieve.as_view()),
]