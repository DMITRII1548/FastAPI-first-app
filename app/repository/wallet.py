from decimal import Decimal

from app.database import SessionLocal
from app.models import Wallet
from sqlalchemy.orm import Session

def is_wallet_exists(db: Session, wallet_name: str) -> bool:
    return db.query(Wallet).filter(Wallet.name == wallet_name).first() is not None

def add_expense(db: Session, wallet_name: str, amount: Decimal) -> Wallet:
    wallet = db.query(Wallet).filter(Wallet.name == wallet_name).first()
    wallet.amount -= amount
    return wallet

def add_income(db: Session, wallet_name: str, amount: Decimal) -> Wallet:
    wallet = db.query(Wallet).filter(Wallet.name == wallet_name).first()
    wallet.amount += amount
    return wallet

def get_wallet_balance_by_name(db: Session, wallet_name: str) -> Decimal:
    wallet = db.query(Wallet).filter(Wallet.name == wallet_name).first()
    return wallet.amount

def get_all_wallets(db: Session) -> list[Wallet]:
    return db.query(Wallet).all()

def create_wallet(db: Session, wallet_name: str, amount: Decimal) -> Wallet:
    wallet = Wallet(name=wallet_name, amount=amount)
    db.add(wallet)
    db.flush()
    db.refresh(wallet)

    return wallet