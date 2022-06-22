from bgeForms.forms import FTEForm, ProcessedPaperSalesForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from datetime import date

# Create your views here.


def userHasAccess(user):
    if (user.department.department_name == "Bord Gais" or
            user.is_superuser):
        return True
    else:
        return False


@login_required
@user_passes_test(userHasAccess,
                  login_url="/dashboard/",
                  redirect_field_name=None)
def form_list(request):
    """Render a list with all available forms."""

    return render(request, "bgeForms/formsList.html")


@login_required
def fte_form(request):
    """Renders a FTE form."""

    form = FTEForm()

    if request.method == "POST":
        form = FTEForm(request.POST)

        if form.is_valid():
            total_headcount = 0
            form.save(commit=False)

            total_headcount = form.instance.induction_headcount + \
                form.instance.total_active_selling

            form.instance.rsm_name = request.user.__str__()
            form.instance.rsm_email = request.user.email
            form.instance.completion_time = date.today()
            form.instance.total_headcount = total_headcount
            form.save()
            messages.success(request, "Form submitted successfully.")
            return redirect("/bgeForms/")

        else:
            messages.error(
                request, """Something went wrong. If the problem
                    persists contact support.""")

    context = {
        "form": form
    }

    return render(request, "bgeForms/FTEForm.html", context)


@login_required
def processed_paper_sales_form(request):
    """Renders a Processed Paper Sales form."""

    form = ProcessedPaperSalesForm(
        request.user.department.department_name)

    if request.method == "POST":
        form = ProcessedPaperSalesForm(
            request.user.department.department_name, request.POST)
        if form.is_valid():

            mprn_list = list(request.POST.get("mprn").split())
            gprn_list = list(request.POST.get("gprn").split())

            if len(mprn_list) > 1:
                save_multiple_mprn(request, mprn_list)
            elif len(gprn_list) > 1:
                save_multiple_gprn(request, gprn_list)
            else:
                form.instance.processor_name = request.user.__str__()
                form.save()
            messages.success(request, "Form submitted successfully.")
            return redirect("/bgeForms/")

        else:
            messages.error(
                request, """Something went wrong. If the problem
                    persists contact support.""")

    context = {
        "form": form

    }

    return render(request, "bgeForms/processedPaperSalesForm.html", context)


def save_multiple_mprn(request, mprn_list: list):
    for mprn in mprn_list:
        f = ProcessedPaperSalesForm(
            request.user.department.department_name,
            request.POST)
        f.save(commit=False)
        f.instance.mprn = mprn
        f.instance.processor_name = request.user.__str__()
        f.instance.save()


def save_multiple_gprn(request, gprn_list: list):
    for gprn in gprn_list:
        f = ProcessedPaperSalesForm(
            request.user.department.department_name,
            request.POST)
        f.save(commit=False)
        f.instance.gprn = gprn
        f.instance.processor_name = request.user.__str__()
        f.instance.save()
