import os
import time
import json
import pandas as pd
from datetime import date, datetime

from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from .models import TelegramMessage, TelegramMedia
from .forms import MessageTagForm


message_json_path = '/home/sree/covid-project/telegram-messages/messages/'
PAGE_SIZE = 50


def add_message_tags(request, pk):
    if request.method == 'POST':
        form = MessageTagForm(request.POST)
        if form.is_valid():
            media = TelegramMedia.objects.get(pk=pk)
            media.category = form.cleaned_data['category']
            media.type = form.cleaned_data['type']
            media.save()
            messages.success(request, f'Media tags updated successfully!')
            return render(request, 'api/telegrammedia_form.html', {'form': form})
    else:
        media = TelegramMedia.objects.get(pk=pk)
        form = MessageTagForm(initial={'id': pk, 'media_path': media.media_path})
    return render(request, 'api/telegrammedia_form.html', {'form': form})


def search_messages(request, searched=None):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        return redirect('search-messages', searched=searched)
    elif request.method == 'GET':
        page_number = request.GET.get('page', 1)
    else:
        searched = None
        page_number = 1

    if searched:
        message_list = TelegramMessage.objects.filter(message__icontains=searched).order_by('-date')
    else:
        message_list = TelegramMessage.objects.all().order_by('-date')

    paginator = Paginator(message_list, PAGE_SIZE)
    page_obj = paginator.page(page_number)
    return render(request, 'api/search_results.html', {'page_obj': page_obj, 'searched': searched})


class TelegramMessageListView(ListView):
    model = TelegramMessage
    template_name = 'api/home.html'
    paginate_by = PAGE_SIZE
    ordering = ['-date']


class TelegramMessageDetailView(DetailView):
    model = TelegramMessage

    def get_object(self):
        url_name = self.request.resolver_match.url_name
        if url_name == 'message-detail':
            return super(TelegramMessageDetailView, self).get_object(queryset=self.queryset)
        if url_name == 'message-detail-next':
            return TelegramMessage.objects.filter(pk__gt=self.kwargs['pk']).earliest('pk')
        if url_name == 'message-detail-prev':
            return TelegramMessage.objects.filter(pk__lt=self.kwargs['pk']).latest('pk')
        return super(TelegramMessageDetailView, self).get_object(queryset=self.queryset)


class TelegramMessageCreateView(LoginRequiredMixin, CreateView):
    model = TelegramMessage
    fields = ['grouped_id', 'media_path', 'text',
              'raw_text', 'message', 'date', 'views',
              'forwards', 'media_size', 'has_media']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TelegramMessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TelegramMessage
    fields = ['grouped_id', 'media_path', 'text',
              'raw_text', 'message', 'date', 'views',
              'forwards', 'media_size', 'has_media']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        #        if self.request.user == model.author
        return True


class TelegramMessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TelegramMessage
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        #        if self.request.user == model.author
        return True


class TelegramMediaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TelegramMedia
    fields = ['category', 'type']

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        #        if self.request.user == model.author
        return True


def message_object_decoder(obj):
    message = TelegramMessage()
    message.message = obj['message']
    message.id = obj['id']
    message.grouped_id = obj['grouped_id']
    message.text = obj['text']
    message.date = obj['date']
    message.forwards = obj['forwards']
    message.has_media = obj['has_media']
    message.media_path = obj['media_path'] if not obj['media_path'] else obj['media_path'].replace(
        '/home/sree/covid-project/', '')
    message.media_size = obj['media_size']
    message.raw_text = obj['raw_text']
    message.views = obj['views']
    return message


def import_json_data(request):
    max_message_id = 0
    max_date = datetime.min
    latest_message = TelegramMessage.objects.first()
    if latest_message:
        latest_message = TelegramMessage.objects.latest('id')
        max_message_id = latest_message.id
        max_date = latest_message.date
    written = 0
    current_group_id = None
    current_message = None
    for filename in sorted(os.listdir(message_json_path)):
        if datetime.strptime(filename.split('.json')[0], '%Y-%m-%d') < datetime.strptime(str(max_date.date()), '%Y-%m-%d'):
            print(filename, ' skipped')
            continue
        with open(os.path.join(message_json_path, filename)) as fp:
            for line in fp:
                message = json.loads(line, object_hook=message_object_decoder)
                message.channel_name = 'Telegram-India-Covid-Updates'
                if message.id > max_message_id:
                    if not message.grouped_id or message.grouped_id != current_group_id:
                        message.save()
                        written += 1
                if message.has_media:
                    if not message.grouped_id or message.grouped_id != current_group_id:
                        current_group_id = message.grouped_id
                        current_message = message
                    media_message = TelegramMedia()
                    media_message.id = message.id
                    media_message.grouped_id = current_group_id
                    media_message.media_path = message.media_path
                    if message.media_path and len(message.media_path.split('.')) > 1:
                        media_message.media_type = message.media_path.split('.')[-1]
                    media_message.telegram_message = current_message
                    media_message.save()
                print("Message id ", message.id)
        # print(len(message_list))
        print(filename)
        if filename == '2020-12-20.json':
            break
    return JsonResponse({'status': "Succeeded"})


def data_stats(request):
    file_list = os.listdir(message_json_path)
    status = {'json': {}}
    status['json']['number_of_files'] = len(file_list)
    total_messages = 0
    max_id = 0
    for filename in sorted(file_list):
        df = pd.read_json(path_or_buf=os.path.join(message_json_path, filename), lines=True)
        total_messages = total_messages + int(df.shape[0])
        max_id = max(df['id'].max(), max_id)
    status['json']['total_messages'] = total_messages
    status['json']['max_id'] = max_id
    print(json.dumps(status))
    return JsonResponse(status)


def api_status(request):
    s = {'test': 'test1', 'test1': 'test2'}
    return JsonResponse(s)
