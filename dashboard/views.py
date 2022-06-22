from django.shortcuts import render
from employee.models import Employee
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication
)
from userRoles.views import getUserType, getSeniorManager
from rest_framework.permissions import IsAuthenticated
from inventory.models import Phone, Tablet, OtherDevice


# TODO Rebuild dashboards rendering same as IT dashboard
@login_required
def dashboard(request):
    """ Render dashboard according to user logged in """

    user = request.user
    team = None
    teamCount = {}
    dashboard = getUserDashboard(user)

    # If HR or Management load team as all employees excluding leavers.
    if dashboard == "HR":
        team = Employee.objects.exclude(employee_status="Leaver")
        teamCount = getTeamCount(team)

    # If Senior Manager loads the whole department
    elif dashboard == "manager" and (getSeniorManager(request.user) == "OPM"):
        team = Employee.objects.filter(
            department=request.user.department,
        ).exclude(employee_status="Leaver")
        teamCount = getTeamCount(team)

    elif dashboard == "manager" and (getSeniorManager(request.user) == "SFSM"):
        team = Employee.objects.filter(
            department=request.user.department,
            sub_department=request.user.sub_department
        ).exclude(employee_status="Leaver")
        teamCount = getTeamCount(team)

    elif dashboard == "manager" and (getSeniorManager(request.user) == "ACD"):
        team = Employee.objects.filter(
            department=request.user.department,
        ).exclude(employee_status="Leaver")
        teamCount = getTeamCount(team)

    # If only manager load team where manager is the same
    elif dashboard == "manager":
        team = Employee.objects.filter(
            manager=user
        ).exclude(employee_status="Leaver")
        teamCount = getTeamCount(team)

    elif dashboard == "IT":

        context = {
            "devices_count": get_device_count(request),
        }
        return render(request, "dashboard/ITDashboard.html", context)

    context = {
        "teamCount": teamCount,
        "dashboard": dashboard
    }

    return render(request, "dashboard/dashboard.html", context)


def getUserDashboard(user):
    """
    Returns what dashboard the logged user should see.
    Required Arguments: User
    """

    userDashboard = ""

    if getUserType(user) == "HR":
        userDashboard = "HR"

    elif ((user.is_manager == "Y" and
           getUserType(user) == "HR") or
          (user.is_manager == "Y" and
           getUserType(user) == "HR")):

        userDashboard = "HR"

    elif user.is_manager == "Y":
        userDashboard = "manager"

    elif getUserType(user) == "IT":
        userDashboard = "IT"

    elif user.role.role_name == "Order Processing Executive":
        userDashboard = "processingExec"

    elif user.role.role_name == "Training Support Executive":
        userDashboard = "trainingExec"

    return userDashboard


def getTeamCount(team):
    """
    Returns a count of all employees status on a team.
    Required Arguments: team object
    """
    teamCount = {
        "teamInactive": team.filter().exclude(
            employee_status="Active").exclude(
                employee_status="Leaver").count(),
        "teamActive": team.filter(employee_status="Active").count(),
        "teamInactivePaid": team.filter(
            employee_status="Inactive paid").count(),
        "teamInactiveUnpaid": team.filter(
            employee_status="Inactive unpaid").count(),
        "teamSick": team.filter(employee_status="Sick").count(),
        "teamHolidays": team.filter(employee_status="Holidays").count(),
        "teamLeaver": team.filter(employee_status="Leaver").count(),
        "teamAWOL": team.filter(
            employee_status="AWOL").count(),
        "teamMaternity": team.filter(
            employee_status="Maternity Leave").count(),
        "teamLTA": team.filter(employee_status="LTA").count(),
        "teamInduction": team.filter(employee_status="Induction").count(),
        "teamBH": team.filter(employee_status="Bank Holiday").count(),
        "teamTotal": team.count()
    }

    return teamCount


def get_device_count(request):
    """ Get a count of all devices to show on dashboard """

    phones = Phone.objects.all()
    tablets = Tablet.objects.all()

    active = {
        "phones": phones.filter(status="active").count(),
        "tablets": tablets.filter(status="active").count(),
    }

    inactive = {
        "phones": phones.filter(status="inactive").count(),
        "tablets": tablets.filter(status="inactive").count(),
    }

    repair = {
        "phones": phones.filter(status="repair").count(),
        "tablets": tablets.filter(status="repair").count(),
    }

    out_of_order = {
        "phones": phones.filter(status="out_of_order").count(),
        "tablets": tablets.filter(status="out_of_order").count(),
    }

    device_count = {
        "active": active,
        "inactive": inactive,
        "repair": repair,
        "out_of_order": out_of_order,
    }

    return device_count


class getChartData(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        user = request.user
        team = None
        dashboard = getUserDashboard(user)

        if dashboard == "HR":

            team = Employee.objects.all()

        # If Senior Manager loads the whole department
        elif dashboard == "manager" and (getSeniorManager(request.user) == "OPM"):
            team = Employee.objects.filter(
                department=request.user.department,
            ).exclude(employee_status="Leaver")

        elif dashboard == "manager" and (getSeniorManager(request.user) == "SFSM"):
            team = Employee.objects.filter(
                department=request.user.department,
                sub_department=request.user.sub_department
            ).exclude(employee_status="Leaver")

        elif dashboard == "manager" and (getSeniorManager(request.user) == "ACD"):
            team = Employee.objects.filter(
                department=request.user.department,
            ).exclude(employee_status="Leaver")

        elif dashboard == "manager":
            team = Employee.objects.filter(
                manager=user,
            ).exclude(employee_status="Leaver")

        if team:
            teamActive = team.filter(employee_status="Active").count()
            teamInactivePaid = team.filter(
                employee_status="Inactive paid").count()
            teamInactiveUnpaid = team.filter(
                employee_status="Inactive unpaid").count()
            teamSick = team.filter(employee_status="Sick").count()
            teamHolidays = team.filter(employee_status="Holidays").count()
            teamLeaver = team.filter(employee_status="Leaver").count()
            teamAWOL = team.filter(employee_status="AWOL").count()
            teamMaternity = team.filter(
                employee_status="Maternity Leave").count()
            teamLTA = team.filter(employee_status="LTA").count()
            teamInduction = team.filter(employee_status="Induction").count()
            teamBH = team.filter(employee_status="Bank Holiday").count()
        else:
            teamActive = 0
            teamInactivePaid = 0
            teamInactiveUnpaid = 0
            teamSick = 0
            teamHolidays = 0
            teamLeaver = 0
            teamAWOL = 0
            teamMaternity = 0
            teamLTA = 0
            teamInduction = 0
            teamBH = 0

        labels = ["Active", "Inactive paid", "Inactive unpaid", "Sick",
                  "Holidays", "Leaver", "AWOL", "Maternity Leave", "LTA",
                  "Induction", "Bank Holiday"]

        defaultItems = [
            teamActive,
            teamInactivePaid,
            teamInactiveUnpaid,
            teamSick,
            teamHolidays,
            teamLeaver,
            teamAWOL,
            teamMaternity,
            teamLTA,
            teamInduction,
            teamBH
        ]

        data = {
            "labels": labels,
            "default": defaultItems
        }
        return Response(data)
