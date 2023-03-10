from django.db import models
from account.models import Account


class Invoice(models.Model):
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    order_id = models.IntegerField()

    @property
    def total_price(self):
        return self.items.aggregate(models.Sum('price'))


class InvoiceItem(models.Model):
    invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField()
    product = models.CharField(max_length=100)
    price = models.IntegerField()
