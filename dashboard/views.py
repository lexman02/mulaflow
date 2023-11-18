import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from budget.models import Budget


@login_required
def get_dashboard(request):
    current_date = datetime.date.today()
    # Get the authenticated user's budget for the current month, assuming your logic to retrieve it
    try:
        # Query the Budget model to get the user's budget for the current month
        budget = Budget.objects.get(user=request.user.id, created__month=current_date.month,
                                    created__year=current_date.year)

        budget_totals = Budget.objects.current_budget_totals(request.user)

        context = {
            'budget': budget,
            'budget_totals': budget_totals,
        }

        return render(request, 'dashboard.html', context)

    except Budget.DoesNotExist:
        # Handle the case where no budget exists for the current month
        return redirect('new_budget')
