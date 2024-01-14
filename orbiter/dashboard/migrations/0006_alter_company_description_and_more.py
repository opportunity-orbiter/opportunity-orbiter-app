# Generated by Django 5.0 on 2024-01-14 14:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "dashboard",
            "0005_rename_experience_in_years_upper_end_job_maximal_experience_in_years_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="company",
            name="employee_count",
            field=models.PositiveBigIntegerField(),
        ),
    ]
