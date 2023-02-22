from django.conf import settings
from django.core.validators import RegexValidator
from rest_framework import serializers


class EmailSenderSerializer(serializers.Serializer):
    email_regex = RegexValidator(
        regex=settings.EMAIL_WHITE_LIST,
        message=settings.EMAIL_WHITE_LIST_MESSAGE,
    )
    subject = serializers.CharField(required=True, help_text='required')
    message = serializers.CharField(required=True, help_text='required')
    recipient_email = serializers.EmailField(
        validators=[email_regex],
        help_text='required',
    )
    cc = serializers.EmailField(
        required=False,
        validators=[email_regex],
        help_text='not required',
    )
    bcc = serializers.EmailField(
        required=False,
        validators=[email_regex],
        help_text='not required',
    )
    html_message = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text='not required',
    )

    class Meta:
        fields = ['receipient_email', 'subject', 'cc', 'bcc', 'message',
                  'html_message']
