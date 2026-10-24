from fastapi import APIRouter
from app.services import operations as operation_service
from app.schemas import OperationRequest

router = APIRouter()

@router.post("/operations/income")
def add_income(operation: OperationRequest):
    return operation_service.add_income(operation)

@router.post("/operations/expense")
def add_expense(operation: OperationRequest):
    return operation_service.add_expense(operation)