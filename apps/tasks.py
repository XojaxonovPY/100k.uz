from celery import shared_task
from django.core.mail import send_mail

from root.settings import EMAIL_HOST_USER


@shared_task
def send_email(message: str, recipient_list: list[str]):
    try:
        send_mail(
            subject="Verification Code !!!",
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=False
        )
        return "✅ Email muvaffaqiyatli yuborildi."
    except Exception as e:
        return f"❌ Email yuborishda xatolik: {str(e)}"
