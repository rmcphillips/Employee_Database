from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .forms import UserRolesModelForm
from django.core.paginator import Paginator
from django.db.models import Q
from userAccounts.models import CustomUser
from django.db.models import Value as V
from django.db.models.functions import Concat

# Create your views here.


@login_required
@staff_member_required
def managerList(request):
    """ Renders a paginated list of all managers. """

    searchQuery = request.GET.get("searchManager", None)

    if searchQuery:
        managers = CustomUser.objects.annotate(
            full_name=Concat('first_name', V(' '), 'last_name')
        ).filter(
            Q(full_name__icontains=searchQuery) |
            Q(last_name__icontains=searchQuery) |
            Q(first_name__icontains=searchQuery) |
            Q(role__role_name__icontains=searchQuery) |
            Q(department__department_name__icontains=searchQuery) |
            Q(sub_department__sub_department_name__icontains=searchQuery)
        ).order_by("first_name")

    else:
        managers = CustomUser.objects.all().order_by("username")

    # Gives a list per page of 10 managers
    managersPaginator = Paginator(managers, 10)

    pageNum = (request.GET.get("page"))

    page = managersPaginator.get_page(pageNum)

    context = {
        "page": page
    }

    return render(request, "userRoles/managerList.html", context)


@login_required
@staff_member_required
def managerUpdate(request, pk):
    """ Update an existing manager """

    manager = get_object_or_404(CustomUser, id=pk)
    form = UserRolesModelForm(instance=manager)

    if request.method == "POST":

        form = UserRolesModelForm(request.POST, instance=manager)

        if form.is_valid():
            form.save()
            messages.success(request, "Manager updated successfully.")
        else:
            messages.error(
                request, "Something went wrong. If the problem persists contact support.")
            print(form.errors)

        return redirect("/userRoles")

    context = {
        "form": form
    }

    return render(request, "userRoles/managerUpdate.html", context)


def getUserType(user):
    # ! This needs to be done better for sure.
    userType = ""

    if user.department:

        if (user.department.department_name == "HR" or
                user.department.department_name == "Management" or
                user.department.department_name == "Accounts"):
            userType = "HR"

        elif ((user.is_manager == "Y" and
               user.department.department_name == "HR") or
              (user.is_manager == "Y" and
               user.department.department_name == "Management") or
              (user.is_manager == "Y" and
                user.department.department_name == "Accounts")):

            userType = "HR"

        elif user.is_manager == "Y":
            userType = "manager"

        elif user.department.department_name == "Technology":
            userType = "IT"

        elif user.department.department_name == "Training":
            userType = "Training"
    else:
        userType = ""

    return userType


def getSeniorManager(user):
    # ! This needs to be done better for sure.

    if user.role.role_name == "Senior Field Sales Manager":
        return "SFSM"
    if user.role.role_name == "Operations Manager":
        return "OPM"
    if user.role.role_name == "Account Director":
        return "ACD"
