from django.test import TestCase
from django.utils import timezone
from .models import Debt
from .serializers import DebtSerializer
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import io

import uuid

class DebtModelTest(TestCase):

    def setUp(self):
        self.debt = Debt.objects.create(
            name='Pessoa teste',
            government_id='1234',
            email='teste@teste.com',
            debt_amount=500.0,
            debt_due_date=timezone.now().date(),
            debt_id=str(uuid.uuid4())
        )
        self.client = APIClient()
        self.url = 'http://localhost:8000/api/v1'

    def test_string_representation(self):
        debt = Debt.objects.create(
            name = self.debt.name,
            government_id = self.debt.government_id,
            email = self.debt.email,
            debt_amount = self.debt.debt_amount,
            debt_due_date = self.debt.debt_due_date,
            debt_id = self.debt.debt_id
        )
        expected_debt = debt.debt_id
        self.assertEqual(expected_debt, str(debt))

    def test_import_debts_with_invalid_url(self):
        csv_content = """Name,Government ID,Email,Debt Amount,Debt Due Date,Debt ID
        John Doe,123456789,john.doe@example.com,1000.0,2023-05-17,DEBT123456
        Jane Smith,987654321,jane.smith@example.com,2000.0,2023-06-17,DEBT654321"""
        
        csv_file = io.BytesIO(csv_content.encode('utf-8'))
        csv_file.name = 'debts.csv'
        
        self.url += '/import_debt'

        response = self.client.post(self.url, {'file': csv_file}, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_import_debts_with_invalid_method(self):
        csv_content = """Name,Government ID,Email,Debt Amount,Debt Due Date,Debt ID
        John Doe,123456789,john.doe@example.com,1000.0,2023-05-17,DEBT123456
        Jane Smith,987654321,jane.smith@example.com,2000.0,2023-06-17,DEBT654321"""
        
        csv_file = io.BytesIO(csv_content.encode('utf-8'))
        csv_file.name = 'debts.csv'
        
        self.url += '/import_debt'

        response = self.client.get(self.url, {'file': csv_file}, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_import_debts(self):
        csv_content = """Name,Government ID,Email,Debt Amount,Debt Due Date,Debt ID
        John Doe,123456789,john.doe@example.com,1000.0,2023-05-17,DEBT123456
        Jane Smith,987654321,jane.smith@example.com,2000.0,2023-06-17,DEBT654321"""
        
        csv_file = io.BytesIO(csv_content.encode('utf-8'))
        csv_file.name = 'debts.csv'
        
        self.url += '/import_debts'

        response = self.client.post(self.url, {'file': csv_file}, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_debts_first_page(self):
        self.url += '/debts'

        # Teste a primeira página de resultados
        response = self.client.get(self.url, {'page': 1})
        debts = Debt.objects.all()[:10]
        serializer = DebtSerializer(debts, many=True)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)
        self.assertEqual(len(response.json()), 1)
