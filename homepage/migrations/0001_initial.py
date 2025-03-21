# Generated by Django 5.1.6 on 2025-03-15 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Feedback",
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
                ("name", models.CharField(max_length=100, verbose_name="Your Name")),
                ("email", models.EmailField(max_length=254, verbose_name="Your Email")),
                ("message", models.TextField(verbose_name="Your Feedback")),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Submission Time"
                    ),
                ),
            ],
            options={
                "verbose_name": "User Feedback",
                "verbose_name_plural": "User Feedbacks",
            },
        ),
    ]
