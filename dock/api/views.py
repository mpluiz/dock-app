from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from dock.api import serializers
from dock.core.services import AccountService, TransactionService


class AccountCreate(GenericAPIView):
    serializer_class = serializers.AccountCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_service = AccountService()
        customer = serializer.data['customer']
        account_type = serializer.data['type']
        daily_withdrawal_limit = serializer.data['daily_withdrawal_limit']
        account_service.create(
            customer=customer,
            account_type=account_type,
            daily_withdrawal_limit=daily_withdrawal_limit,
        )
        return Response(status=status.HTTP_201_CREATED)


class AccountDeposit(GenericAPIView):
    serializer_class = serializers.AccountAmountSerializer

    def post(self, request, account_id):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_service = AccountService()
        account_service.deposit(account_id=account_id, **serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AccountWithdraw(GenericAPIView):
    serializer_class = serializers.AccountAmountSerializer

    def post(self, request, account_id):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_service = AccountService()
        account_service.withdraw(account_id=account_id, **serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AccountDetails(GenericAPIView):
    serializer_class = serializers.AccountDetailsSerializer

    def get(self, request, account_id):
        account_service = AccountService()
        account = account_service.get_by_id(account_id=account_id)
        account = self.serializer_class(account)
        return Response(data=account.data, status=status.HTTP_200_OK)


class AccountDeactivate(GenericAPIView):
    def patch(self, request, account_id):
        account_service = AccountService()
        account_service.deactivate(account_id=account_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AccountActivate(GenericAPIView):
    def patch(self, request, account_id):
        account_service = AccountService()
        account_service.activate(account_id=account_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AccountTransactions(GenericAPIView):
    serializer_class = serializers.TransactionSerializer

    def get(self, request, account_id):
        transaction_service = TransactionService()
        query_params = request.query_params
        transactions = transaction_service.get_by_account_id(
            account_id=account_id, query_params=query_params
        )
        transactions_serialized = self.serializer_class(transactions, many=True)
        return Response(transactions_serialized.data, status=status.HTTP_200_OK)
