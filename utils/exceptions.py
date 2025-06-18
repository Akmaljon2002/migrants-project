import os
import traceback

import requests
from django.db.models import IntegerChoices
from rest_framework.exceptions import APIException
from rest_framework import serializers
from rest_framework.views import exception_handler
from rest_framework.response import Response
from dotenv import load_dotenv

load_dotenv()


class CustomValidationError(APIException):
    status_code = 400
    default_detail = "Something went wrong."

    def __init__(self, error_code, message):
        self.detail = {
            "error_code": str(error_code),
            "message": message
        }


class ErrorCodes(IntegerChoices):
    SOMETHING_WENT_WRONG = 400_001
    USER_NOT_FOUND = 400_002

    #BRANCH PERMISSION
    PERMISSION_DENIED_DRIVER = 400_040

    #USER
    USER_ALREADY_EXISTS = 400_060
    ALREADY_SUBMITTED = 400_061

    #INVALID
    INVALID_STATUS_ACCESSLOG= 400_080


def exception(exp_class, error_code, message) -> APIException:
    return exp_class(error_code, message)

def raise_error(error_code, message="Something went wrong."):
    raise CustomValidationError(error_code, message)


class ResponseSerializer(serializers.Serializer):
    error_code = serializers.CharField(max_length=7)
    message = serializers.CharField(max_length=100)


def resp(code, ser_class = ""):
    return {
        code: ser_class,
        400: ResponseSerializer()
    }


def send_me(message):
    try:
        token = os.getenv('BOT_TOKEN')
        chat_id = 887307931
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': message
        }
        requests.post(url=url, params=data)
    except Exception as e:
        print(f"Error while sending message to telegram: {e}")

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    error_details = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))

    if response is not None:
        return response
    if os.getenv('IS_SERVER'):
        send_me(f"OLX Test:\n{error_details}")
    # return Response(
    #     {
    #         "error_code": "500_500",
    #         "message": str(exc)
    #     },
    #     status=400
    # )

