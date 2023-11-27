# Generated by Django 4.2.7 on 2023-11-20 07:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("budget", "0005_remove_budget_surplus_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="budget",
            name="created",
            field=models.DateField(default=datetime.date(2023, 11, 20)),
        ),
        migrations.AlterField(
            model_name="budget",
            name="updated",
            field=models.DateField(auto_now=True),
        ),
    ]