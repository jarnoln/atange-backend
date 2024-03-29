# Generated by Django 4.1.6 on 2023-03-20 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("collective", "0013_alter_usergroup_collective_name_alter_usergroup_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="GlobalSettings",
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
                (
                    "title",
                    models.CharField(blank=True, default="Atange", max_length=250),
                ),
                ("one_collective", models.BooleanField(blank=True, default=False)),
                (
                    "users_can_create_collectives",
                    models.BooleanField(blank=True, default=False),
                ),
                ("require_names", models.BooleanField(blank=True, default=False)),
            ],
        ),
    ]
