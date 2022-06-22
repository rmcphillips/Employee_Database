# Generated by Django 3.0 on 2021-07-21 16:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgeForms', '0007_auto_20210721_1536'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='processedpapersales',
            options={'verbose_name': 'Processed Paper Sales Form', 'verbose_name_plural': 'Processed Paper Sales Forms'},
        ),
        migrations.AlterField(
            model_name='processedpapersales',
            name='gprn',
            field=models.IntegerField(blank=True, validators=[django.core.validators.MinLengthValidator(7)], verbose_name='GPRN'),
        ),
        migrations.AlterField(
            model_name='processedpapersales',
            name='mprn',
            field=models.IntegerField(blank=True, validators=[django.core.validators.MinLengthValidator(11)], verbose_name='MPRN'),
        ),
    ]