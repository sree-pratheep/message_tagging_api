from django.db import models
from image_parser.models import TableFromImage


class VerifiedTableCell(models.Model):
    table = models.ForeignKey(TableFromImage, on_delete=models.CASCADE,
                              related_name='verified_cells')
    row = models.IntegerField(default=0, null=False)
    column = models.IntegerField(default=0, null=False)
    text = models.fields.TextField(default=None, blank=True, null=False)
    image = models.TextField(default=None, null=False)

    class Meta:
        # unique_together = ('table', 'row', 'column')
        ordering = ['row', 'column']
