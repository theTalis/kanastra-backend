from rest_framework import status
from django.http import JsonResponse

def ping(request):
    return JsonResponse('OK', status=status.HTTP_200_OK, safe=False)