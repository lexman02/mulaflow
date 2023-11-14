from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_budget, name="budget"),
    path("new", views.create_budget, name="new_budget"),
    path("calendar", views.get_calendar, name="calendar"),
    path("<int:year>/<int:month>/", views.get_budget, name="budget_by_month"),
    path("manage/<int:year>/<int:month>/", views.edit_budget, name="manage_budget"),
]