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


class BudgetManager(models.Manager):
    def adjacent_budgets(self, user, year, month):
        prev_month = month - 1 if month > 1 else 12
        prev_year = year if month > 1 else year - 1
        next_month = month + 1 if month < 12 else 1
        next_year = year if month < 12 else year + 1

        try:
            next_budget = self.get(user=user, created__month=next_month, created__year=next_year)
        except Budget.DoesNotExist:
            next_budget = None

        try:
            prev_budget = self.get(user=user, created__month=prev_month, created__year=prev_year)
        except Budget.DoesNotExist:
            prev_budget = None

        return prev_budget, next_budget

    def current_budget_totals(self, user):
        budget = self.get(user=user)
        income, expenses = sum(item.amount for item in budget.income_sources.all()), sum(item.amount for item in budget.expenses.all())
        return {'income': income, 'expenses': expenses, 'surplus': income - expenses}


class Budget(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    income_sources = models.ManyToManyField(IncomeSource)
    expenses = models.ManyToManyField(UserExpense)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = BudgetManager()
