from fastapi import HTTPException
from app.schemas import OperationRequest
from app.repository import wallet as wallet_repository

def add_income(operation: OperationRequest):
    if not wallet_repository.is_wallet_exists(operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found"
        )

    new_balance = wallet_repository.add_income(operation.wallet_name, operation.amount)

    return {
        "message": "Income added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": new_balance
    }


def add_expense(operation: OperationRequest):
    if not wallet_repository.is_wallet_exists(operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found"
        )

    balance = wallet_repository.get_wallet_balance_by_name(operation.wallet_name)

    if operation.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount must be positive"
        )


    if operation.amount > balance:
        raise HTTPException(
            status_code=400,
            detail="Not enough balance"
        )


    new_balance = wallet_repository.add_expense(operation.wallet_name, operation.amount)

    return {
        "message": "Expense Added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": new_balance
    }