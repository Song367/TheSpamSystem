from django.urls import path
from . import views


urlpatterns = [
    path('login/',views.login),
    path('register/',views.register),
    path('insert_email/',views.insert_email),
    path('delete_email/',views.delete_email),
    path('query_email_send/',views.query_email_send),
    path('query_email_receive/',views.query_email_receive),
    path('query_email_spam/',views.query_email_spam),
    path('dw/',views.every_month_day_emails),
]