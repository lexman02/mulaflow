from django import forms
from budget.models import UserExpense

class UserExpenseForm(forms.ModelForm):
    class Meta:
        model = UserExpense
        fields = ['frequency', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }