from django.db import models


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(Base):
    name = models.CharField(max_length=128)
    document_id = models.CharField(max_length=11)
    birth_date = models.DateField()


class Account(Base):
    class AccountType(models.IntegerChoices):
        CHECKING = 1, 'Conta Corrente'
        SAVINGS = 2, 'Conta Poupança'
        SALARY = 3, 'Conta Salário'

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    balance = models.FloatField(default=0.0)
    daily_withdrawal_limit = models.FloatField(default=0.0)
    active = models.BooleanField(default=True)
    type = models.PositiveSmallIntegerField(choices=AccountType.choices)


class Transaction(Base):
    class TransactionType(models.IntegerChoices):
        DEPOSIT = 1, 'Depósito'
        WITHDRAW = 2, 'Saque'

    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    amount = models.FloatField()
    operation = models.PositiveSmallIntegerField(choices=TransactionType.choices)
