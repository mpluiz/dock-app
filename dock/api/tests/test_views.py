import json
from datetime import datetime

import pytest
from rest_framework import status

from dock.core.models import Account, Customer, Transaction


@pytest.fixture()
def one_account():
    customer = Customer.objects.create(
        name='Marcos Paulo', document_id='41618789821', birth_date='1995-03-02'
    )
    return Account.objects.create(customer=customer, type=1)


@pytest.fixture()
def one_transaction(one_account):
    return Transaction.objects.create(
        account=one_account,
        amount=100,
        operation=Transaction.TransactionType.DEPOSIT.value,
    )


def create_transaction_with_date(account, date):
    transaction = Transaction.objects.create(
        account=account,
        amount=100,
        operation=Transaction.TransactionType.DEPOSIT.value,
    )

    transaction.created_at = date
    transaction.save()
    return transaction


def test_should_create_account(api_client):
    account_body = json.dumps(
        {
            'daily_withdrawal_limit': 100,
            'type': Account.AccountType.SAVINGS.value,
            'customer': {
                'birth_date': '1995-03-02',
                'document_id': '41618789821',
                'name': 'Marcos Paulo',
            },
        }
    )

    response = api_client.post(
        '/api/v1/accounts/',
        data=account_body,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert Account.objects.exists()


def test_should_make_deposit(api_client, one_account):
    deposit_body = json.dumps({'amount': 100})

    response = api_client.post(
        f'/api/v1/accounts/{one_account.id}/deposit/',
        data=deposit_body,
        content_type='application/json',
    )

    one_account.refresh_from_db()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert one_account.balance == 100


def test_should_make_withdraw(api_client, one_account):
    one_account.balance = 199.9
    one_account.daily_withdrawal_limit = 200
    one_account.save()

    withdraw_body = json.dumps({'amount': 99.9})

    response = api_client.post(
        f'/api/v1/accounts/{one_account.id}/withdraw/',
        data=withdraw_body,
        content_type='application/json',
    )

    one_account.refresh_from_db()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert one_account.balance == 100


def test_should_return_withdraw_limit_reached(api_client, one_account):
    one_account.daily_withdrawal_limit = 200
    one_account.save()

    withdraw_body = json.dumps({'amount': 200.1})

    response = api_client.post(
        f'/api/v1/accounts/{one_account.id}/withdraw/',
        data=withdraw_body,
        content_type='application/json',
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {'message': 'withdraw limit reached'}


def test_should_return_account_details(api_client, one_account):
    response = api_client.get(f'/api/v1/accounts/{one_account.id}/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'active': True,
        'balance': 0.0,
        'customer': {
            'birth_date': '1995-03-02',
            'document_id': '41618789821',
            'name': 'Marcos Paulo',
        },
        'daily_withdrawal_limit': 0.0,
        'type': Account.AccountType.CHECKING.label,
    }


def test_should_deactivate_account(api_client, one_account):
    response = api_client.patch(f'/api/v1/accounts/{one_account.id}/deactivate/')

    one_account.refresh_from_db()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert one_account.active is False


def test_should_activate_account(api_client, one_account):
    one_account.active = False
    one_account.save()

    response = api_client.patch(f'/api/v1/accounts/{one_account.id}/activate/')

    one_account.refresh_from_db()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert one_account.active is True


def test_should_return_account_transactions(api_client, one_transaction):
    response = api_client.get(
        f'/api/v1/accounts/{one_transaction.account.id}/transactions/'
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "account": one_transaction.account.id,
            "amount": 100,
            "operation": Transaction.TransactionType.DEPOSIT.label,
            "transaction_date": one_transaction.created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        }
    ]


def test_should_return_account_transactions_by_period(api_client, one_account):
    create_transaction_with_date(one_account, datetime(2021, 1, 1)),
    create_transaction_with_date(one_account, datetime(2021, 1, 2)),
    create_transaction_with_date(one_account, datetime(2021, 1, 3)),
    create_transaction_with_date(one_account, datetime(2021, 1, 4)),
    create_transaction_with_date(one_account, datetime(2021, 1, 5)),

    query_params = '?start_date=2021-01-02&end_date=2021-01-04'
    response = api_client.get(
        f'/api/v1/accounts/{one_account.id}/transactions/{query_params}'
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3
