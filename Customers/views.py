import csv
import os
import pandas as pd
from datetime import datetime

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from yes_backend.settings import sheetsFolder, sheetsFolderPath, sheetsCustomers

from requirements import success, error
from .models import CustomersModel
from .serializers import CustomersSerializer
from Transaction.models import TransactionHistoryModel
from Transaction.serializers import TransactionHistorySerializer
from Business.models import BusinessModel
# Create your views here.

# Add Customer Api


class AddCustomerView(APIView):
    """Api for Adding Customer"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        customerName = request.data.get("customerName")
        customerDebit = request.data.get("customerDebit")
        customerCredit = request.data.get("customerCredit")
        customerContact = request.data.get("customerContact")
        customerAddress = request.data.get("customerAddress")
        customerAadharNumber = request.data.get("customerAadharNumber")
        customerPanNumber = request.data.get("customerPanNumber")
        customerDOB = request.data.get("customerDOB")
        customerBusiness = request.data.get("businessId")

        try:
            customer_dic = {
                "customerName": customerName,
                "customerDebit": customerDebit,
                "customerCredit": customerCredit,
                "customerPending": int(customerCredit) - int(customerDebit),
                "customerContact": customerContact,
                "customerAddress": customerAddress,
                "customerAadharNumber": customerAadharNumber,
                "customerPanNumber": customerPanNumber,
                "customerDOB": customerDOB,
                "customerBusiness": customerBusiness,
            }
            serializer = CustomersSerializer(data=customer_dic)
            if (serializer.is_valid()):
                serializer.save()
            else:
                response_message = success.APIResponse(
                    404, "Unable to add to Customers Model", {'error': None}).respond()
                return Response(response_message)
            transaction_dic = {
                "transactionName": customerName,
                "transactionDebit": customerDebit,
                "transactionCredit": customerCredit,
                "transactionPending": int(customerCredit) - int(customerDebit),
                "transactionBusiness": customerBusiness,
                "transactionCustomer": serializer.data['customerId']
            }
            serializer = TransactionHistorySerializer(data=transaction_dic)
            if (serializer.is_valid()):
                serializer.save()
            else:
                response_message = success.APIResponse(
                    404, "Unable to add customer to Transaction Model", {'error': None}).respond()
                return Response(response_message)

            response_message = success.APIResponse(
                200, "Customer Added Successfully", customer_dic).respond()
        except Exception as e:
            response_message = error.APIResponse(404, "Unable to add Customer", {
                                                 'error': str(e)}).respond()
        finally:
            return Response(response_message)

# Api for Get Customer


class GetCustomersView(generics.ListCreateAPIView):
    """Api for Get Customers"""

    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        try:
            businessId = request.query_params['businessId']
            businessObj = BusinessModel.objects.get(
                businessId=businessId)
            businessName = businessObj.businessName
            customerList = CustomersModel.objects.filter(
                customerBusiness=businessId)
            serializer = CustomersSerializer(customerList, many=True)
            totalCredit = totalDebit = totalPending = 0
            totalDict = {}
            for i in range(len(serializer.data)):
                totalCredit += int(serializer.data[i]['customerCredit'])
                totalDebit += int(serializer.data[i]['customerDebit'])
                totalPending += int(serializer.data[i]['customerPending'])
            totalDict['totalCredit'] = totalCredit
            totalDict['totalDebit'] = totalDebit
            totalDict['totalPending'] = totalPending
            totalDict['businessName'] = businessName
            dic = {
                "status": 200,
                "msg": "List of All Customers",
                "data": {'customersList': serializer.data},
                "total": totalDict,
            }
            return Response(data=dic)
        except Exception as e:
            response_message = error.APIResponse(404, "Unable to list Customers", {
                                                 'error': str(e)}).respond()
            return Response(response_message)

# Api for Delete Customers


class DeleteCustomerView(APIView):
    """Api for Delete Customer"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        customerId = request.query_params['customerId']
        try:
            customerObj = CustomersModel.objects.get(customerId=customerId)
            if customerObj:
                customerObj.delete()
            transactionCustomerObj = TransactionHistoryModel.objects.filter(
                transactionCustomer=customerId)
            if customerObj:
                transactionCustomerObj.delete()
                response_message = success.APIResponse(
                    200, "Customer Deleted Successfully", None).respond()
            else:
                response_message = error.APIResponse(
                    404, "Authentication Failed", None).respond()

        except CustomersModel.DoesNotExist:
            response_message = error.APIResponse(
                404, "Customer Does Not Exist", None).respond()

        except Exception as e:
            response_message = error.APIResponse(
                404, "Invalid CustomerId", None).respond()

            return Response(response_message)
        finally:
            return Response(response_message)

# API for Update Customers


