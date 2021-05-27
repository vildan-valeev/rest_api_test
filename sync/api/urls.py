
from django.contrib import admin
from django.urls import path

from .views import SumArray

urlpatterns = [
    path('sum/', SumArray.as_view()),

]
