import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from budget.models import Budget


@login_required
def get_dashboard(request):
    expenses = []
    current_date = datetime.date.today().replace(day=15)

    # Get the authenticated user's budget for the current month
    try:
        # Query the Budget model to get the user's budget for the current month
        budget = Budget.objects.get(user=request.user.id, created__month=current_date.month,
                                    created__year=current_date.year)

        budget_totals = Budget.objects.current_budget_totals(request.user)

        # Order the expenses by due date moving the ones without a due date or that have passed to the end
        for expense in budget.expenses.all():
            if expense.due_date < current_date:
                expenses.append(expense)
            else:
                expenses.insert(0, expense)

        context = {
            'expenses': expenses,
            'today': current_date,
            'budget_totals': budget_totals,
        }

        return render(request, 'dashboard.html', context)

    except Budget.DoesNotExist:
        # Handle the case where no budget exists for the current month
        return redirect('new_budget')
