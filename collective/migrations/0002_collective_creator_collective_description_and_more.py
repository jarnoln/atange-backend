# Generated by Django 4.0.4 on 2022-04-26 03:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("collective", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="collective",
            name="creator",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="collective",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="collective",
            name="is_visible",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="collective",
            name="name",
            field=models.SlugField(max_length=100),
        ),
    ]
