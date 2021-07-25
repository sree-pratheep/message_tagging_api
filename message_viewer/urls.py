from django.urls import path
from . import views
from .views import (
    TelegramMessageListView,
    TelegramMessageDetailView,
    TelegramMessageCreateView,
    TelegramMessageUpdateView,
    TelegramMessageDeleteView,
    TelegramMessageFilterListView,
)

urlpatterns = [
    path('', TelegramMessageListView.as_view(), name="message_viewer-home"),
    path('message/<int:pk>', TelegramMessageDetailView.as_view(), name="message-detail"),
    path('message/<int:pk>/next', TelegramMessageDetailView.as_view(), name="message-detail-next"),
    path('message/<int:pk>/prev', TelegramMessageDetailView.as_view(), name="message-detail-prev"),
    path('message/new', TelegramMessageCreateView.as_view(), name="message-create"),
    path('message/<int:pk>/update/', TelegramMessageUpdateView.as_view(), name="message-update"),
    path('media/<int:pk>/update/', views.add_message_tags, name="media-update"),
    path('message/<int:pk>/delete/', TelegramMessageDeleteView.as_view(), name="message-delete"),
    path('message_viewer-status', views.api_status, name="message_viewer-json-status"),
    path('message/search/<str:searched>/', views.search_messages, name="search-messages"),
    path('message/search/', views.search_messages, name="search-messages-post"),
    path('refresh-data', views.import_json_data, name="import-json-data"),
    path('json-data-status', views.data_stats, name="json-data-status"),
    path('message/filter_list', TelegramMessageFilterListView.as_view(), name="filter-messages"),
]
