# Generated by Django 3.0 on 2021-12-08 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0024_employeeleave_has_deduction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeleave',
            name='has_deduction',
            field=models.BooleanField(
                default=False, verbose_name='Clawback/Deductions'),
        ),
    ]
