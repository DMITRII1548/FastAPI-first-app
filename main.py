from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, HttpUrl

app = FastAPI()

BALANCE = {}

class OperationRequest(BaseModel):
    wallet_name: str
    amount: float
    description: str | None = None

@app.get('/balance')
def get_balance(wallet_name: str | None = None):
    if wallet_name is None:
        return {"total_balance": sum(BALANCE)}


    if wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{wallet_name}' not found"
        )

    return {
        "Wallet": wallet_name,
        "balance:": BALANCE[wallet_name]
    }

@app.post("/wallets/{wallet}")
def create_wallet(name: str, initial_balance: float = 0):
    if name in BALANCE:
        raise HTTPException(
            status_code=400,
            detail=f"Wallet '{name}' already exists"
        )

    BALANCE[name] = initial_balance

    return {
        "message": f"Wallet '{name}' created",
        "wallet": name,
        "balance": BALANCE[name]
    }

@app.post("/operations/income")
def add_income(operation: OperationRequest):
    if operation.wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found"
        )

    if operation.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount must be positive"
        )

    BALANCE[operation.wallet_name] += operation.amount

    return {
        "message": "Income added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": BALANCE[operation.wallet_name]
    }

@app.post("/operations/expense")
def add_expense(operation: OperationRequest):
    if operation.wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found"
        )

    if operation.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount must be positive"
        )


    if operation.amount > BALANCE[operation.wallet_name]:
        raise HTTPException(
            status_code=400,
            detail="Not enough balance"
        )


    BALANCE[operation.wallet_name] -= operation.amount

    return {
        "message": "Expense Added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": BALANCE[operation.wallet_name]
    }