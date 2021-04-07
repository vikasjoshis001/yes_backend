from Customers.models import CustomersModel
import os

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from yes_backend.settings import sheetsFolderPath, sheetsFolder

from requirements import success, error
from .models import BusinessModel
from Customers.models import CustomersModel
from .serializers import BusinessSerializer

# Create your views here.

# Add Business Api


class AddBusinessView(APIView):
    """Api for Adding Business"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        businessName = request.data.get('businessName')
        try:
            path = sheetsFolderPath + "/" + sheetsFolder
            if not os.path.exists(path):
                path = os.path.join(sheetsFolderPath, sheetsFolder)
                os.mkdir(path)
            newPath = os.path.join(sheetsFolderPath, sheetsFolder)
            dic = {
                "businessName": businessName
            }
            serializer = BusinessSerializer(data=dic)
            if (serializer.is_valid()):
                serializer.save()
                myFolder = businessName
                path = os.path.join(newPath, myFolder)
                os.mkdir(path)
                response_message = success.APIResponse(200, "Business Added Successfully", {
                    "businessName": dic}).respond()
            else:
                response_message = error.APIResponse(404, "Unable to add Business due to invalid serializer", {
                    'error': None}).respond()
        except Exception as e:
            response_message = error.APIResponse(404, "Unable to add Business", {
                                                 'error': str(e)}).respond()
        finally:
            return Response(response_message)


# Get Business Api
class GetBusinessView(generics.ListCreateAPIView):
    """Api for Getting Businesses"""

    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        try:
            businessList = BusinessModel.objects.all()
            serializer = BusinessSerializer(businessList, many=True)
            response_message = success.APIResponse(200, "List of All Businesses", {
                                                   "businessList": serializer.data}).respond()
        except Exception as e:
            response_message = error.APIResponse(404, "Unable to list Businesses", {
                                                 'error': str(e)}).respond()
        finally:
            return Response(response_message)

# Delete Business Api


class DeleteBusinessView(APIView):
    """Api for Delete Business"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        businessId = request.query_params['businessId']
        try:
            businessObj = BusinessModel.objects.get(businessId=businessId)
            if businessObj:
                businessObj.delete()
                response_message = success.APIResponse(
                    200, "Business Deleted Successfully", None).respond()
            else:
                response_message = error.APIResponse(
                    404, "Invalid BusinessId", None).respond()
        except Exception as e:
            response_message = error.APIResponse(
                404, "Invalid BusinessId", None).respond()
        finally:
            return Response(response_message)

# Update Business Api


class EditBusinessView(generics.CreateAPIView):
    ''' Api for Update Business '''

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            businessId = request.data.get("businessId")
            businessName = request.data.get("businessName")

            businessObjFolder = BusinessModel.objects.get(
                businessId=businessId)
            businessObj = BusinessModel.objects.filter(businessId=businessId)
            if (businessObj):
                previousFolder = sheetsFolderPath+"/" + \
                    sheetsFolder + "/" + businessObjFolder.businessName
                businessObj.update(businessName=businessName)
                renamedFolder = sheetsFolderPath+"/" + sheetsFolder + "/" + businessName
                os.rename(previousFolder, renamedFolder)
                response_message = success.APIResponse(
                    200, "Business Updated Successfully", None).respond()
            else:
                response_message = error.APIResponse(
                    404, "Invalid BusinessId", None).respond()
        except Exception as e:
            response_message = error.APIResponse(
                404, "Invalid BusinessId", None).respond()
        finally:
            return Response(response_message)
        
        
class BusinessManagement(APIView):
        permission_classes = [IsAuthenticated]
        
        def get(self,request):
            businessId = request.query_params['businessId']
            totalCredit = totalDebit = totalPending = 0;
            try:
                businessList = CustomersModel.objects.filter(customerBusiness = businessId)
                businessList = businessList.values()
                businessObj  = BusinessModel.objects.get(businessId=businessId)
                businessName = businessObj.businessName
                totalDic = {}
                for i in range(len(businessList)):
                    totalCredit += int(businessList[i]['customerCredit'])
                    totalDebit += int(businessList[i]['customerDebit'])
                    totalPending += int(businessList[i]['customerPending'])
                totalDic['totalCredit'] = totalCredit
                totalDic['totalDebit'] = totalDebit
                totalDic['totalPending'] = totalPending
                totalDic['businessName'] = businessName
                response_message = success.APIResponse(200, "List of All Finance", {
                                                    "totalList": totalDic}).respond()
            except Exception as e:
                response_message = error.APIResponse(404, "Unable to list Finance", {
                                                    'error': str(e)}).respond()
            finally:
                return Response(response_message)

