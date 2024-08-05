# arquivo de teste
from django.test import TestCase, Client
from django.core import mail

class SendMailViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_send_mail_success(self):
        response = self.client.post('http://127.0.0.1:8000/sendmail/', {  
            'subject': 'Test Subject',
            'message': 'Test message',
            'to_email': 'test@example.com',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Mail sent successfully')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Test Subject')

    def test_send_mail_bad_header(self):
        response = self.client.post('http://127.0.0.1:8000/sendmail/', {  
            'subject': 'Test Subject\nBad Header',
            'message': 'Test message',
            'to_email': 'test@example.com',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Invalid header found.')
        self.assertEqual(len(mail.outbox), 0)

    def test_send_mail_missing_fields(self):
        response = self.client.post('http://127.0.0.1:8000/sendmail/', {  
            'subject': 'Test Subject',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Make sure all fields are entered and valid.')
        self.assertEqual(len(mail.outbox), 0)
