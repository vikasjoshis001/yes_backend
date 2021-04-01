import csv
import json
import requests
from datetime import datetime
import pandas as pd
import pdfkit as pdf

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from requirements import success, error
from Customers.models import TransactionHistoryModel, CustomersModel
from Customers.serializers import TransactionHistorySerializer,CustomersSerializer
from Business.models import BusinessModel

# Email
from django.core.mail import EmailMessage

# Create your views here.

# Api for Add Transaction


class AddTransactionView(generics.CreateAPIView):
    """Api for Adding Transaction"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        transactionName = request.data.get("transactionName")
        transactionNewDebit = request.data.get("transactionNewDebit")
        transactionCredit = request.data.get("transactionCredit")
        transactionContact = request.data.get("transactionContact")
        transactionAddress = request.data.get("transactionAddress")
        transactionAadharNumber = request.data.get("transactionAadharNumber")
        transactionPanNumber = request.data.get("transactionPanNumber")
        transactionBusiness = request.data.get("businessId")
        transactionCustomer = request.data.get("customerId")

        try:

            customerObj = CustomersModel.objects.get(
                customerId=transactionCustomer)
            totalDebit = customerObj.customerDebit

            customerObj = CustomersModel.objects.filter(
                customerId=transactionCustomer)
            customerDebit = int(transactionNewDebit) + int(totalDebit)
            customerObj.update(customerDebit=customerDebit, customerCredit=transactionCredit,
                               customerPending=int(transactionCredit) - int(customerDebit))

            transaction_dic = {
                "transactionName": transactionName,
                "transactionNewDebit": transactionNewDebit,
                "transactionTotalDebit": customerDebit,
                "transactionCredit": transactionCredit,
                "transactionPending": int(transactionCredit) - int(customerDebit),
                "transactionContact": transactionContact,
                "transactionAddress": transactionAddress,
                "transactionAadharNumber": transactionAadharNumber,
                "transactionPanNumber": transactionPanNumber,
                "transactionBusiness": transactionBusiness,
                "transactionCustomer": transactionCustomer
            }

            serializer = TransactionHistorySerializer(data=transaction_dic)
            print(serializer.is_valid())
            if (serializer.is_valid()):
                serializer.save()

            else:
                response_message = success.APIResponse(
                    404, "Customer Does Not Exist", {'error': None}).respond()
                return Response(response_message)

            response_message = success.APIResponse(
                200, "Transaction Added Successfully", transaction_dic).respond()
        except Exception as e:
            response_message = error.APIResponse(404, "Unable to add Transaction", {
                                                 'error': str(e)}).respond()
        finally:
            return Response(response_message)


# Api for Getting Transactions
class GetTransactionView(generics.ListCreateAPIView):
    """Api for Get Transactions"""

    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        try:
            transactionCustomer = request.query_params['customerId']
            transactions_list = TransactionHistoryModel.objects.filter(
                transactionCustomer=transactionCustomer)
            serializer = TransactionHistorySerializer(
                transactions_list, many=True)
            totalCredit = totalDebit = totalPending = 0
            totalDict = {}
            for i in range(len(serializer.data)):
                totalDebit = int(serializer.data[i]['transactionTotalDebit'])
                totalCredit = serializer.data[i]['transactionCredit']
                totalPending = int(serializer.data[i]['transactionPending'])
            totalDict['totalCredit'] = totalCredit
            totalDict['totalDebit'] = totalDebit
            totalDict['totalPending'] = totalPending
            dic = {
                "status": 200,
                "msg": "List of All Transactions",
                "data": {'transactionHistory': serializer.data},
                "total": totalDict,
            }
            return Response(data=dic)
        except Exception as e:
            response_message = error.APIResponse(404, "Unable to list Transactions", {
                                                 'error': str(e)}).respond()
            return Response(response_message)


# Api to CreateCSV
class CreateCSV(APIView):
    """Api for creating CSV FIle"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        try:
            try:
                entries = data['customersList']
                business = entries[0]['customerBusiness']
                print(business)
                businessName = BusinessModel.objects.get(businessId=business)
                print(businessName.businessName)
                print("Working...")
                filename = "CSV Sheets/" + businessName.businessName + \
                    " Customers List - " + datetime.now().strftime("%d%m%Y%H%M%S") + ".csv"
                row_list = [["Name", "Debit", "Credit", "Pending", "Contact"],
                            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]]
                with open(filename, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(row_list)

                for entry in entries:
                    dic = {
                        "Name": entry['customerName'],
                        "Debit": entry['customerDebit'],
                        "Credit": entry['customerCredit'],
                        "Pending": entry['customerPending'],
                        "Contact": entry['customerContact'],
                    }

                    row_list = [[dic['Name'], dic['Debit'],
                                 dic['Credit'], dic['Pending'], dic['Contact']]]
                    with open(filename, 'a') as file:
                        writer = csv.writer(file)
                        writer.writerows(row_list)
                response_message = success.APIResponse(200, "CSV File Created Successfully", {
                    "transactionsList": None}).respond()

            except:
                transaction = data['transactionHistory']
                name = transaction[0]['transactionName']
                filename = "CSV Sheets/" + name + \
                    " Transaction History - " + datetime.now().strftime("%d%m%Y%H%M%S") + ".csv"
                row_list = [["Date", "Name", "Credit", "New Debit", "Total Debit", "Pending"],
                            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]]
                with open(filename, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(row_list)

                for transact in transaction:
                    dic = {
                        "Date": transact['creationTime'],
                        "Name": transact['transactionName'],
                        "Credit": transact['transactionCredit'],
                        "New Debit": transact['transactionNewDebit'],
                        "Total Debit": transact['transactionTotalDebit'],
                        "Pending": transact['transactionPending'],
                    }

                    row_list = [[dic['Date'], dic['Name'], dic['Credit'], dic['New Debit'],
                                 dic['Total Debit'], dic['Pending']]]
                    with open(filename, 'a') as file:
                        writer = csv.writer(file)
                        writer.writerows(row_list)

                response_message = success.APIResponse(200, "CSV File Created Successfully", {
                    "transactionsList": None}).respond()
        except Exception as e:
            response_message = error.APIResponse(404, "Unable to Create CSV File", {
                                                 'error': str(e)}).respond()
        finally:
            return Response(response_message)

# Api for backup Database


class BackUpDataBase(APIView):
    """ Api for backup database """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            subject = "Database  Backup of Yes MultiServices"
            message = ""
            recipient_list = ['vikasjoshis001@gmail.com']
            email = EmailMessage(
                subject, message, 'crunchbase.io@gmail.com', recipient_list)
            print("A")
            email.attach_file("./db.sqlite3")
            print("B")
            email.send()           
            
                
            dic = {
            "Type": "Success",
            "msg": "Mail Sent Succesfully",
            }
            return Response(data=dic)
        
        except:
            dic = {
            "Type": "Error",
            "msg": "Sorry!Mail not Sent...",
            }
            return Response(data=dic)
        
        
# Copy Customers Api


class CopyCustomersView(APIView):
    """ Api for Copy Customers from One Business to Another """
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        businessId = request.data.get('businessId')
        customersId = request.data.get('customersId')
        
        try:
            for userId in customersId:
                customerObj = CustomersModel.objects.get(customerId = userId)
                newCustomerName = customerObj.customerName
                newCustomerDebit= customerObj.customerDebit
                newCustomerCredit = customerObj.customerCredit
                newCustomerPending = customerObj.customerPending
                newCustomerAddress = customerObj.customerAddress
                newCustomerAadharNumber = customerObj.customerAadharNumber
                newCustomerPanNumber = customerObj.customerPanNumber
                newCustomerContact = customerObj.customerContact
                customer_dic = {
                    "customerName": newCustomerName,
                    "customerDebit": newCustomerDebit,
                    "customerCredit": newCustomerCredit,
                    "customerPending": newCustomerPending,
                    "customerContact": newCustomerContact,
                    "customerAddress": newCustomerAddress,
                    "customerAadharNumber": newCustomerAadharNumber,
                    "customerPanNumber": newCustomerPanNumber,
                    "customerBusiness": businessId,
                }
                serializer = CustomersSerializer(data=customer_dic)
                if (serializer.is_valid()):
                    serializer.save()
                else:
                    response_message = success.APIResponse(
                        404, "Unable to add to Customer Model", {'error': None}).respond()
                    return Response(response_message)
                transaction_dic = {
                    "transactionName": newCustomerName,
                    "transactionNewDebit": newCustomerDebit,
                    "transactionTotalDebit": newCustomerDebit,
                    "transactionCredit": newCustomerCredit,
                    "transactionPending": newCustomerPending,
                    "transactionContact": newCustomerContact,
                    "transactionAddress": newCustomerAddress,
                    "transactionAadharNumber": newCustomerAadharNumber,
                    "transactionPanNumber": newCustomerPanNumber,
                    "transactionBusiness": businessId,
                    "transactionCustomer": serializer.data['customerId']
                }
                serializer = TransactionHistorySerializer(data=transaction_dic)
                if (serializer.is_valid()):
                    serializer.save()
                else:
                    response_message = success.APIResponse(
                        404, "Unable to add to Transaction Model", {'error': str(e)}).respond()
                    return Response(response_message)

            response_message = success.APIResponse(
                200, "Customer Added Successfully", customer_dic).respond()
        except Exception as e:
            response_message = error.APIResponse(404, "Unable to add Customer", {
                                                'error': str(e)}).respond()
        finally:
            return Response(response_message)
            
            
        
