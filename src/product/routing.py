from django.urls import path
from . import consumers


websocket_urlpatterns = [

    path('api/getdata/', consumers.McxDataRetrieve)
]
