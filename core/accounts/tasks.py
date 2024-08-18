import random
import logging
from mail_templated import EmailMessage
from celery import shared_task
from django.core.cache import cache
from accounts.models.users import User

logger = logging.getLogger(__name__)


@shared_task
def send_verification_code_task(user_id):
    try:
        user = User.objects.get(id=user_id)  
        verification_code = str(random.randint(10000, 99999))
        cache.set(str(user.id), verification_code, 120)
        email_obj = EmailMessage(
            "email/activation_email.tpl",
            {"verification_code": verification_code},
            "admin@admin.com",
            to=[user.email],
        )
        email_obj.send()
        logger.info(
            f"Sent activation email to {user.email} with verification code {verification_code}"
        )
        return True
    except User.DoesNotExist:
        logger.error(f"User with id {user_id} does not exist.")
        return False
    except Exception as e:
        logger.error(f"Failed to send activation email: {str(e)}")
        return False
