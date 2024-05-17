from django.db import models

class Debt(models.Model):
    class Meta:
        db_table = 'debt'
    name = models.CharField(max_length=200)
    government_id = models.CharField(max_length=50)
    email = models.CharField(max_length=200)
    debt_amount = models.FloatField()
    debt_due_date = models.DateField()
    debt_id = models.CharField(max_length=300)
    
    def __str__(self):
        return self.debt_id
