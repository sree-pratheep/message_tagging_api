from django.db import models
from django.db.models import ForeignKey
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
    channel_name = models.fields.TextField(blank=False, null=False)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('message-detail', kwargs={'pk': self.pk})


class TelegramMedia(models.Model):
    grouped_id = models.BigIntegerField(default=None, blank=True, null=True)
    media_path = models.fields.TextField(default=None, blank=True, null=True)
    media_type = models.fields.TextField(default=None, blank=True, null=True)
    telegram_message: ForeignKey = models.ForeignKey(TelegramMessage, on_delete=models.CASCADE,
                                                     related_name='media_set')
    category = models.CharField(choices=[('India', 'India'), ('Tamil Nadu', 'Tamil Nadu')],
                                max_length=20,default=None, blank=True, null=True)
    type = models.CharField(choices=[('Stats', 'Stats'), ('News', 'News')],
                            max_length=20,default=None, blank=True, null=True)
