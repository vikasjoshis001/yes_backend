import csv
import json
import requests
from datetime import datetime

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from requirements import success, error
from Customers.models import TransactionHistoryModel, CustomersModel
from Customers.serializers import TransactionHistorySerializer
from Business.models import BusinessModel

# Create your views here.

# Api for Add Transaction


class AddTransactionView(generics.CreateAPIView):
    """Api for Adding Transaction"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        transactionName = request.data.get("transactionName")
        transactionDebit = request.data.get("transactionDebit")
        transactionCredit = request.data.get("transactionCredit")
        transactionContact = request.data.get("transactionContact")
        transactionAddress = request.data.get("transactionAddress")
        transactionAadharNumber = request.data.get("transactionAadharNumber")
        transactionPanNumber = request.data.get("transactionPanNumber")
        transactionBusiness = request.data.get("businessId")
        transactionCustomer = request.data.get("customerId")

        try:
            transaction_dic = {
                "transactionName": transactionName,
                "transactionDebit": transactionDebit,
                "transactionCredit": transactionCredit,
                "transactionPending": int(transactionCredit) - int(transactionDebit),
                "transactionContact": transactionContact,
                "transactionAddress": transactionAddress,
                "transactionAadharNumber": transactionAadharNumber,
                "transactionPanNumber": transactionPanNumber,
                "transactionBusiness": transactionBusiness,
                "transactionCustomer": transactionCustomer
            }

            customerObj = CustomersModel.objects.filter(
                customerId=transactionCustomer)
            customerObj.update(customerDebit=transactionDebit, customerCredit=transactionCredit,
                               customerPending=int(transactionCredit) - int(transactionDebit))
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
            response_message = success.APIResponse(200, "List of All Transactions", {
                                                   "transactionsList": serializer.data}).respond()
        except Exception as e:
            response_message = error.APIResponse(404, "Unable to list Transactions", {
                                                 'error': str(e)}).respond()
        finally:
            return Response(response_message)


# Api to CreateCSV
class CreateCSV(APIView):
    """Api for creating CSV FIle"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
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
        except Exception as e:
            response_message = error.APIResponse(404, "Unable to Create CSV File", {
                                                 'error': str(e)}).respond()
        finally:
            return Response(response_message)

# Api for backup Database


class BackUpDataBase(APIView):
    """ Api for backup database """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            headers = {
                "Authorization": "Bearer 1//04YG-qyy5gIs_CgYIARAAGAQSNwF-L9IrgUQkvGqjD1bnclOnuJNivSnOdNrkCX3OyUds7A6hPYN-E6hj2cBv1MFCKGj2tMp1xqM"}
            para = {
                "name": "db.sqlite3",
                # "parents": ["1uKXpvoR3B15S-HZ--h-h3qjxlFUKJN6S"]
            }

            files = {
                'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
                'file': open("./db.sqlite3", "rb")
            }
            r = requests.post(
                "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
                headers=headers,
                files=files
            )
            print(r.text)
            response_message = success.APIResponse(
                200, "Database file Uploaded Successfully", None).respond()
        except Exception as e:
            response_message = error.APIResponse(404, "Unable to Upload Database", {
                                                 'error': str(e)}).respond()
        finally:
            return Response(response_message)
