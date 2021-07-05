from django.urls import path
from . import views
from .views import (
    TelegramMessageListView,
    TelegramMessageDetailView,
    TelegramMessageCreateView,
    TelegramMessageUpdateView,
    TelegramMessageDeleteView
)

urlpatterns = [
    path('api-home', TelegramMessageListView.as_view(), name="api-home"),
    path('message/<int:pk>', TelegramMessageDetailView.as_view(), name="message-detail"),
    path('message/new', TelegramMessageCreateView.as_view(), name="message-create"),
    path('message/<int:pk>/update/', TelegramMessageUpdateView.as_view(), name="message-update"),
    path('message/<int:pk>/delete/', TelegramMessageDeleteView.as_view(), name="message-delete"),
    path('api-status', views.api_status, name="api-json-status"),
    path('refresh-data', views.import_json_data, name="import-json-data"),
    path('json-data-status', views.data_stats, name="Stats of JSON data"),
]
