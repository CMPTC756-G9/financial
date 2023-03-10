from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from account.models import Account
from account.serializers import AccountSerializer
from invoice.serializers import InvoiceSerializer


class AccountViewset(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
# order_id, user_id, a list of price, quantity, product

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        user_id = request.data.pop('user_id')
        try:
            account = Account.objects.get(user_id=user_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            invoice = serializer.save()
            Account.objects.filter(pk=account.pk).update(balance=F('balance')-invoice.total_price)
            account.balance = account.balance-invoice.total_price
            account.save()
            return Response({'status': 'paid'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
