from rest_framework import serializers

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


