"""yes_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from login.views import LoginView
from Business.views import AddBusinessView, GetBusinessView, DeleteBusinessView, EditBusinessView
from Customers.views import AddCustomerView, GetCustomersView, DeleteCustomerView, EditCustomerView
from finance.views import AddTransactionView, GetTransactionView, CreateCSV, BackUpDataBase, CopyCustomersView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('addBusiness/', AddBusinessView.as_view()),
    path('getBusiness/', GetBusinessView.as_view()),
    path('deleteBusiness/', DeleteBusinessView.as_view()),
    path('editBusiness/', EditBusinessView.as_view()),
    path('addCustomer/', AddCustomerView.as_view()),
    path('getCustomer/', GetCustomersView.as_view()),
    path('deleteCustomer/', DeleteCustomerView.as_view()),
    path('editCustomer/', EditCustomerView.as_view()),
    path('addTransaction/', AddTransactionView.as_view()),
    path('getTransaction/', GetTransactionView.as_view()),
    path('createCSV/', CreateCSV.as_view()),
    path('backup/', BackUpDataBase.as_view()),
    path('copy/', CopyCustomersView.as_view()),












]
