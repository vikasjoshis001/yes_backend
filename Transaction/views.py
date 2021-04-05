import csv
import os
import pandas as pd
from datetime import datetime
import shutil

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from yes_backend.settings import sheetsFolder, sheetsFolderPath, sheetsCustomers,currentPath

from requirements import success, error
from Customers.models import CustomersModel,SavePdf,YesMultiServicesLogo
from Customers.serializers import CustomersSerializer,SavePdfSerializer,YesMultiServicesLogoSerializer
from Business.models import BusinessModel
from .models import TransactionHistoryModel
from .serializers import TransactionHistorySerializer

# PDF
from Customers.utils import render_to_pdf
from io import BytesIO
from django.core.files import File
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

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
            customerObj = CustomersModel.objects.get(
                customerId=transactionCustomer)
            customerName = customerObj.customerName
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
            totalDict['customerName'] = customerName
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
            path = os.path.join(newPath, name)
            if not os.path.exists(path):
                os.mkdir(path)
            newPath = path
            filename = newPath + "/" + name + \
                " Transaction History - " + datetime.now().strftime("%d%m%Y%H%M%S") + ".csv"
            row_list = [["Date", "Name", "Credit", "Debit", "Pending"],
                        [None, None, None, None, None]]
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(row_list)

            for transact in transaction:
                newDate = transact['transactionDate'] + " (" + transact['transactionTime'] +" )"
                dic = {
                    "Date": newDate,
                    "Name": transact['transactionName'],
                    "Credit": transact['transactionCredit'],
                    "Debit": transact['transactionDebit'],
                    "Pending": transact['transactionPending'],
                }
                totalCredit += int(transact['transactionCredit'])
                totalDebit += int(transact['transactionDebit'])

                row_list = [[dic['Date'], dic['Name'],
                             dic['Credit'], dic['Debit'], dic['Pending']]]
                with open(filename, 'a') as file:
                    writer = csv.writer(file)
                    writer.writerows(row_list)
            totalPending = totalCredit-totalDebit
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


class CreateTransactionPdf(APIView):
    """ API for Creating Pdf of Grades and SGPA"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        transaction_list = request.data
        my_list = transaction_list['transactionHistory']
        customerName = my_list[0]['transactionName']
        business = my_list[0]['transactionBusiness']
        businessObj = BusinessModel.objects.get(businessId=business)
        businessName = businessObj.businessName
        totalCredit = totalDebit = totalPending = 0
        for transact in my_list:
            totalCredit += int(transact['transactionCredit'])
            totalDebit += int(transact['transactionDebit'])
        totalPending = int(totalCredit) - int(totalDebit)
        # Getting gradify logo
        local_url = "http://localhost:8000/media/"
        yes_logo = YesMultiServicesLogo.objects.get(imageId=1)
        my_logo = local_url+str(yes_logo.imageLogo)
        transaction_list['logo'] = my_logo
        transaction_list['totalCredit'] = totalCredit
        transaction_list['totalDebit'] = totalDebit
        transaction_list['totalPending'] = totalPending
        transaction_list['customerName'] = customerName

       #  Creating Pdf
        try:
            # Generating Pdf
            pdf = render_to_pdf('pdf/transaction.html', transaction_list)
            my_filename = customerName + " - Transaction History - " + datetime.now().strftime("%d%m%Y%H%M%S")+".pdf"
            dic = {
                "filename": my_filename
            }

            # Saving filename
            serializers = SavePdfSerializer(data=dic)
            if(serializers.is_valid()):
                serializers.save()
            my_pdf = SavePdf.objects.filter(filename=my_filename)[0]
            output_file = PdfFileWriter()
            input_file = PdfFileReader(File(BytesIO(pdf.content)))

            # Adding Page no, website name and greetings in file
            for page in range(input_file.getNumPages()):
                tmp = BytesIO()
                can = canvas.Canvas(tmp, pagesize=A4)
                can.setFont('Times-Roman', 10)
                can.drawString(25, 20, "Yes Multiservices")
                can.drawString(290, 20, "***")
                can.drawString(525, 20, "Page " + str(page + 1))
                can.save()
                tmp.seek(0)
                watermark = PdfFileReader(tmp)
                watermark_page = watermark.getPage(0)
                pdf_page = input_file.getPage(page)
                pdf_page.mergePage(watermark_page)
                output_file.addPage(pdf_page)
            tmp = BytesIO()
            output_file.write(tmp)

            # Saving Pdf
            my_pdf.pdf_file.save(my_filename, File(tmp))
            my_pdf = SavePdf.objects.filter(filename=my_filename)[0]
            serializer = SavePdfSerializer(my_pdf)
            transaction_list['pdf'] = serializer.data['pdf_file']

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
            pdfPath = currentPath + transaction_list['pdf']
            shutil.copy(pdfPath, newPath)
            dic = {
                "Type": "Success",
                "msg": "Pdf genereted successfully",
                "data": transaction_list['pdf']
            }
            return Response(data=dic)
        except:
            dic = {
                "Type": "Error",
                "msg": "Unable to Create pdf",
                "data": None
            }
            return Response(data=dic)
