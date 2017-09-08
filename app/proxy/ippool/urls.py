from django.conf.urls import url
import views


urlpatterns = [
    url(r'^test/$', views.test),
    url(r'^get-list/$', views.get_list)
]
