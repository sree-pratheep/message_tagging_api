from django.shortcuts import render
from django.contrib import messages
from django.views.generic import UpdateView
from django.forms import inlineformset_factory, modelformset_factory

from .models import TableFromImage, TelegramMedia, TableRowFromImage, TableCellFromImage
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



def manage_data(request, id):
    table_row = TableRowFromImage.objects.filter(table__id=id).first()
    TableRowInlineFormSet = inlineformset_factory(TableRowFromImage, TableCellFromImage, fields=['column', 'text', 'image'])
    formset = TableRowInlineFormSet(instance=table_row)

    return render(request, context={'form': formset}, template_name='image_parser/tablefromimage_form.html')

# class TableRowFromImage(UpdateView):
#     model = TableRowFromImage
#     fields = ['row']
#     queryset = TableRowFromImage.objects.filter( table_id = pk)
#

