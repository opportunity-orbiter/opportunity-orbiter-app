# Generated by Django 4.2.2 on 2023-07-10 18:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_avatars"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.ImageField(
                blank=True, null=True, upload_to="avatars/", verbose_name="avatar"
            ),
        ),
        migrations.AlterField(
            model_name="userfeedback",
            name="email",
            field=models.EmailField(blank=True, max_length=254, verbose_name="email"),
        ),
        migrations.AlterField(
            model_name="userfeedback",
            name="text",
            field=models.TextField(verbose_name="text"),
        ),
    ]
