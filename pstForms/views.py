from pstForms.models import CECDisplay
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

    return render(request, "pstForms/cecDisplayForm.html", context)


def cecDisplay(request):

    salesQ = CECDisplay.objects.filter(
        entry_type="sales").order_by("entry_date").last()

    retentionQ = CECDisplay.objects.filter(
        entry_type="retention").order_by("entry_date").last()

    currentSales = salesQ.current
    targetSales = salesQ.target

    currentRetention = retentionQ.current
    targetRetention = retentionQ.target

    context = {
        "currentSales": currentSales,
        "targetSales": targetSales,
        "currentRetention": currentRetention,
        "targetRetention": targetRetention
    }

    return render(request, "pstForms/cecDisplay.html", context)


class getChartData(APIView):

    def get(self, request, format=None):
        salesQ = CECDisplay.objects.filter(
            entry_type="sales").order_by("entry_date").last()

        retentionQ = CECDisplay.objects.filter(
            entry_type="retention").order_by("entry_date").last()

        currentSales = salesQ.current
        targetSales = salesQ.target

        currentRetention = retentionQ.current
        targetRetention = retentionQ.target

        sales = [
            currentSales,
            targetSales,
        ]

        retention = [
            currentRetention,
            targetRetention
        ]

        data = {
            "sales": sales,
            "retention": retention
        }
        return Response(data)
