from django.db import models
from message_viewer.models import TelegramMedia


class TableFromImage(models.Model):
    telegram_media = models.ForeignKey(TelegramMedia, on_delete=models.CASCADE, related_name='parsed_table')
    total_columns = models.IntegerField(default=None, blank=False, null=False)
    total_rows = models.IntegerField(default=None, blank=False, null=False)

    def __str__(self):
        return str(self.id)+":("+str(self.total_rows)+","+str(self.total_columns)+")"


class TableRowFromImage(models.Model):
    table = models.ForeignKey(TableFromImage, on_delete=models.CASCADE, related_name="table_rows")
    row = models.IntegerField(default=None, blank=False, null=False)

    class Meta:
        ordering = ['row', ]


class TableCellFromImage(models.Model):
    row = models.ForeignKey(TableRowFromImage, on_delete=models.CASCADE, related_name="table_cells")
    column = models.IntegerField(default=None, blank=False, null=False)
    text = models.CharField(max_length=1000, default=None, blank=False, null=False)
    image = models.TextField(default=None, null=False)
    processed_image = models.TextField(default=None, null=False)

    class Meta:
        ordering = ['column', ]
