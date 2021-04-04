import csv
import os
import pandas as pd
from datetime import datetime

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from yes_backend.settings import sheetsFolder, sheetsFolderPath

from requirements import success, error
from Customers.models import CustomersModel
from Customers.serializers import CustomersSerializer
from Business.models import BusinessModel
from .models import TransactionHistoryModel
from .serializers import TransactionHistorySerializer
# Create your views here.
# Api for Add Transaction


class AddTransactionView(generics.CreateAPIView):
    """Api for Adding Transaction"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        transactionName = request.data.get("transactionName")
        transactionDebit = request.data.get("transactionDebit")
        transactionCredit = request.data.get("transactionCredit")
        transactionBusiness = request.data.get("businessId")
        transactionCustomer = request.data.get("customerId")

        try:

            customerObj = CustomersModel.objects.get(
                customerId=transactionCustomer)
            totalDebit = customerObj.customerDebit
            totalCredit = customerObj.customerCredit

            customerObj = CustomersModel.objects.filter(
                customerId=transactionCustomer)
            customerDebit = int(transactionDebit) + int(totalDebit)
            customerCredit = int(transactionCredit) + int(totalCredit)
            customerObj.update(customerDebit=customerDebit, customerCredit=customerCredit,
                               customerPending=int(customerCredit) - int(customerDebit))

            transaction_dic = {
                "transactionName": transactionName,
                "transactionDebit": transactionDebit,
                "transactionCredit": transactionCredit,
                "transactionPending": int(customerCredit) - int(customerDebit),
                "transactionBusiness": transactionBusiness,
                "transactionCustomer": transactionCustomer
            }

            serializer = TransactionHistorySerializer(data=transaction_dic)
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
                totalDebit += int(serializer.data[i]['transactionDebit'])
                totalCredit += int(serializer.data[i]['transactionCredit'])
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


# Api to CreateTransactionCSV
class CreateTransactionCSV(APIView):
    """Api for creating CSV FIle"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        try:
            transaction = data['transactionHistory']
            name = transaction[0]['transactionName']
            business = transaction[0]['transactionBusiness']
            businessName = BusinessModel.objects.get(businessId=business)
            totalCredit = totalDebit = totalPending = 0
            # Folder Path
            folderPath = sheetsFolderPath + "/" + \
                sheetsFolder + "/" + businessName.businessName
            newFolder = datetime.now().strftime("%d%m%Y")
            path = os.path.join(folderPath, newFolder)
            if not os.path.exists(path):
                os.mkdir(path)
            newPath = path
            filename = newPath + "/" + name + \
                " Transaction History - " + datetime.now().strftime("%d%m%Y%H%M%S") + ".csv"
            row_list = [["Date", "Name", "Credit", "Debit", "", "Pending"],
                        [None, None, None, None, None]]
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(row_list)

            for transact in transaction:
                dic = {
                    "Date": transact['creationTime'],
                    "Name": transact['transactionName'],
                    "Credit": transact['transactionCredit'],
                    "Debit": transact['transactionDebit'],
                    "Pending": transact['transactionPending'],
                }
                totalCredit += int(transact['transactionCredit'])
                totalDebit += int(transact['transactionDebit'])
                totalPending += int(transact['transactionPending'])

                row_list = [[dic['Date'], dic['Name'],
                             dic['Credit'], dic['Debit'], dic['Pending']]]
                with open(filename, 'a') as file:
                    writer = csv.writer(file)
                    writer.writerows(row_list)
            row_list = [["", "Total", totalCredit, totalDebit, totalPending]]
            with open(filename, 'a') as file:
                writer = csv.writer(file)
                writer.writerows(row_list)
            response_message = success.APIResponse(200, "CSV File Created Successfully", {
                "transactionsList": None}).respond()
            return Response(response_message)
        except Exception as e:
            response_message = error.APIResponse(404, "Unable to Create CSV File", {
                'error': str(e)}).respond()
        finally:
            return Response(response_message)
