import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from budget.models import Budget


@login_required
def get_dashboard(request):
    expenses = []
    totals_by_month = {}
    current_date = datetime.date.today().replace(day=15)

    # Get the authenticated user's budget for the current month
    try:
        # Query the Budget model to get the user's budget for the current month
        current_budget = Budget.objects.get(user=request.user.id, created__month=current_date.month,
                                            created__year=current_date.year)

        # Order the expenses by due date moving the ones without a due date or that have passed to the end
        for expense in current_budget.expenses.all():
            if expense.due_date < current_date:
                expenses.append(expense)
            else:
                expenses.insert(0, expense)

        all_budgets = Budget.objects.filter(user=request.user.id)
        for budget in all_budgets:
            totals_by_month.update({budget.created.strftime('%B'): Budget.objects.current_budget_totals(budget)})

        context = {
            'expenses': expenses,
            'today': {
                'date': current_date,
                'totals': totals_by_month[current_date.strftime('%B')]
            },
            'totals_by_month': {
                'months': [month for month in totals_by_month],
                'surplus': [totals_by_month[month]['surplus'] for month in totals_by_month],
                'income': [totals_by_month[month]['income'] for month in totals_by_month],
                'expenses': [totals_by_month[month]['expenses'] for month in totals_by_month],
            },
        }
        print(context['totals_by_month']['surplus'])

        return render(request, 'dashboard.html', context)

    except Budget.DoesNotExist:
        # Handle the case where no budget exists for the current month
        return redirect('new_budget')
