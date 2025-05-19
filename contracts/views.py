from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from openpyxl import Workbook
from .models import Contract
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

def generate_pdf(request, contract_id):
    contract = Contract.objects.get(id=contract_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=contract_{contract.number}.pdf'

    font_path = "contracts/fonts/DejaVuSans.ttf"
    pdfmetrics.registerFont(TTFont('DejaVu', font_path))

    p = canvas.Canvas(response)
    p.setFont("DejaVu", 12)
    p.drawString(100, 750, f"Номер договора: {contract.number}")
    p.drawString(100, 730, f"Поставщик: {contract.supplier.name}")
    p.showPage()
    p.save()
    return response

def export_to_excel(request):
    contracts = Contract.objects.all()
    wb = Workbook()
    ws = wb.active
    ws.append(['Номер', 'Поставщик', 'Покупатель', 'Статус'])

    for contract in contracts:
        ws.append([
            contract.number,
            contract.supplier.name,
            contract.buyer.name,
            contract.status
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=contracts.xlsx'
    wb.save(response)
    return response

@shared_task
def check_contract_expiration():
    expired = Contract.objects.filter(expiration_date__lt=timezone.now(), status='active')
    for contract in expired:
        send_mail(
            f'Договор истекает: {contract.number}',
            f'Договор {contract.number} истекает {contract.expiration_date}',
            'from@example.com',
            ['to@example.com'],
            fail_silently=False,
        )
        contract.status = 'closed'
        contract.save()