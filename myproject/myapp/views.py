from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponse
from .models import Account, Transaction
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
import logging

# Configure logging
logger = logging.getLogger(__name__)
handler = logging.FileHandler('transaction_errors.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.ERROR)

@transaction.atomic
def transfer_funds(request, from_account_id, to_account_id, amount):
    try:
        amount = Decimal(amount)
        sid = transaction.savepoint()
        
        from_account = Account.objects.select_for_update().get(id=from_account_id)
        to_account = Account.objects.select_for_update().get(id=to_account_id)
        
        if from_account.balance < amount:
            transaction.savepoint_rollback(sid)
            return HttpResponse("Insufficient funds")

        from_account.balance -= amount
        to_account.balance += amount

        from_account.save()
        to_account.save()

        # Log the transaction
        Transaction.objects.create(
            from_account=from_account,
            to_account=to_account,
            amount=amount,
            transaction_type='transfer'
        )

        transaction.savepoint_commit(sid)
        return HttpResponse("Transfer successful")

    except ObjectDoesNotExist:
        transaction.savepoint_rollback(sid)
        logger.error(f"Account not found: from_account_id={from_account_id}, to_account_id={to_account_id}")
        return HttpResponse("Account not found")
    except Exception as e:
        transaction.savepoint_rollback(sid)
        logger.error(f"Error during transfer: {str(e)}")
        return HttpResponse("An error occurred during the transfer")

@transaction.atomic
def deposit_funds(request, account_id, amount):
    try:
        amount = Decimal(amount)
        sid = transaction.savepoint()
        
        account = Account.objects.select_for_update().get(id=account_id)
        account.balance += amount
        account.save()

        # Log the transaction
        Transaction.objects.create(
            to_account=account,
            amount=amount,
            transaction_type='deposit'
        )

        transaction.savepoint_commit(sid)
        return HttpResponse("Deposit successful")
    except ObjectDoesNotExist:
        transaction.savepoint_rollback(sid)
        return HttpResponse("Account does not exist")
    except Exception as e:
        transaction.savepoint_rollback(sid)
        return HttpResponse(f"Error: {e}")

@transaction.atomic
def withdraw_funds(request, account_id, amount):
    try:
        amount = Decimal(amount)
        sid = transaction.savepoint()
        
        account = Account.objects.select_for_update().get(id=account_id)
        if account.balance < amount:
            transaction.savepoint_rollback(sid)
            return HttpResponse("Insufficient funds")

        account.balance -= amount
        account.save()

        # Log the transaction
        Transaction.objects.create(
            from_account=account,
            amount=amount,
            transaction_type='withdraw'
        )

        transaction.savepoint_commit(sid)
        return HttpResponse("Withdrawal successful")
    except ObjectDoesNotExist:
        transaction.savepoint_rollback(sid)
        return HttpResponse("Account does not exist")
    except Exception as e:
        transaction.savepoint_rollback(sid)
        return HttpResponse(f"Error: {e}")

def view_account(request, account_id):
    try:
        account = Account.objects.get(id=account_id)
        return HttpResponse(f"Account: {account.name}, Balance: {account.balance}")
    except ObjectDoesNotExist:
        return HttpResponse("Account does not exist")

def view_all_accounts(request):
    accounts = Account.objects.all()
    response = "\n".join([f"Account: {account.name}, Balance: {account.balance}" for account in accounts])
    return HttpResponse(response)

def view_transaction_history(request, account_id):
    try:
        account = Account.objects.get(id=account_id)
        transactions = Transaction.objects.filter(from_account=account) | Transaction.objects.filter(to_account=account)
        response = "\n".join([f"Transaction: {transaction.transaction_type}, Amount: {transaction.amount}" for transaction in transactions])
        return HttpResponse(response)
    except ObjectDoesNotExist:
        return HttpResponse("Account does not exist")

@transaction.atomic
def create_account(request):
    try:
        name = request.POST.get('name')
        initial_balance = Decimal(request.POST.get('initial_balance', '0.00'))
        
        account = Account.objects.create(name=name, balance=initial_balance)
        return HttpResponse(f"Account created: {account.name}, Balance: {account.balance}")
    except Exception as e:
        return HttpResponse(f"Error: {e}")

@transaction.atomic
def update_account(request, account_id):
    try:
        account = Account.objects.select_for_update().get(id=account_id)
        name = request.POST.get('name')
        if name:
            account.name = name
        balance = request.POST.get('balance')
        if balance:
            account.balance = Decimal(balance)
        account.save()
        return HttpResponse(f"Account updated: {account.name}, Balance: {account.balance}")
    except ObjectDoesNotExist:
        return HttpResponse("Account does not exist")
    except Exception as e:
        return HttpResponse(f"Error: {e}")

@transaction.atomic
def delete_account(request, account_id):
    try:
        account = Account.objects.select_for_update().get(id=account_id)
        account.delete()
        return HttpResponse("Account deleted")
    except ObjectDoesNotExist:
        return HttpResponse("Account does not exist")
    except Exception as e:
        return HttpResponse(f"Error: {e}")

def list_transactions(request):
    transactions = Transaction.objects.all()
    response = "\n".join([f"Transaction: {transaction.transaction_type}, Amount: {transaction.amount}, From: {transaction.from_account}, To: {transaction.to_account}" for transaction in transactions])
    return HttpResponse(response)