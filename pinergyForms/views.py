from pinergyForms.models import CECDisplay
from django.shortcuts import render
from .forms import CECDisplayForm
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib import messages

# Create your views here.


def cecDisplayForm(request):

    form = CECDisplayForm()

    if request.method == "POST":
        form = CECDisplayForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Entry updated successfully.")

    context = {
        "form": form
    }

    return render(request, "pinergyForms/cecDisplayForm.html", context)


def cecDisplay(request):

    salesB2BQ = CECDisplay.objects.filter(
        entry_type="salesB2B").order_by("entry_date").last()

    salesB2CQ = CECDisplay.objects.filter(
        entry_type="salesB2C").order_by("entry_date").last()

    retentionQ = CECDisplay.objects.filter(
        entry_type="retention").order_by("entry_date").last()

    currentSalesB2B = salesB2BQ.current
    targetSalesB2B = salesB2BQ.target

    currentSalesB2C = salesB2CQ.current
    targetSalesB2C = salesB2CQ.target

    currentRetention = retentionQ.current
    targetRetention = retentionQ.target

    context = {
        "currentSalesB2B": currentSalesB2B,
        "targetSalesB2B": targetSalesB2B,
        "currentSalesB2C": currentSalesB2C,
        "targetSalesB2C": targetSalesB2C,
        "currentRetention": currentRetention,
        "targetRetention": targetRetention
    }

    return render(request, "pinergyForms/cecDisplay.html", context)


class getChartData(APIView):

    def get(self, request, format=None):
        salesB2BQ = CECDisplay.objects.filter(
            entry_type="salesB2B").order_by("entry_date").last()

        salesB2CQ = CECDisplay.objects.filter(
            entry_type="salesB2C").order_by("entry_date").last()

        retentionQ = CECDisplay.objects.filter(
            entry_type="retention").order_by("entry_date").last()

        currentSalesB2B = salesB2BQ.current
        targetSalesB2B = salesB2BQ.target

        currentSalesB2C = salesB2CQ.current
        targetSalesB2C = salesB2CQ.target

        currentRetention = retentionQ.current
        targetRetention = retentionQ.target

        salesB2B = [
            currentSalesB2B,
            targetSalesB2B,
        ]

        salesB2C = [
            currentSalesB2C,
            targetSalesB2C,
        ]

        retention = [
            currentRetention,
            targetRetention
        ]

        data = {
            "salesB2B": salesB2B,
            "salesB2C": salesB2C,
            "retention": retention
        }
        return Response(data)
