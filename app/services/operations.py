from fastapi import HTTPException

from app.database import SessionLocal
from app.schemas import OperationRequest
from app.repository import wallet as wallet_repository

def add_income(operation: OperationRequest):
    db = SessionLocal()

    try:
        if not wallet_repository.is_wallet_exists(db, operation.wallet_name):
            raise HTTPException(
                status_code=404,
                detail=f"Wallet '{operation.wallet_name}' not found"
            )

        wallet = wallet_repository.add_income(db, operation.wallet_name, operation.amount)

        db.commit()

        return {
            "message": "Income added",
            "wallet": operation.wallet_name,
            "amount": operation.amount,
            "description": operation.description,
            "new_balance": wallet.amount
        }
    finally:
        db.close()

def add_expense(operation: OperationRequest):
    db = SessionLocal()
    try:
        if not wallet_repository.is_wallet_exists(db, operation.wallet_name):
            raise HTTPException(
                status_code=404,
                detail=f"Wallet '{operation.wallet_name}' not found"
            )

        balance = wallet_repository.get_wallet_balance_by_name(db, operation.wallet_name)

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


        wallet = wallet_repository.add_expense(db, operation.wallet_name, operation.amount)

        db.commit()

        return {
            "message": "Expense Added",
            "wallet": operation.wallet_name,
            "amount": operation.amount,
            "description": operation.description,
            "new_balance": wallet.amount
        }
    finally:
        db.close()