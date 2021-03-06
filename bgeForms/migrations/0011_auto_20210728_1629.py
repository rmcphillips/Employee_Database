# Generated by Django 3.0 on 2021-07-28 16:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgeForms', '0010_auto_20210722_1325'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fte',
            old_name='total_active_electricity',
            new_name='group_sales_electricity',
        ),
        migrations.AlterField(
            model_name='processedpapersales',
            name='gprn',
            field=models.CharField(blank=True, help_text='For New Customer Gas Only. You can enter                                 multiple GRPNs by separating them                                      by a white space.', max_length=1000, validators=[django.core.validators.MinLengthValidator(7)], verbose_name='GPRN'),
        ),
        migrations.AlterField(
            model_name='processedpapersales',
            name='mprn',
            field=models.CharField(blank=True, help_text='For Electricity Only. You can enter                                 multiple MRPNs by separating them                                      by a white space.', max_length=1000, validators=[django.core.validators.MinLengthValidator(11)], verbose_name='MPRN'),
        ),
    ]
