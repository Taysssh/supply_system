from django.db import models
from django.utils import timezone

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    inn = models.CharField(max_length=12, unique=True)
    contact_info = models.TextField()

    def __str__(self):
        return self.name

class Buyer(models.Model):
    name = models.CharField(max_length=255)
    inn = models.CharField(max_length=12, unique=True)
    contact_info = models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Contract(models.Model):
    number = models.CharField(max_length=50, unique=True)
    date = models.DateField(default=timezone.now)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[('active', 'Активен'), ('closed', 'Закрыт')],
        default='active'
    )
    expiration_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Договор {self.number}"

class Invoice(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=50)
    invoice_date = models.DateField(default=timezone.now)
    products = models.ManyToManyField(Product, through='InvoiceProduct')
    file = models.FileField(upload_to='invoices/', null=True, blank=True)

    def total_amount(self):
        return sum(ip.subtotal() for ip in self.invoiceproduct_set.all())

class InvoiceProduct(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.unit_price