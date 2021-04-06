from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


# Email
from django.core.mail import EmailMessage

# Create your views here.

# Api for backup Database


class BackUpDataBase(APIView):
    """ Api for backup database """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            subject = "Database  Backup of Yes MultiServices"
            message = ""
            recipient_list = ['vikasjoshis001@gmail.com','crunchbase.io@gmail.com']
            email = EmailMessage(
                subject, message, 'crunchbase.io@gmail.com', recipient_list)
            email.attach_file("./db.sqlite3")
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
