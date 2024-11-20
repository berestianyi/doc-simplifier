# Generated by Django 5.1.3 on 2024-11-10 15:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Bank Name')),
                ('mfo', models.CharField(blank=True, null=True, verbose_name='MFO')),
            ],
        ),
        migrations.CreateModel(
            name='BusinessEntities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_entity', models.CharField(choices=[('TOV', 'ТОВ'), ('FOP', 'ФОП')], default='FOP', max_length=3)),
                ('edrpou', models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='Code EDRPOU')),
                ('short_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Short Name')),
                ('full_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Full Name')),
                ('director_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Director Name')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='Address')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=200, null=True, verbose_name='Phone')),
                ('iban', models.CharField(blank=True, max_length=200, null=True, verbose_name='IBAN')),
                ('bank', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='business_entities', to='business_entities.bank')),
            ],
        ),
    ]