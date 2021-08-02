from django.urls import path
from . import views
from .views import api_status, table_data_list, update_verified_table_data


urlpatterns = [
    path('', api_status, name="api-status"),
    path('parser/image/table/<str:table_id>', table_data_list, name="parsed-image-data"),
    path('data/verified/table/', update_verified_table_data, name="save-verified-table-data"),
]
