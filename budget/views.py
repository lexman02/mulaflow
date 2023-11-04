import datetime

from django.shortcuts import render, redirect
from budget.models import Budget, IncomeSource, UserExpense, CommonExpense
from budget.forms import UserExpenseForm


# Create your views here.
def budget(request):
    current_date = datetime.date.today()
    try:
        cur_budget = Budget.objects.get(user=request.user.id,
                                        created__month=current_date.month,
                                        created__year=current_date.year)

        context = {
            'budget': cur_budget,
        }
    except Budget.DoesNotExist:
        context = {
            'budget': None,
        }

    return render(request, 'budget.html', context)


def new_budget(request):
    if request.method == 'POST':
        income_sources = []
        expenses = []

        form = UserExpenseForm(request.POST)

        if form.is_valid():
            income_source_count = int(request.POST.get('incomeSourceCount', 0))
            expense_count = int(request.POST.get('expenseCount', 0))

            for i in range(1, income_source_count + 1):
                income_source_name = request.POST.get(f'income_source_name_{i}')
                income_source_amount = int(request.POST.get(f'income_source_amount_{i}'))
                # Validate and create IncomeSource instances
                if income_source_name and income_source_amount:
                    income_sources.append({
                        'name': income_source_name,
                        'amount': income_source_amount,
                    })

            for i in range(1, expense_count + 1):
                expense_name = request.POST.get(f'expense_name_{i}')
                expense_amount = int(request.POST.get(f'expense_amount_{i}'))
                expense_frequency = form.cleaned_data['frequency']
                expense_due_date = form.cleaned_data['due_date']
                # Validate and create Expense instances
                if expense_name and expense_amount:
                    expenses.append({
                        'name': expense_name,
                        'amount': expense_amount,
                        'frequency': expense_frequency,
                        'due_date': expense_due_date,
                    })

            print(income_sources)
            print(expenses)

            budget, created = Budget.objects.get_or_create(user=request.user)

            for source_data in income_sources:
                income_source = IncomeSource.objects.create(user=request.user, **source_data)
                budget.income_sources.add(income_source)
                budget.total_monthly_income += source_data['amount']

            for expense_data in expenses:
                expense = UserExpense.objects.create(user=request.user, **expense_data)
                budget.expenses.add(expense)
                budget.total_monthly_expenses += expense_data['amount']

            budget.surplus = budget.total_monthly_income - budget.total_monthly_expenses
            budget.save()
    else:
        form = UserExpenseForm()

    context = {
        'form': form,
        'common_expenses': CommonExpense.objects.filter(is_common=True),
    }

    return render(request, 'new_budget.html', context)

