from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from requirements import success, error
from .models import CustomersModel, TransactionHistoryModel
from .serializers import CustomersSerializer, TransactionHistorySerializer

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
                "customerBusiness": customerBusiness,
            }
            serializer = CustomersSerializer(data=customer_dic)
            if (serializer.is_valid()):
                serializer.save()
            else:
                response_message = success.APIResponse(
                    404, "Business Does Not Exist", {'error': None}).respond()
                return Response(response_message)
            transaction_dic = {
                "transactionName": customerName,
                "transactionNewDebit": customerDebit,
                "transactionTotalDebit": customerDebit,
                "transactionCredit": customerCredit,
                "transactionPending": int(customerCredit) - int(customerDebit),
                "transactionContact": customerContact,
                "transactionAddress": customerAddress,
                "transactionAadharNumber": customerAadharNumber,
                "transactionPanNumber": customerPanNumber,
                "transactionBusiness": customerBusiness,
                "transactionCustomer": serializer.data['customerId']
            }
            serializer = TransactionHistorySerializer(data=transaction_dic)
            if (serializer.is_valid()):
                serializer.save()
            else:
                response_message = success.APIResponse(
                        404, "Unable to add to Transaction Model", {'error': None}).respond()
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
            customers_list = CustomersModel.objects.filter(
                customerBusiness=businessId)
            serializer = CustomersSerializer(customers_list, many=True)
            totalCredit = totalDebit = totalPending = 0
            totalDict = {}
            for i in range(len(serializer.data)):
                totalCredit += int(serializer.data[i]['customerCredit'])
                totalDebit += int(serializer.data[i]['customerDebit'])
                totalPending += int(serializer.data[i]['customerPending'])
            totalDict['totalCredit'] = totalCredit
            totalDict['totalDebit'] = totalDebit
            totalDict['totalPending'] = totalPending

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

            transactionCustomerObj = TransactionHistoryModel.objects.filter(
                transactionCustomer=customerId)
            transactionCustomerObj.update(
                transactionName=customerName, transactionContact=customerContact, transactionAddress=customerAddress, transactionAadharNumber=customerAadharNumber, transactionPanNumber=customerPanNumber)

            customerObj = CustomersModel.objects.filter(customerId=customerId)
            customerObj.update(customerName=customerName,
                               customerContact=customerContact, customerAddress=customerAddress, customerAadharNumber=customerAadharNumber, customerPanNumber=customerPanNumber)

            response_message = success.APIResponse(
                200, "Customer Updated Successfully", None).respond()
            # except:
            #     customerObj = CustomersModel.objects.filter(customerId=customerId)
            #     customerObj.update(customerName=customerName,
            #                     customerContact=customerContact)

            #     transactionObj = TransactionHistoryModel.objects.filter(
            #         transactionName=customerName, transactionContact=customerContact)
            #     transactionObj.update(
            #         transactionName=customerName, transactionContact=customerContact)

            #     response_message = success.APIResponse(
            #         200, "Customer Updated Successfully", None).respond()
        except CustomersModel.DoesNotExist:
            response_message = error.APIResponse(
                404, "Customer Does Not Exist", None).respond()

        except Exception as e:
            response_message = error.APIResponse(
                404, "Invalid CustomerId", {'error': str(e)}).respond()
        finally:
            return Response(response_message)
