# Generated by Django 5.1.6 on 2025-03-10 02:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_alter_userprofile_nickname"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="commented_posts",
        ),
    ]
