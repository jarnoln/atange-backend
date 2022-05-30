# Generated by Django 4.0.4 on 2022-05-21 03:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('collective', '0002_collective_creator_collective_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionnaireItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('order', models.IntegerField(blank=True, default=0, help_text='Determines the order between items at same level.')),
                ('item_type', models.CharField(choices=[('Q', 'Question'), ('H', 'Header')], default='Q', max_length=1)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('edited', models.DateTimeField(auto_now=True, null=True)),
                ('collective', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collective.collective')),
                ('creator', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='collective.questionnaireitem')),
            ],
        ),
    ]