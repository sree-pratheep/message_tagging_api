from django.urls import path
from .views import manage_data, process_image


urlpatterns = [
    path('media/<int:message_id>/', process_image, name="image-parser-process"),
    path('media/table/<int:id>', manage_data, name="table-data-update"),
]
