# Generated by Django 5.0 on 2023-12-29 21:18

import django.db.models.deletion
import orbiter.laboratory.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("laboratory", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ToDoList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="ToDoItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                (
                    "due_date",
                    models.DateTimeField(
                        default=orbiter.laboratory.models.one_week_hence
                    ),
                ),
                (
                    "todo_list",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="laboratory.todolist",
                    ),
                ),
            ],
            options={
                "ordering": ["due_date"],
            },
        ),
    ]
