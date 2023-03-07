from django.core import mail
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TaskTest(APITestCase):
    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    @override_settings(EMAIL_FROM="xyb@test.com")
    def test_create_email(self):
        url = reverse("email-sender")
        data = {
            "subject": "hello from xyb",
            "message": "Welcome!",
            "recipient_email": "xyb@test.site",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'"xyb@test.site"')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'hello from xyb')
        self.assertEqual(mail.outbox[0].body, 'Welcome!')
        self.assertEqual(mail.outbox[0].from_email, 'xyb@test.com')
        self.assertEqual(mail.outbox[0].to, ['xyb@test.site'])
