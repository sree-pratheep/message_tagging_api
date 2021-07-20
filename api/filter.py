from django_filters import FilterSet, DateFilter, CharFilter
from api.models import TelegramMessage
from django.forms import DateInput



class TelegramMessageFilter(FilterSet):
    date__gt = DateFilter(field_name='date__date', lookup_expr='exact', label='Date')
    text_icase = CharFilter(field_name='text', lookup_expr='icontains', label='Text')
    class Meta:
        model = TelegramMessage
        fields = []
