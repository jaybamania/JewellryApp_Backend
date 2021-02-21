"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from user.urls import router as user_router
# from product.urls import router as product_router


# class DefaultRouter(routers.DefaultRouter):
#     def extend(self, router):
#         self.registry.extend(router.registry)


# router = DefaultRouter()
# router.extend(user_router)
# router.extend(product_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include(user_router.urls)),
    # path('api/product/', include(product_router.urls)),
    path('api/user/', include('user.urls'), name='user'),
    path('api/product/', include('product.urls'), name='product'),
]
