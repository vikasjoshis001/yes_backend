from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from requirements import success, error


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        try:
            response = super(LoginView, self).post(request, *args, **kwargs)
            token = Token.objects.get(key=response.data['token'])
            response_message = success.APIResponse(
                200, "Successfull Login", {'token': token.key}).respond()
            return Response(response_message)
            
        except Exception as e:
            response_message = error.APIResponse(
                404, "Invalid Credentials", {'error': str(e)}).respond()
            return Response(response_message)
