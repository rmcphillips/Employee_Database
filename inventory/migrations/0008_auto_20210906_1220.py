# Generated by Django 3.0 on 2021-09-06 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_auto_20210906_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phone',
            name='sim',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.SIM', verbose_name='SIM'),
        ),
    ]
