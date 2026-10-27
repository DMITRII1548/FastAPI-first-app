from fastapi import HTTPException

from app.database import SessionLocal
from app.repository import wallet as wallet_repository
from app.schemas import CreateWalletRequest

def get_wallet(wallet_name: str | None = None):
    db = SessionLocal()

    try:
        if wallet_name is None:
            wallets = wallet_repository.get_all_wallets(db)
            return {"total_balance": sum(w.amount for w in wallets)}

        if not wallet_repository.is_wallet_exists(db, wallet_name):
            raise HTTPException(
                status_code=404,
                detail=f"Wallet '{wallet_name}' not found"
            )

        balance = wallet_repository.get_wallet_balance_by_name(db, wallet_name)

        return {
            "Wallet": wallet_name,
            "balance:": balance
        }
    finally:
        db.close()

def create_wallet(wallet: CreateWalletRequest):
    db = SessionLocal()

    try:
        if wallet_repository.is_wallet_exists(db, wallet.name):
            raise HTTPException(
                status_code=400,
                detail=f"Wallet '{wallet.name}' already exists"
            )

        wallet = wallet_repository.create_wallet(db, wallet.name, wallet.initial_balance)

        db.commit()

        return {
            "message": f"Wallet '{wallet.name}' created",
            "wallet": wallet.name,
            "balance": wallet.amount
        }
    finally:
        db.close()