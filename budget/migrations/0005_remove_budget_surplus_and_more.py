# Generated by Django 4.2.7 on 2023-11-14 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("budget", "0004_alter_incomesource_id_alter_userexpense_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="budget",
            name="surplus",
        ),
        migrations.RemoveField(
            model_name="budget",
            name="total_monthly_expenses",
        ),
        migrations.RemoveField(
            model_name="budget",
            name="total_monthly_income",
        ),
    ]
