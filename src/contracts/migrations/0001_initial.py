# Generated by Django 5.1.3 on 2024-11-10 15:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('business_entities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Templates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('type', models.CharField(blank=True, choices=[('ATP', 'АТП'), ('OFFICE', 'Офіс')], default='ATP', max_length=100, null=True)),
                ('path', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contracts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('business_entities', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='business_entities.businessentities')),
                ('template', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contracts.templates')),
            ],
        ),
    ]