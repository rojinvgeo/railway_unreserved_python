from django.core.mail import send_mail
import uuid
from django.conf import settings

# def send_forgot_password_mail(email,token):
#     subject='Your Forgot Password Link'
#     message= f'Hi,click on the link to reset your password http://127.0.0.1:8000/change_password/{token}/'
#     email_from=settings.Email_HOST_USER
#     recipient_list=[email]
#     send_mail(subject,message,email_from,recipient_list)
#     return True