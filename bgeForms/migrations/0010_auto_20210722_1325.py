# Generated by Django 3.0 on 2021-07-22 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgeForms', '0009_auto_20210721_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processedpapersales',
            name='submitted_on',
            field=models.DateTimeField(verbose_name='Submission Date'),
        ),
    ]
