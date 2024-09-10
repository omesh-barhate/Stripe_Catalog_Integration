from django.urls import path
from .views import CustomerReadWrite,CustomerReadWriteDelete

urlpatterns=[
    path('customers/',CustomerReadWrite.as_view()),
    path('customers/<str:pk>',CustomerReadWriteDelete.as_view()),
]