from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from account.models import Account
from invoice.models import Invoice, InvoiceItem


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ('invoice_id', 'quantity', 'product', 'price')


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ('account_id', 'order_id', 'items')

    items = InvoiceItemSerializer(many=True)

    def validate(self, attrs):
        items = attrs.get('items', [])
        total_price = sum([item.get('price') * item.get('quantity') for item in items])
        account = Account.objects.get(pk=attrs.get('account_id'))
        if account.balance < total_price:
            raise ValidationError
        return attrs


