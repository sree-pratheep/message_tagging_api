import os
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from .models import TelegramMessage

message_json_path = '/home/sree/covid-project/telegram-messages/messages/'


def home(request):
    message_list = TelegramMessage.objects.all()[:10]
    return render(request, 'api/home.html', {'telegram_messages': message_list})



def message_object_decoder(obj):
    message = TelegramMessage()
    message.message = obj['message']
    message.id = obj['id']
    message.grouped_id = obj['grouped_id']
    message.text = obj['text']
    message.date = obj['date']
    message.forwards = obj['forwards']
    message.has_media = obj['has_media']
    message.media_path = obj['media_path']
    message.media_size = obj['media_size']
    message.raw_text = obj['raw_text']
    message.views = obj['views']
    return message


def import_json_data(request):
    max_message_id = TelegramMessage.objects.latest('id').id
    for filename in sorted(os.listdir(message_json_path)):
        with open(os.path.join(message_json_path, filename)) as fp:
            for line in fp:
                message = json.loads(line, object_hook=message_object_decoder)
                if message.id > max_message_id:
                    message.save()
                    break
        # print(len(message_list))
        print(filename)
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
