from django.db import models
from django.db.models import F

from account.models import Account


class Invoice(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='invoices')
    order_id = models.IntegerField()

    @property
    def total_price(self):
        return self.items.aggregate(models.Sum(F('price')) * F('quantity'))

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        Account.objects.filter(pk=self.account_id).update(balance=F('balance') - self.total_price)
        return super().save(force_insert, force_update, using, update_fields)


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField()
    product = models.CharField(max_length=100)
    price = models.IntegerField()
