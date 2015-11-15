from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    error = {}

    if response is not None:
        error["code"] = response.status_code
        error["message"] = response.status_text
        error["description"] = response.data
        response.data = {"error": error}

    return response