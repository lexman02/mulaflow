# Generated by Django 4.2.7 on 2023-11-20 07:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("budget", "0006_alter_budget_created_alter_budget_updated"),
    ]

    operations = [
        migrations.AlterField(
            model_name="budget",
            name="created",
            field=models.DateField(default=datetime.date.today),
        ),
    ]
