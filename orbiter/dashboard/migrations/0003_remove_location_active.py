# Generated by Django 5.0 on 2024-01-14 10:44

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0002_alter_company_business_fields_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="location",
            name="active",
        ),
    ]
