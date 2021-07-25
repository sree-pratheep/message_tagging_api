from django.urls import path
from . import views
from .views import manage_data


urlpatterns = [
    path('media/<int:message_id>/job/', views.process_image, name="image-parser-process"),
    path('media/table/<int:id>', manage_data, name="table-data-update"),
]
