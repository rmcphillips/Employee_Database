# Generated by Django 3.0 on 2021-09-02 14:40

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employee', '0019_auto_20210818_1035'),
        ('inventory', '0004_auto_20210902_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='phone',
            name='transit',
            field=models.BooleanField(null=True, verbose_name='In Transit'),
        ),
        migrations.AddField(
            model_name='sim',
            name='transit',
            field=models.BooleanField(null=True, verbose_name='In Transit'),
        ),
        migrations.AlterField(
            model_name='phone',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='employee.Employee', verbose_name='Assign to Employee'),
        ),
        migrations.AlterField(
            model_name='phone',
            name='sim',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.SIM', validators=[django.core.validators.MinLengthValidator(16)], verbose_name='SIM'),
        ),
        migrations.AlterField(
            model_name='phone',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('broken', 'Broken'), ('repair', 'Repair')], max_length=20, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='sim',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='employee.Employee', verbose_name='Assign to Employee'),
        ),
        migrations.AlterField(
            model_name='sim',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('broken', 'Broken'), ('repair', 'Repair')], max_length=20, verbose_name='Status'),
        ),
        migrations.CreateModel(
            name='Tablet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('serial_number', models.CharField(max_length=255, unique=True, verbose_name='Serial Number')),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('broken', 'Broken'), ('repair', 'Repair')], max_length=20, verbose_name='Status')),
                ('location', models.CharField(choices=[('cec1', 'CEC-1'), ('cec2', 'CEC-2'), ('field', 'Field'), ('galway', 'Galway'), ('other', 'Other')], max_length=20, null=True, verbose_name='Location')),
                ('damaged', models.BooleanField(null=True, verbose_name='Damaged')),
                ('transit', models.BooleanField(null=True, verbose_name='In Transit')),
                ('tablet_name', models.CharField(max_length=255, verbose_name='Tablet Name')),
                ('imei', models.CharField(max_length=16, unique=True, validators=[django.core.validators.MinLengthValidator(14), django.core.validators.MaxLengthValidator(16)], verbose_name='IMEI')),
                ('brand', models.CharField(max_length=255, verbose_name='Brand')),
                ('model', models.CharField(max_length=255, verbose_name='Model')),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='employee.Employee', verbose_name='Assign to Employee')),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('sim', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.SIM', validators=[django.core.validators.MinLengthValidator(16)], verbose_name='SIM')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]