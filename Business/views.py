from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from requirements import success, error
from .models import BusinessModel
from .serializers import BusinessSerializer

# Create your views here.

# Add Business Api


class AddBusinessView(APIView):
    """Api for Adding Business"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        businessName = request.data.get("businessName")
        try:
            dic = {
                "businessName": businessName
            }
            serializer = BusinessSerializer(data=dic)
            if (serializer.is_valid()):
                serializer.save()
            response_message = success.APIResponse(200, "Business Added Successfully", {
                                                   "businessName": businessName}).respond()
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
            business_list = BusinessModel.objects.all()
            serializer = BusinessSerializer(business_list, many=True)
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
                    404, "Authentication Failed", None).respond()

        except BusinessModel.DoesNotExist:
            response_message = error.APIResponse(
                404, "Bussiness Does Not Exist", None).respond()

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

            businessObj = BusinessModel.objects.filter(businessId=businessId)
            businessObj.update(businessName=businessName)
            response_message = success.APIResponse(
                200, "Business Updated Successfully", None).respond()
        except BusinessModel.DoesNotExist:
            response_message = error.APIResponse(
                404, "Bussiness Does Not Exist", None).respond()

        except Exception as e:
            response_message = error.APIResponse(
                404, "Invalid BusinessId", None).respond()
        finally:
            return Response(response_message)
