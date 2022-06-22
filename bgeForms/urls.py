from django.urls import path
from .views import form_list, fte_form, processed_paper_sales_form

app_name = "bgeForms"

urlpatterns = [
    path("", form_list, name="form_list"),
    path("FTEForm/", fte_form, name="fte_form"),
    path("ProcessedPaperSalesForm/", processed_paper_sales_form,
         name="processed_paper_sales_form"),
]
