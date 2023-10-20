import datetime

from django.shortcuts import render

from .models import Budget


# Create your views here.
def index(request):
    current_date = datetime.date.today()
    try:
        cur_budget = Budget.objects.get(user=request.user.id,
                                        created__month=current_date.month,
                                        created__year=current_date.year)

        total_monthly_income = cur_budget.total_monthly_income
        total_monthly_expenses = cur_budget.total_monthly_expenses
        surplus = cur_budget.surplus

        context = {
            'budget': cur_budget,
            'total_monthly_income': total_monthly_income,
            'total_monthly_expenses': total_monthly_expenses,
            'surplus': surplus,
        }
    except Budget.DoesNotExist:
        context = {
            'budget': None,
            'total_monthly_income': 0,
            'total_monthly_expenses': 0,
            'surplus': 0,
        }

    return render(request, 'index.html', context)
