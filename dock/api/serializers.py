from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from dock.core.models import Customer, Account, Transaction


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = ('name', 'document_id', 'birth_date')


class AccountCreateSerializer(ModelSerializer):
    customer = CustomerSerializer(required=True)

    class Meta:
        model = Account
        fields = ('daily_withdrawal_limit', 'type', 'customer')


class AccountAmountSerializer(ModelSerializer):
    amount = serializers.FloatField(required=True)

    class Meta:
        model = Account
        fields = ('amount',)


class AccountDetailsSerializer(ModelSerializer):
    customer = CustomerSerializer(required=True)
    type = serializers.CharField(source='get_type_display')

    class Meta:
        model = Account
        fields = ('customer', 'balance', 'daily_withdrawal_limit', 'active', 'type')


class TransactionSerializer(ModelSerializer):
    operation = serializers.CharField(source='get_operation_display')
    transaction_date = serializers.DateTimeField(
        source='created_at', format='%Y-%m-%d %H:%M:%S'
    )

    class Meta:
        model = Transaction
        fields = ('account', 'amount', 'operation', 'transaction_date')
