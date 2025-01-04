# Generated by Django 5.1.3 on 2024-12-29 21:54

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
    ]
