from django.urls import path
from . import views

urlpatterns = [
    path("", views.budget, name="budget"),
    path("new", views.new_budget, name="new_budget"),
]