class EditCustomerView(generics.CreateAPIView):
    ''' Api for Update Customer '''

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            customerId = request.data.get("customerId")
            customerName = request.data.get("customerName")
            customerContact = request.data.get("customerContact")
            customerAddress = request.data.get("customerAddress")
            customerAadharNumber = request.data.get("customerAadharNumber")
            customerPanNumber = request.data.get("customerPanNumber")
            customerDOB = request.data.get("customerDOB")

            transactionCustomerObj = TransactionHistoryModel.objects.filter(
                transactionCustomer=customerId)
            transactionCustomerObj.update(
                transactionName=customerName)

            customerObj = CustomersModel.objects.filter(customerId=customerId)
            if(customerObj):
                customerObj.update(customerName=customerName,
                                   customerContact=customerContact, customerAddress=customerAddress, customerAadharNumber=customerAadharNumber, customerPanNumber=customerPanNumber, customerDOB=customerDOB)
                response_message = success.APIResponse(
                    200, "Customer Updated Successfully", None).respond()
            else:
                response_message = error.APIResponse(
                    404, "Customer Does Not Exist", None).respond()

        except Exception as e:
            response_message = error.APIResponse(
                404, "Invalid CustomerId", {'error': str(e)}).respond()
        finally:
            return Response(response_message)


# Customer Transaction with All Businesses

class CustomerProfit(APIView):
    ''' Api for Customer Transaction with All Businesses '''

    permission_classes = [IsAuthenticated]

    def get(self, request):
        customerId = request.query_params["customerId"]
        businessId = request.query_params["businessId"]
        
        try:
            customerObj = CustomersModel.objects.get(customerId = customerId,customerBusiness = businessId)
            customerName = customerObj.customerName
            customerContact = customerObj.customerContact
            customerAddress = customerObj.customerAddress
            customerAadharNumber = customerObj.customerAadharNumber
            customerPanNumber = customerObj.customerPanNumber
            customerDOB = customerObj.customerDOB
            
            customerDic = {}
            customerList = []
            customerObjList = CustomersModel.objects.filter(customerName=customerName,
                                                        customerContact=customerContact, customerAddress=customerAddress, customerAadharNumber=customerAadharNumber, customerPanNumber=customerPanNumber, customerDOB=customerDOB)
            print(customerObjList)
            serializer = CustomersSerializer(customerObjList, many=True)
            totalCredit = totalDebit = totalPending = 0
            totalDict = {}
            for i in range(len(serializer.data)):
                businessObj = BusinessModel.objects.get(
                    businessId=serializer.data[i]['customerBusiness'])
                customerDic = {
                    "customerName": serializer.data[i]['customerName'],
                    "customerBusiness": businessObj.businessName,
                    "customerCredit": serializer.data[i]['customerCredit'],
                    "customerDebit": serializer.data[i]['customerDebit'],
                    "customerPending": serializer.data[i]['customerPending'],
                }
                customerList.append(customerDic)
                totalCredit += int(serializer.data[i]['customerCredit'])
                totalDebit += int(serializer.data[i]['customerDebit'])
                totalPending += int(serializer.data[i]['customerPending'])
            totalDict['totalCredit'] = totalCredit
            totalDict['totalDebit'] = totalDebit
            totalDict['totalPending'] = totalPending
            totalDict['customerName'] = customerName
            print(totalCredit)

            dic = {
                "status": 200,
                "msg": "List of All Customers",
                "data": {'profitList': customerList},
                "total": totalDict,
            }
            return Response(data=dic)
        except Exception as e:
            response_message = error.APIResponse(404, "Unable to list Customers", {
                                                 'error': str(e)}).respond()
            return Response(response_message)


# Copy Customers Api


class CopyCustomersView(APIView):
    """ Api for Copy Customers from One Business to Another """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        businessId = request.data.get('businessId')
        customersId = request.data.get('customersId')

        try:
            for userId in customersId:
                customerObj = CustomersModel.objects.get(customerId=userId)
                newCustomerName = customerObj.customerName
                newCustomerAddress = customerObj.customerAddress
                newCustomerAadharNumber = customerObj.customerAadharNumber
                newCustomerPanNumber = customerObj.customerPanNumber
                newCustomerContact = customerObj.customerContact
                newCustomerDOB = customerObj.customerDOB
                customer_dic = {
                    "customerName": newCustomerName,
                    "customerDebit": 0,
                    "customerCredit": 0,
                    "customerPending": 0,
                    "customerContact": newCustomerContact,
                    "customerAddress": newCustomerAddress,
                    "customerAadharNumber": newCustomerAadharNumber,
                    "customerPanNumber": newCustomerPanNumber,
                    "customerDOB":newCustomerDOB,
                    "customerBusiness": businessId,
                }
                serializer = CustomersSerializer(data=customer_dic)
                if (serializer.is_valid()):
                    serializer.save()
                else:
                    response_message = success.APIResponse(
                        404, "Unable to add to Customers Model", {'error': None}).respond()
                    return Response(response_message)
                transaction_dic = {
                    "transactionName": newCustomerName,
                    "transactionDebit": 0,
                    "transactionCredit": 0,
                    "transactionPending": 0,
                    "transactionBusiness": businessId,
                    "transactionCustomer": serializer.data['customerId']
                }
                serializer = TransactionHistorySerializer(data=transaction_dic)
                if (serializer.is_valid()):
                    serializer.save()
                else:
                    response_message = success.APIResponse(
                        404, "Unable to add customer to Transaction Model", {'error': None}).respond()
                    return Response(response_message)

            response_message = success.APIResponse(
                200, "Customer Added Successfully", None).respond()
        except Exception as e:
            response_message = error.APIResponse(404, "Unable to add Customer", {
                'error': str(e)}).respond()
        finally:
            return Response(response_message)


