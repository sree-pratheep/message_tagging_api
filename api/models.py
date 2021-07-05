from django.db import models
from django.urls import reverse


class TelegramMessage(models.Model):
    grouped_id = models.BigIntegerField(default=None, blank=True, null=True)
    media_path = models.fields.TextField(default=None, blank=True, null=True)
    text = models.fields.TextField(default=None, blank=True, null=True)
    raw_text = models.fields.TextField(default=None, blank=True, null=True)
    message = models.fields.TextField(default=None, blank=True, null=True)
    date = models.fields.DateTimeField(null=False)
    views = models.fields.IntegerField(default=0, null=True)
    forwards = models.fields.IntegerField(default=0, null=True)
    media_size = models.fields.BigIntegerField(default=0, null=True)
    has_media = models.fields.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('message-detail', kwargs={'pk': self.pk})

