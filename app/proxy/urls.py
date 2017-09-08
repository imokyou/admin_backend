from django.conf.urls import include, url
import views


urlpatterns = [
    url(r'^test/', views.test),
    url(r'^user/', include('app.proxy.user.urls')),
    url(r'^ippool/', include('app.proxy.ippool.urls')),
    url(r'^apikey/', include('app.proxy.apikey.urls')),
]
