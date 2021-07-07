from django.contrib import admin
from .models import TelegramMessage, TelegramMedia

admin.site.register(TelegramMessage)
admin.site.register(TelegramMedia)