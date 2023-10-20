from django.contrib import admin
from .models import Budget, IncomeSource, CommonExpense, UserExpense

class CommonExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'frequency')

admin.site.register(CommonExpense, CommonExpenseAdmin)