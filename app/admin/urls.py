from django.conf.urls import include, url
import views


urlpatterns = [
    url(r'^test/', views.test),
    url(r'^user/', include('app.admin.user.urls'))
]
