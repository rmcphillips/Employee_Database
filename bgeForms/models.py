from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator
from employee.models import Employee
# Create your models here.


class FTE(models.Model):

    class Meta:
        verbose_name = ("FTE Form")
        verbose_name_plural = ("FTE Forms")

    start_time = models.DateTimeField(
        verbose_name="Start Time", auto_now_add=True)
    completion_time = models.DateTimeField(
        verbose_name="Completion Time", blank=True, null=True)
    rsm_email = models.EmailField(
        verbose_name="Email", max_length=50, blank=True)
    rsm_name = models.CharField(verbose_name="RSM Name",
                                max_length=100, blank=True)
    head_count_date = models.DateTimeField(
        verbose_name="Total Headcount on", auto_now=False, auto_now_add=False)
    fte = models.IntegerField(verbose_name="FTE", blank=False, validators=[
                              MinValueValidator(0)])
    total_active_selling = models.IntegerField(
        verbose_name="Total Active Selling",
        blank=False, validators=[MinValueValidator(0)])
    total_sales = models.IntegerField(
        verbose_name="Total Sales",
        blank=False, validators=[MinValueValidator(0)])
    group_sales_gas = models.IntegerField(
        verbose_name="Group Sales GAS",
        blank=False, validators=[MinValueValidator(0)])
    group_sales_electricity = models.IntegerField(
        verbose_name="Group Sales Electricity",
        blank=False, validators=[MinValueValidator(0)])
    induction_headcount = models.IntegerField(
        verbose_name="Induction",
        blank=False, validators=[MinValueValidator(0)])
    total_headcount = models.IntegerField(
        verbose_name="Active Including Induction",
        blank=True)
    total_calls = models.IntegerField(
        verbose_name="Total Calls",
        blank=False, validators=[MinValueValidator(0)])
    decision_makers_met_dmm = models.IntegerField(
        verbose_name="Decision Makers Met (DMM)",
        blank=False, validators=[MinValueValidator(0)])
    decision_makers_presented_dmp = models.IntegerField(
        verbose_name="Decision Makers Presented (DMP)",
        blank=False, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.rsm_name


sale_type_choices = (
    ("ELE", "Electricity Only"),
    ("NGAS", "New Gas Customer"),
    ("NDUAL", "New Dual Fuel Customer"),
)


class ProcessedPaperSales(models.Model):

    class Meta:
        verbose_name = ("Processed Paper Sales Form")
        verbose_name_plural = ("Processed Paper Sales Forms")

    sale_type = models.CharField(
        choices=sale_type_choices, max_length=100, verbose_name="Sale Type")
    mprn = models.CharField(max_length=1000,
                            blank=True, verbose_name="MPRN",
                            validators=[MinLengthValidator(11)],
                            help_text="For Electricity Only. You can enter\
                                 multiple MRPNs by separating them\
                                      by a white space.")
    gprn = models.CharField(max_length=1000,
                            blank=True, verbose_name="GPRN",
                            validators=[MinLengthValidator(7)],
                            help_text="For New Customer Gas Only. You can enter\
                                 multiple GRPNs by separating them\
                                      by a white space.")
    sales_agent = models.ForeignKey(
        Employee, on_delete=models.CASCADE, verbose_name="Agent")
    processor_name = models.CharField(verbose_name="Processor Name",
                                      max_length=100, blank=True)
    submitted_on = models.DateTimeField(verbose_name="Submission Date")
