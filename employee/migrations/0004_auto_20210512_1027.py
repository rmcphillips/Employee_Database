# Generated by Django 3.0 on 2021-05-12 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_employee_eircode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='employee_status',
            field=models.CharField(blank=True, default='Active', max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='EmployeeDocuments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.ImageField(blank=True, null=True, upload_to='')),
                ('upload_date', models.DateField(auto_now_add=True)),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='employee.Employee')),
            ],
            options={
                'verbose_name': 'Employee Documents',
                'verbose_name_plural': 'Employees Documents',
            },
        ),
    ]
