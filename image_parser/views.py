from django.shortcuts import render
from django.contrib import messages
from django.views.generic import UpdateView

from .models import TableFromImage, TelegramMedia, TableRowFromImage
from .india.stats import get_table_cells


def process_image(request, message_id):
    media_message = TelegramMedia.objects.get(pk=message_id)
    parsed_table, rows, cells = get_table_cells('/home/sree/covid-project/' + media_message.media_path)
    parsed_table.telegram_media = media_message
    parsed_table.save()
    messages.success(request, f'Image processed successfully!')
    for row in rows:
        row.save()
    for cell in cells:
        cell.save()

    return render(request, 'image_parser/processed_table.html', {'table': parsed_table})


class TableDataUpdateView(UpdateView):
    model = TableRowFromImage
    fields = ['total_rows', 'total_columns']

