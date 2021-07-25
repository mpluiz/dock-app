from datetime import date

from rest_framework import status
from rest_framework.exceptions import APIException

from dock.core.models import Account, Customer, Transaction


class CustomerService:
    def create(self, *, name: str, document_id: str, birth_date: str) -> Customer:
        customer = Customer(name=name, document_id=document_id, birth_date=birth_date)
        customer.full_clean()
        customer.save()
        return customer


class AccountService:
    def create(
        self, *, customer: dict, account_type: int, daily_withdrawal_limit: float = 0
    ) -> Account:
        customer_service = CustomerService()
        customer = customer_service.create(**customer)
        account = Account(
            customer=customer,
            daily_withdrawal_limit=daily_withdrawal_limit,
            type=account_type,
        )
        account.full_clean()
        account.save()
        return account

    def deposit(self, *, account_id: int, amount: float):
        account = self.get_by_id(account_id=account_id)
        account.balance = round(account.balance + amount, 2)
        account.save()

        transaction_service = TransactionService()
        transaction_service.create(
            account=account,
            amount=amount,
            operation=Transaction.TransactionType.DEPOSIT,
        )

    def withdraw(self, *, account_id: int, amount: float):
        account = self.get_by_id(account_id=account_id)

        self.check_withdraw_limit(account=account, amount=amount)

        account.balance = round(account.balance - amount, 2)
        account.save()

        transaction_service = TransactionService()
        transaction_service.create(
            account=account,
            amount=amount,
            operation=Transaction.TransactionType.WITHDRAW,
        )

    def deactivate(self, *, account_id: int):
        account = self.get_by_id(account_id=account_id)
        account.active = False
        account.save()

    def activate(self, *, account_id: int):
        account = self.get_by_id(account_id=account_id)
        account.active = True
        account.save()

    def get_by_id(self, *, account_id: int) -> Account:
        return Account.objects.get(pk=account_id)

    def check_withdraw_limit(self, *, account: Account, amount: float):
        today = date.today()
        total_amount = amount

        transactions = Transaction.objects.filter(
            account=account,
            operation=Transaction.TransactionType.WITHDRAW,
            created_at__year=today.year,
            created_at__month=today.month,
            created_at__day=today.day,
        )

        for transaction in transactions:
            total_amount += transaction.amount

        if total_amount > account.daily_withdrawal_limit:
            raise WithdrawLimitError


class TransactionService:
    def create(
        self, *, account: Account, amount: float, operation: Account.AccountType.choices
    ) -> Transaction:
        transaction = Transaction(account=account, amount=amount, operation=operation)
        transaction.full_clean()
        transaction.save()
        return transaction

    def get_by_account_id(self, *, account_id: int, query_params=None):
        if query_params:
            return Transaction.objects.filter(
                account__pk=account_id,
                created_at__gte=query_params.get('start_date'),
                created_at__lte=query_params.get('end_date'),
            )

        return Transaction.objects.filter(account__pk=account_id)


class WithdrawLimitError(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = {'message': 'withdraw limit reached'}
