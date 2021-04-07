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
from Business.views import AddBusinessView, GetBusinessView, DeleteBusinessView, EditBusinessView, BusinessManagement
from Customers.views import AddCustomerView, GetCustomersView, DeleteAllCustomers,DeleteCustomerView, EditCustomerView,CustomerProfit,CreateCustomersCSV,CopyCustomersView,CreateProfitCSV,CreateCustomerPdf,CreateProfitPdf
from finance.views import BackUpDataBase
from Transaction.views import AddTransactionView, GetTransactionView,CreateTransactionCSV,CreateTransactionPdf
 
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url

schema_view = get_schema_view(
   openapi.Info(
      title="Yes Multiservices API Documentation",
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    url('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url('api_documentation',schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    path('login/', LoginView.as_view()),
    
    path('addBusiness/', AddBusinessView.as_view()),
    path('getBusiness/', GetBusinessView.as_view()),
    path('deleteBusiness/', DeleteBusinessView.as_view()),
    path('editBusiness/', EditBusinessView.as_view()),
    path('businessManagement/', BusinessManagement.as_view()),
    
    path('addCustomer/', AddCustomerView.as_view()),
    path('getCustomer/', GetCustomersView.as_view()),
    path('deleteCustomer/', DeleteCustomerView.as_view()),
    path('editCustomer/', EditCustomerView.as_view()),
    path('getCustomerProfit/', CustomerProfit.as_view()),
    path('copyCustomers/', CopyCustomersView.as_view()),
    path('deleteAllCustomers/', DeleteAllCustomers.as_view()),
    path('createCustomersCSV/', CreateCustomersCSV.as_view()),
    path('createProfitCSV/', CreateProfitCSV.as_view()),
    path('createCustomersPdf/', CreateCustomerPdf.as_view()),
    path('createProfitPdf/', CreateProfitPdf.as_view()),
    
    path('addTransaction/', AddTransactionView.as_view()),
    path('getTransaction/', GetTransactionView.as_view()),
    path('createTransactionCSV/', CreateTransactionCSV.as_view()),
    path('createTransactionPdf/', CreateTransactionPdf.as_view()),
    
    path('backup/', BackUpDataBase.as_view()),
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
