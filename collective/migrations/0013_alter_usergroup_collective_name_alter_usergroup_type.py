# Generated by Django 4.1.6 on 2023-03-09 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("collective", "0012_usergroup_collective_name_usergroup_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usergroup",
            name="collective_name",
            field=models.SlugField(blank=True, default=None, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="usergroup",
            name="type",
            field=models.SlugField(blank=True, default=None, max_length=250, null=True),
        ),
    ]