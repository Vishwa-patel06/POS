from django.urls import path, include
from Customer import views

urlpatterns = [
    path('create/', views.CustomerRegistrationView.as_view()),
    path('customer-list/', views.CustomerListView.as_view()),
]
