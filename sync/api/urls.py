
from django.contrib import admin
from django.urls import path

from .views import SetArray, GetSum

urlpatterns = [
    path('set/', SetArray.as_view()),
    path('sum/', GetSum.as_view()),

]
