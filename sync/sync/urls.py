
from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as swagger_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include('api.urls'))
]
urlpatterns += swagger_urls