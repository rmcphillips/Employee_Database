# Generated by Django 3.0 on 2021-06-14 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0006_auto_20210609_1648'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employeeattendance',
            options={'ordering': ['attendance_date'], 'verbose_name': 'Employee Attendance', 'verbose_name_plural': 'Employees Attendances'},
        ),
        migrations.AddField(
            model_name='employeeattendance',
            name='modified_by',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='employeeattendance',
            name='modified_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='employeeattendance',
            name='notes',
            field=models.TextField(blank=True, max_length=900, null=True, verbose_name='Additional Notes'),
        ),
    ]