# Api to CreateCusomersCSV
class CreateCustomersCSV(APIView):
    """Api for creating CSV FIle"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        try:
            entries = data['customersList']
            business = entries[0]['customerBusiness']
            businessName = BusinessModel.objects.get(businessId=business)
            totalCredit = totalDebit = totalPending = 0
            # Folder Path
            folderPath = sheetsFolderPath + "/" + \
                sheetsFolder
            path = os.path.join(folderPath, businessName.businessName)
            if not os.path.exists(path):
                os.mkdir(path)
            folderPath = path
            newFolder = datetime.now().strftime("%d%m%Y")
            path = os.path.join(folderPath, newFolder)
            if not os.path.exists(path):
                os.mkdir(path)
            newPath = path
            filename = newPath + "/" + businessName.businessName + \
                "-Customers List - " + datetime.now().strftime("%d%m%Y%H%M%S") + ".csv"
            row_list = [["Name", "Credit", "Debit", "Pending", "Contact","Aadhar Card Number","Pan Card Number","Address","Date of Birth", ],
                        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]]
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(row_list)

            for entry in entries:
                dic = {
                    "Name": entry['customerName'],
                    "Credit": entry['customerCredit'],
                    "Debit": entry['customerDebit'],
                    "Pending": entry['customerPending'],
                    "Contact": entry['customerContact'],
                    "Aadhar Card Number":entry["customerAadharNumber"],
                    "Pan Card Number":entry["customerPanNumber"],
                    "Address":entry["customerAddress"],
                    "Date of Birth":entry["customerDOB"],
                    
                }
                totalCredit += int(entry['customerCredit'])
                totalDebit += int(entry['customerDebit'])
                totalPending += int(entry['customerPending'])

                row_list = [[dic['Name'], dic['Credit'],
                             dic['Debit'], dic['Pending'], dic['Contact'],dic['Aadhar Card Number'],dic['Pan Card Number'],dic["Address"],dic["Date of Birth"]]]
                with open(filename, 'a') as file:
                    writer = csv.writer(file)
                    writer.writerows(row_list)
            row_list = [["Total", totalCredit, totalDebit, totalPending, ""]]
            with open(filename, 'a') as file:
                writer = csv.writer(file)
                writer.writerows(row_list)
            response_message = success.APIResponse(200, "CSV File Created Successfully", {
                "transactionsList": None}).respond()
            return Response(response_message)
        except Exception as e:
            response_message = error.APIResponse(404, "Unable to Create CSV File", {
                                                 'error': str(e)}).respond()
            return Response(response_message)
        
        
# Api to CreateProfitCSV
class CreateProfitCSV(APIView):
    """Api for creating CSV FIle"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        try:
            profit = data['profitList']
            name = profit[0]['customerName']
            businessName = profit[0]['customerBusiness']
            totalCredit = totalDebit = totalPending = 0
            # Folder Path
            folderPath = sheetsFolderPath + "/" + \
                sheetsFolder
            path = os.path.join(folderPath, businessName)
            if not os.path.exists(path):
                os.mkdir(path)
            folderPath = path
            newFolder = datetime.now().strftime("%d%m%Y")
            path = os.path.join(folderPath, newFolder)
            if not os.path.exists(path):
                os.mkdir(path)
            newPath = path
            path = os.path.join(newPath, name)
            if not os.path.exists(path):
                os.mkdir(path)
            newPath = path
            filename = newPath + "/" + name + \
                " Customer Profit" + datetime.now().strftime("%d%m%Y%H%M%S") + ".csv"
            row_list = [["Business", "Name", "Credit", "Debit", "Pending"],
                        [None, None, None, None, None]]
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(row_list)

            for prof in profit:
                dic = {
                    "Business": prof['customerBusiness'],
                    "Name": prof['customerName'],
                    "Credit": prof['customerCredit'],
                    "Debit": prof['customerDebit'],
                    "Pending": prof['customerPending'],
                }
                totalCredit += int(prof['customerCredit'])
                totalDebit += int(prof['customerDebit'])
                totalPending += int(prof['customerPending'])

                row_list = [[dic['Business'], dic['Name'],
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
