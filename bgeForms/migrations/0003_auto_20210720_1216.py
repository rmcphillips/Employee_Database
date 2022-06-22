# Generated by Django 3.0 on 2021-07-20 12:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgeForms', '0002_auto_20210720_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fte',
            name='decision_makers_met_dmm',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Decision Makers Met (DMM)'),
        ),
        migrations.AlterField(
            model_name='fte',
            name='decision_makers_presented_dmp',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Decision Makers Presented (DMP)'),
        ),
        migrations.AlterField(
            model_name='fte',
            name='fte',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='FTE'),
        ),
        migrations.AlterField(
            model_name='fte',
            name='group_sales_gas',
            field=models.IntegerField(blank=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Group Sales GAS'),
        ),
        migrations.AlterField(
            model_name='fte',
            name='induction_headcount',
            field=models.IntegerField(blank=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Induction'),
        ),
        migrations.AlterField(
            model_name='fte',
            name='total_active_electricity',
            field=models.IntegerField(blank=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Group Sales Electricity'),
        ),
        migrations.AlterField(
            model_name='fte',
            name='total_active_selling',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Total Active Selling'),
        ),
        migrations.AlterField(
            model_name='fte',
            name='total_calls',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Total Calls'),
        ),
        migrations.AlterField(
            model_name='fte',
            name='total_headcount',
            field=models.IntegerField(blank=True, verbose_name='Active Including Induction'),
        ),
        migrations.AlterField(
            model_name='fte',
            name='total_sales',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Total Sales'),
        ),
    ]