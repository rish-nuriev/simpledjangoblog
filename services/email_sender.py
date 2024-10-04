from django.core.mail import send_mail


def send(user_email, message=''):
    send_mail(
        'New Email from simplepythonblog!',
        message,
        'info@simplepythonblog.com',
        [user_email],
        fail_silently=False
    )
