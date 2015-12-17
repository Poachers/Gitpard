# coding: utf-8

from django.http import Http404
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    errors = []
    if response is not None:
        if isinstance(exc, ValidationError):
            if isinstance(response.data, list):
                for data in response.data:
                    error = {
                        "code": -1,
                        "message": u"Ошибка валидации",
                        "description": data
                    }
                    errors.append(error)
            elif isinstance(response.data, dict):
                for key in response.data:
                    description = response.data[key]
                    if isinstance(description, list):
                        description = description[0]
                    elif isinstance(description, dict):
                        if 'message' in description:
                            description = description['message']
                        else:
                            description = next(description.iteritems())[1]
                    error = {
                        "code": -1,
                        "message": u"Ошибка валидации",
                        "description": description
                    }
                    errors.append(error)
            response.data = {"error": errors}
        elif isinstance(exc, Http404):
            for key in response.data:
                error = {
                    "code": -2,
                    "message": u"Ресурс не найден",
                    "description": u"Данный ресурс не найден"
                }
                errors.append(error)
            response.data = {"error": errors}
    return response
