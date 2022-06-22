"""employeeweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from allauth.account.views import LoginView
from django.views import defaults


def pageNotFound(request):
    return defaults.page_not_found(request, None)


def serverError(request):
    return defaults.server_error(request)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("employee/", include("employee.urls", namespace="employee")),
    path("inventory/", include("inventory.urls", namespace="inventory")),
    path("apiTools/", include("apiTools.urls", namespace="apiTools")),
    path("dashboard/", include("dashboard.urls", namespace="dashboard")),
    path("userRoles/", include("userRoles.urls", namespace="userRoles")),
    path("bgeForms/", include("bgeForms.urls", namespace="bgeForms")),
    path("iberForms/", include("iberForms.urls", namespace="iberForms")),
    path("pstForms/", include("pstForms.urls", namespace="pstForms")),
    path("pinergyForms/", include("pinergyForms.urls", namespace="pinergyForms")),
    path("reports/", include("reports.urls", namespace="reports")),
    path('accounts/', include('allauth.urls')),
    path("", LoginView.as_view(), name="login"),
    path("404/", pageNotFound),
    path("500/", serverError),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
