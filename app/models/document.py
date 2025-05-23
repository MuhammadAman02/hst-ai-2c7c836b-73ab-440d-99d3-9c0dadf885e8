from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class DocumentType(str, Enum):
    BANK_STATEMENT = "bank_statement"
    PAYSLIP = "payslip"
    IRP = "irp"
    PPSN = "ppsn"
    TAX_RECORD = "tax_record"


class Document(BaseModel):
    """Represents a document uploaded for validation."""
    file_path: str
    document_type: DocumentType
    customer_name: str
    customer_id: str
    upload_date: datetime
    metadata: dict = {}


class ValidationCheck(BaseModel):
    """Represents a single validation check performed on a document."""
    check_type: str
    passed: bool
    details: str


class ValidationResult(BaseModel):
    """Represents the result of validating a document."""
    document: Document
    is_valid: bool
    risk_score: int  # 0-100, where 100 is highest risk
    checks: List[ValidationCheck]
    anomalies: List[str] = []
    recommendations: List[str] = []
    validation_date: datetime = datetime.now()