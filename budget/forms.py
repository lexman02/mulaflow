from django import forms
from budget.models import UserExpense, IncomeSource


class IncomeSourceForm(forms.ModelForm):
    class Meta:
        model = IncomeSource
        fields = ['name', 'amount']


class UserExpenseForm(forms.ModelForm):
    class Meta:
        model = UserExpense
        fields = ['name', 'amount', 'frequency', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }