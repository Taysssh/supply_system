from django.contrib import admin
from .models import Contract, Supplier, Buyer, Product, Invoice, InvoiceProduct
from django.http import HttpResponse  # Импортируем здесь
import openpyxl
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# ==== Регистрация моделей ====
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'inn']

@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ['name', 'inn']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit', 'price']

class InvoiceProductInline(admin.TabularInline):
    model = InvoiceProduct
    extra = 1

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceProductInline]
    list_display = ['invoice_number', 'invoice_date']

# ==== Кастомные действия ====
class ContractAdmin(admin.ModelAdmin):
    list_display = ['number', 'supplier', 'buyer', 'status']
    actions = ['export_to_excel', 'generate_pdf']

    def export_to_excel(self, request, queryset):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(['ID', 'Номер', 'Поставщик', 'Покупатель', 'Статус'])

        for contract in queryset:
            ws.append([
                contract.id,
                contract.number,
                contract.supplier.name,
                contract.buyer.name,
                contract.status
            ])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=contracts_{timezone.now().date()}.xlsx'
        wb.save(response)
        return response
    export_to_excel.short_description = "Экспорт в Excel"

    def generate_pdf(self, request, queryset):
        contract = queryset.first()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=contract_{contract.number}.pdf'

        # Путь к шрифту
        font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'DejaVuSans.ttf')
        
        try:
            pdfmetrics.registerFont(TTFont('DejaVu', font_path))
        except Exception as e:
            return HttpResponse(f"Ошибка загрузки шрифта: {e}", status=500)

        p = canvas.Canvas(response)
        p.setFont("DejaVu", 12)

        p.drawString(100, 750, f"Номер договора: {contract.number}")
        p.drawString(100, 730, f"Поставщик: {contract.supplier.name}")
        p.drawString(100, 710, f"Дата заключения: {contract.date}")
        p.drawString(100, 690, f"Дата окончания: {contract.expiration_date}")
        p.drawString(100, 670, f"Статус: {contract.status}")

        p.showPage()
        p.save()
        return response
    generate_pdf.short_description = "Сгенерировать PDF"

admin.site.register(Contract, ContractAdmin)