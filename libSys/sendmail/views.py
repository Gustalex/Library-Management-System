from django.core.mail import BadHeaderError, send_mail as django_send_mail
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from decouple import config

@csrf_exempt
def send_mail(request):
    subject = request.POST.get("subject", "")
    message = request.POST.get("message", "")
    to_email = request.POST.get("to_email", "")
    from_email = config("EMAIL_HOST_USER")

    if subject and message and from_email and to_email:
        try:
            django_send_mail(subject, '', from_email, [to_email], html_message=message)
        except BadHeaderError:
            return HttpResponse("Invalid header found.")
        return HttpResponse("Mail sent successfully")
    else:
        return HttpResponse("Make sure all fields are entered and valid.")