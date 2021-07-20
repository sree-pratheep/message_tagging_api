from django.urls import path
from . import views
from .views import TableDataUpdateView


urlpatterns = [
    path('media/<int:message_id>/job/', views.process_image, name="image-parser-process"),
    path('media/table/<int:pk>', TableDataUpdateView.as_view(), name="table-data-update"),
]
