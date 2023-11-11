from django.urls import path
from . import views

urlpatterns = [
    path("", views.budget, name="budget"),
    path("new", views.new_budget, name="new_budget"),
    path("calendar", views.calendar, name="calendar"),
    path("<int:year>/<int:month>/", views.budget, name="budget_by_month"),
    path("manage/<int:year>/<int:month>/", views.manage_budget, name="manage_budget"),
]