from .views import ping

from django.urls import path

from debt.views import import_debts, list_debts, clean_debts

app_name = 'api'

urlpatterns = [
    path('ping', ping, name='ping'),

    path('debts', list_debts, name='debts'),
    path('import_debts', import_debts, name='import_debts'),
    path('clean_debts', clean_debts, name='clean_debts'),
]
