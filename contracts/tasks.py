from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Contract

@shared_task
def check_contract_expiration():
    expired = Contract.objects.filter(expiration_date__lt=timezone.now(), status='active')
    for contract in expired:
        send_mail(
            'Договор истекает',
            f'Договор {contract.number} истекает {contract.expiration_date}',
            'from@example.com',
            ['to@example.com'],
            fail_silently=False,
        )
        contract.status = 'closed'
        contract.save()