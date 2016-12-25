from django.conf.urls import url
from . import views

app_name = 'places'

urlpatterns = [
   # url(r'^home/$', views.home, name = 'home'),

    url(r'^register/$', views.adduser, name='register'),
    url(r'^$', views.logins, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^connection/$', views.formView, name='connection'),

    # /country_id/
    url(r'^(?P<country_id>[0-9]{1})$', views.city, name='city'),

    # country_id/city/
    url(r'^(?P<city_id>[0-9]{2})/[0-9]{2}$', views.place, name='place'),

    # country_id/city/attractions
    url(r'^[0-9]{2}/attractions/$', views.attraction, name='attraction'),

    url(r'^[0-9]{2}/booked/$', views.book, name='book')
    #country_id/city/attractions
    #url(r'^(?P<country_id>[0-9]+)/attraction/$', views.attraction, name = 'attraction')

    #country_id/city/attractions/place
    #url(r'^(?P<country_id>[0-9]+)/city/attractions/$', views.attraction, name='attraction')

]