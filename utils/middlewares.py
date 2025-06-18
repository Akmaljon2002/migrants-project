import os
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import traceback
import requests
import socket
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
USER_ID = 887307931
TARGET_SERVER_HOSTNAME = ['vps02306.eskiz.uz']


class SendErrorToBotMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.hostname = socket.gethostname()

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if self.hostname in TARGET_SERVER_HOSTNAME:
            token = BOT_TOKEN
            chat_id = USER_ID
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            traceback_info = traceback.format_exc()
            exception_type = type(exception).__name__
            message = f"TaxiProject\n{exception_type}: {str(exception)}\n\n{traceback_info}\n\nTaxiProject"
            data = {
                'chat_id': chat_id,
                'text': message
            }
            requests.post(url=url, params=data)


class DoesNotExistMiddleware:
    def __init__(self, get_response, model=None):
        self.get_response = get_response
        self.model = model

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, ObjectDoesNotExist):
            model = str(exception).split(" ")[0]
            return JsonResponse({"response": f"{model} not found!"}, status=404)
