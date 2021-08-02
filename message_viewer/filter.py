from django_filters import FilterSet, DateFilter, CharFilter
from message_viewer.models import TelegramMessage, TelegramMedia


class TelegramMessageFilter(FilterSet):
    date__lt = DateFilter(field_name='date__date', lookup_expr='lt', label='Date Below')
    date__exact = DateFilter(field_name='date__date', lookup_expr='exact', label='Date exact')
    text_icase = CharFilter(field_name='text', lookup_expr='icontains', label='Text')

    class Meta:
        model = TelegramMessage
        fields = []


class TelegramMediaFilter(FilterSet):
    category = CharFilter(field_name='category', lookup_expr='icontains', label='Category')
    telegram_message_date = CharFilter(method='filter_message_date', label='Date')
    telegram_message_text = CharFilter(method='filter_message_text', label='Text')

    def filter_message_date(self, queryset, name, value):
        return queryset.filter(telegram_message__date__date=value)

    def filter_message_text(self, queryset, name, value):
        return queryset.filter(telegram_message__text__icontains=value)

    class Meta:
        model = TelegramMedia
        fields = []
