from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email(subject, message, from_email, recipient_list, fail_silently=False):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=fail_silently
        )
        return "✅ Email muvaffaqiyatli yuborildi."
    except Exception as e:
        return f"❌ Email yuborishda xatolik: {str(e)}"
