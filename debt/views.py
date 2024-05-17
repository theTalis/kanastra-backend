from rest_framework import status
from django.http import JsonResponse
from .models import Debt
from django.core.paginator import Paginator
from django.core import serializers
from .serializers import DebtSerializer

from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt

import json

@csrf_exempt
@action(methods=['post'], detail=True)
def import_debts(request):
    file = request.FILES['file']
    content = file.read()

    debts = []
    count = 0

    lines = content.splitlines()
    for line in lines:
        if count > 7:
            line = line.decode("utf-8")
            items = line.split(',')

            debts.append(
                Debt(name=items[0],
                government_id=items[1],
                email=items[2],
                debt_amount=items[3],
                debt_due_date=items[4],
                debt_id=items[5])
            )
        count += 1
        
    Debt.objects.bulk_create(debts)
    return JsonResponse('Dados importados com sucesso', status=status.HTTP_201_CREATED, safe=False)

@csrf_exempt
@action(methods=['get'], detail=True)
def list_debts(request):
    debts = list(Debt.objects.all())
    paginator = Paginator(debts, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    serializer = DebtSerializer(page_obj, many=True)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
@action(methods=['get'], detail=True)
def clean_debts(request):
    Debt.objects.all().delete()
    return JsonResponse('Dados excluidos com sucesso', status=status.HTTP_204_NO_CONTENT, safe=False)
