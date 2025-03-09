# Generated by Django 4.2.16 on 2025-03-07 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("records", "0003_remove_menstrualrecord_menstrual_symptoms_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="menstrualrecord",
            name="menstrual_symptoms",
            field=models.JSONField(
                blank=True, default=list, verbose_name="Menstrual Symptoms"
            ),
        ),
        migrations.AddField(
            model_name="menstrualrecord",
            name="post_menstrual_symptoms",
            field=models.JSONField(
                blank=True, default=list, verbose_name="Post-menstrual Symptoms"
            ),
        ),
        migrations.AddField(
            model_name="menstrualrecord",
            name="pre_menstrual_symptoms",
            field=models.JSONField(
                blank=True, default=list, verbose_name="Pre-menstrual Symptoms"
            ),
        ),
        migrations.AlterField(
            model_name="menstrualrecord",
            name="clotting",
            field=models.CharField(
                choices=[
                    ("none", "None"),
                    ("small", "Few Small Clots"),
                    ("large", "Many or Large Clots"),
                ],
                default="none",
                max_length=10,
                verbose_name="Clotting",
            ),
        ),
        migrations.AlterField(
            model_name="menstrualrecord",
            name="mood_swings",
            field=models.CharField(
                choices=[
                    ("none", "None"),
                    ("mild", "Mild"),
                    ("moderate", "Moderate"),
                    ("severe", "Severe"),
                ],
                default="none",
                max_length=10,
                verbose_name="Mood Swings",
            ),
        ),
        migrations.AlterField(
            model_name="menstrualrecord",
            name="stress_level",
            field=models.CharField(
                choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")],
                default="medium",
                max_length=10,
                verbose_name="Stress Level",
            ),
        ),
    ]
