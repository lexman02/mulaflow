import datetime
import json
import uuid

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from budget.models import Budget, IncomeSource, UserExpense, CommonExpense
from budget.forms import UserExpenseForm, IncomeSourceForm


# Get the budget view for the current month
@login_required
def get_budget(request, year=None, month=None):
    if year and month:
        target_date = datetime.date(year, month, 1)
    else:
        target_date = datetime.date.today()
        year = target_date.year
        month = target_date.month

    try:
        cur_budget = Budget.objects.get(user=request.user,
                                        created__month=month,
                                        created__year=year)

        prev_budget, next_budget = Budget.objects.adjacent_budgets(request.user, year, month)

        budget_totals = Budget.objects.current_budget_totals(request.user)

        context = {
            'budget': cur_budget,
            'year': year,
            'month': month,
            'next_budget': True if next_budget else False,
            'prev_budget': True if prev_budget else False,
            'budget_totals': budget_totals,
        }
    except Budget.DoesNotExist:
        redirect('new_budget')

    return render(request, 'budget.html', context)


# Get the calendar view for the current month
@login_required
def get_calendar(request, year=None, month=None):
    if year and month:
        target_date = datetime.date(year, month, 1)
    else:
        target_date = datetime.date.today()
        year = target_date.year
        month = target_date.month

    try:
        cur_budget = Budget.objects.get(user=request.user,
                                        created__month=target_date.month,
                                        created__year=target_date.year)

        prev_budget, next_budget = Budget.objects.adjacent_budgets(request.user, year, month)

        events = []

        for expense in cur_budget.expenses.all():
            events.append({
                'title': expense.name,
                'date': expense.due_date,
            })

        context = {
            'events': events,
            'year': year,
            'month': month,
            'next_budget': True if next_budget else False,
            'prev_budget': True if prev_budget else False,
        }
    except Budget.DoesNotExist:
        redirect('new_budget')

    return render(request, 'calendar.html', context)


# Create a new budget (add income sources and expenses)
@login_required
def create_budget(request):
    user_expense_form = None
    income_source_form = None

    if request.method == 'POST':
        income_sources = []
        expenses = []

        income_source_count = int(request.POST.get('incomeSourceCount', 0))
        expense_count = int(request.POST.get('expenseCount', 0))

        for i in range(0, income_source_count):
            income_source_name = request.POST.get(f'income_source_name_{i}')
            income_source_amount = int(request.POST.get(f'income_source_amount_{i}'))
            # Validate and create IncomeSource instances
            if income_source_name and income_source_amount:
                income_sources.append({
                    'name': income_source_name,
                    'amount': income_source_amount,
                })

        for i in range(0, expense_count):
            expense_name = request.POST.get(f'expense_name_{i}')
            expense_amount = int(request.POST.get(f'expense_amount_{i}'))
            expense_frequency = request.POST.get(f'expense_frequency_{i}')
            expense_due_date = request.POST.get(f'expense_due_date_{i}')
            # Validate and create Expense instances
            if expense_name and expense_amount:
                expenses.append({
                    'name': expense_name,
                    'amount': expense_amount,
                    'frequency': expense_frequency,
                    'due_date': expense_due_date,
                })

        budget, created = Budget.objects.get_or_create(user=request.user)
        if not created:
            return redirect('budget')

        for source_data in income_sources:
            income_source = IncomeSource.objects.create(user=request.user, **source_data)
            budget.income_sources.add(income_source)

        for expense_data in expenses:
            expense = UserExpense.objects.create(user=request.user, **expense_data)
            budget.expenses.add(expense)

        budget.save()

        return redirect('budget')
    else:
        user_expense_form = UserExpenseForm()
        income_source_form = IncomeSourceForm()

    context = {
        'user_expense_form': user_expense_form,
        'income_source_form': income_source_form,
        'common_expenses': CommonExpense.objects.filter(is_common=True),
    }

    return render(request, 'new_budget.html', context)


# Edit a current budget (add, remove, update income sources and expenses)
@login_required
def edit_budget(request, year, month):
    budget = Budget.objects.get(user=request.user, created__month=month, created__year=year)

    if request.method == 'POST':
        income_sources = []
        expenses = []

        income_source_count = int(request.POST.get('incomeSourceCount', 0))
        expense_count = int(request.POST.get('expenseCount', 0))
        deleted_income_sources = json.loads(request.POST.get('deletedIncomeSources'))
        deleted_expenses = json.loads(request.POST.get('deletedExpenses'))

        if deleted_income_sources:
            for income_source_id in deleted_income_sources:
                IncomeSource.objects.delete(id=income_source_id)

        if deleted_expenses:
            for expense_id in deleted_expenses:
                UserExpense.objects.delete(id=expense_id)

        for i in range(0, income_source_count):
            income_source_id = request.POST.get(f'income_source_id_{i}')
            income_source_name = request.POST.get(f'income_source_name_{i}')
            income_source_amount = int(request.POST.get(f'income_source_amount_{i}'))

            if income_source_id == '':
                income_source_id = uuid.uuid4()

            # Validate and create IncomeSource instances
            if income_source_name and income_source_amount:
                income_sources.append({
                    'id': income_source_id,
                    'name': income_source_name,
                    'amount': income_source_amount,
                })

        for i in range(0, expense_count):
            expense_id = request.POST.get(f'expense_id_{i}')
            expense_name = request.POST.get(f'expense_name_{i}')
            expense_amount = int(request.POST.get(f'expense_amount_{i}'))
            expense_frequency = request.POST.get(f'expense_frequency_{i}')
            expense_due_date = request.POST.get(f'expense_due_date_{i}')

            if expense_id == '':
                expense_id = uuid.uuid4()

            # Validate and create Expense instances
            if expense_name and expense_amount and expense_frequency and expense_due_date:
                expenses.append({
                    'id': expense_id,
                    'name': expense_name,
                    'amount': expense_amount,
                    'frequency': expense_frequency,
                    'due_date': expense_due_date,
                })

        for income_source_data in income_sources:
            income_source, created = IncomeSource.objects.update_or_create(user=request.user, **income_source_data)
            if created:
                budget.income_sources.add(income_source)

        for expense_data in expenses:
            expense, created = UserExpense.objects.update_or_create(user=request.user, **expense_data)
            if created:
                budget.expenses.add(expense)

        budget.save()

        if year == datetime.date.today().year and month == datetime.date.today().month:
            return redirect('budget')

        return redirect('budget_by_month', year=year, month=month)
    else:
        income_source_form = IncomeSourceForm()
        user_expense_form = UserExpenseForm()

    context = {
        'budget': budget,
        'income_source_form': income_source_form,
        'user_expense_form': user_expense_form,
        'common_expenses': CommonExpense.objects.filter(is_common=True),
    }
    return render(request, 'manage_budget.html', context)
