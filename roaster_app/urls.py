from django.conf.urls import url

from . import views

urlpatterns = [

	url(r'^', views.home_page_home, name='home'),

]


