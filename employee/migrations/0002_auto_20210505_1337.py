# Generated by Django 3.0 on 2021-05-05 13:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attendancestatus',
            options={'verbose_name': 'Attendance Status', 'verbose_name_plural': 'Attendance Status'},
        ),
        migrations.AlterModelOptions(
            name='department',
            options={'verbose_name': 'Account/Department', 'verbose_name_plural': 'Accounts/Departments'},
        ),
        migrations.AlterModelOptions(
            name='employeeattendance',
            options={'verbose_name': 'Employee Attendance', 'verbose_name_plural': 'Employees Attendances'},
        ),
        migrations.AlterModelOptions(
            name='employeejobhistory',
            options={'verbose_name': 'Employee Job History', 'verbose_name_plural': 'Employees Job History'},
        ),
        migrations.AlterModelOptions(
            name='employeeleave',
            options={'verbose_name': 'Employee Leave', 'verbose_name_plural': 'Employee Leaves'},
        ),
        migrations.AlterModelOptions(
            name='jobrole',
            options={'verbose_name': 'Job Role', 'verbose_name_plural': 'Job Roles'},
        ),
        migrations.AlterModelOptions(
            name='leavestatus',
            options={'verbose_name': 'Leave Status', 'verbose_name_plural': 'Leave Status'},
        ),
        migrations.AlterModelOptions(
            name='subdepartment',
            options={'verbose_name': 'Sub Department', 'verbose_name_plural': 'Sub Departments'},
        ),
        migrations.AddField(
            model_name='employeeattendance',
            name='overtime_hours',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(8)], verbose_name='Overtime Hours'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='employee_status',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='employeeattendance',
            name='additional_hours_worked',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(8)], verbose_name='Additional Status Hours'),
        ),
        migrations.AlterField(
            model_name='employeeattendance',
            name='hours_worked',
            field=models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(8)], verbose_name='Hours'),
        ),
    ]