from django.urls import path
from . import views

urlpatterns = [
    path('api-home', views.home, name="api-home"),
    path('api-status', views.api_status, name="api-json-status"),
    path('refresh-data', views.import_json_data, name="import-json-data"),
    path('json-data-status', views.data_stats, name="Stats of JSON data"),

]
