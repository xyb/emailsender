from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import EmailSenderSerializer


class EmailSenderView(APIView):
    permission_classes = [AllowAny]
    serializer_class = EmailSenderSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request},
        )
        if serializer.is_valid(raise_exception=False):
            msg = serializer.validated_data
            send_mail(
                msg['subject'],
                msg['message'],
                settings.EMAIL_FROM,
                [msg['recipient_email']],
                html_message=msg['html_message'] or None,
            )

            return Response(
                serializer.validated_data['recipient_email'],
                status=status.HTTP_200_OK,
            )

        return Response(status=status.HTTP_401_UNAUTHORIZED)
