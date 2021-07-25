from django.urls import path
from . import views
from .views import api_status, table_data_list


urlpatterns = [
    path('', api_status, name="api-status"),
    path('parser/image/table/', table_data_list, name="parsed-image-data"),
]
