# coding=utf-8
from django.conf.urls import include, url


# 总的URL设置,新版本按下面的来不会有warning.
urlpatterns = [
    url(r'^api/common/', include('app.common.urls')),
    url(r'^api/auth/', include('app.auth.urls')),
    url(r'^api/admin/', include('app.admin.urls'))
]
