from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import EmailSenderSerializer


def send_mail(subject, message, html_message, from_email, to, cc, bcc):
    email = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=from_email,
        to=[to],
        cc=[cc],
        bcc=[bcc],
    )
    if html_message:
        email.attach_alternative(html_message, 'text/html')
    return email.send()


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
                subject=msg['subject'],
                message=msg['message'],
                html_message=msg.get('html_message') or None,
                from_email=settings.EMAIL_FROM,
                to=msg['recipient_email'],
                cc=msg.get('cc'),
                bcc=msg.get('bcc'),
            )

            return Response(
                serializer.validated_data['recipient_email'],
                status=status.HTTP_200_OK,
            )

        return Response(status=status.HTTP_401_UNAUTHORIZED)
