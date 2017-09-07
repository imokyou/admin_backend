from django.conf.urls import url
import views


urlpatterns = [
    url(r'^test/$', views.test),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
]
