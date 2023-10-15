import requests
import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    if request.method == 'POST':
        print(request.POST, request.FILES)
        file = request.FILES['file']

        files = {'files': file}

        # ВАЖНО: соединение с беком
        # url = 'http://127.0.0.1:5000/filechecker'
        # response = requests.post(url, files=files)
        # print(response.json())

        json_data = '{"М11_71_15.05.2023.pdf": ["Ошибка имени"],' \
                    ' "М-11 1390 от 31.01.2023.pdf": ["Ошибка имени"],' \
                    ' "М-11 1029 от 27.01.2023.pdf": ["Ошибка оформления"]}'
        result = json.loads(json_data)
        stat = {}
        for key, val in result.items():
            for error in val:
                stat[error] = stat.get(error, 0) + 1
        return render(request, "geocoder/stats.html", {'files': result, 'stat': stat})
    else:
        return render(request, "geocoder/index.html")


def learning(request):
    return render(request, "geocoder/stats.html")
