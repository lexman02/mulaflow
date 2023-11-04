import uuid

from django.contrib.auth.models import User
from django.db import models


class IncomeSource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class Expense(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    FREQUENCY_CHOICES = [
        ('d', 'Daily'),
        ('w', 'Weekly'),
        ('m', 'Monthly'),
        ('q', 'Quarterly'),
        ('y', 'Yearly'),
    ]

    frequency = models.CharField(
        max_length=1,
        choices=FREQUENCY_CHOICES,
        default='m',
        help_text='Frequency of expense'
    )

    class Meta:
        abstract = True


class CommonExpense(Expense):
    service_provider = models.CharField(max_length=255, default='None')
    tier = models.CharField(max_length=255, null=True, blank=True)
    is_common = models.BooleanField(default=True, editable=False)


class UserExpense(Expense):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateField(null=True, blank=True)


class Budget(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    income_sources = models.ManyToManyField(IncomeSource)
    expenses = models.ManyToManyField(UserExpense)
    total_monthly_income = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_monthly_expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    surplus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
