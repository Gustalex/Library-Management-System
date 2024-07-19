from datetime import datetime

from rest_framework.response import Response


def return_response(request, status, data):
    print(
        '[' + datetime.now().strftime('%d/%m/%Y %H:%M:%S') + ']',
        request.method,
        request.get_full_path(),
        status,
    )
    return Response(data, status=status)
