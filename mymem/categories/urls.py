from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^categories/$', views.CategoriesList.as_view()),
]