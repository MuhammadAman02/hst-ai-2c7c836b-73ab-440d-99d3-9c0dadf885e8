import random
from datetime import datetime
from typing import List, Dict, Any

from app.models.document import Document, DocumentType, ValidationResult, ValidationCheck


class DocumentValidator:
    """Service for validating documents and detecting fraud indicators."""
    
    def validate_document(self, document: Document) -> ValidationResult:
        """
        Validates a document based on its type and returns a validation result.
        
        For the preview, this uses mock validation logic. In a production system,
        this would implement actual document analysis and validation rules.
        """
        # Select validation strategy based on document type
        if document.document_type == DocumentType.BANK_STATEMENT:
            return self._validate_bank_statement(document)
        elif document.document_type == DocumentType.PAYSLIP:
            return self._validate_payslip(document)
        elif document.document_type == DocumentType.IRP:
            return self._validate_irp(document)
        elif document.document_type == DocumentType.PPSN:
            return self._validate_ppsn(document)
        elif document.document_type == DocumentType.TAX_RECORD:
            return self._validate_tax_record(document)
        else:
            # Default validation for unknown document types
            return ValidationResult(
                document=document,
                is_valid=False,
                risk_score=100,
                checks=[
                    ValidationCheck(
                        check_type="Document Type",
                        passed=False,
                        details="Unknown document type"
                    )
                ],
                anomalies=["Unknown document type"],
                recommendations=["Please select a valid document type"]
            )
    
    def _validate_bank_statement(self, document: Document) -> ValidationResult:
        """Mock validation for bank statements."""
        # In a real implementation, this would analyze the actual document content
        
        # Simulate validation checks
        checks = [
            ValidationCheck(
                check_type="Template Verification",
                passed=True,
                details="Document matches known bank statement template"
            ),
            ValidationCheck(
                check_type="Logo Verification",
                passed=True,
                details="Bank logo position and appearance verified"
            ),
            ValidationCheck(
                check_type="Account Number Format",
                passed=True,
                details="IBAN format is valid"
            ),
            ValidationCheck(
                check_type="Balance Calculation",
                passed=random.choice([True, False]),
                details="Opening balance + transactions = closing balance" if random.random() > 0.3 
                        else "Discrepancy detected in balance calculation"
            ),
            ValidationCheck(
                check_type="Transaction Pattern Analysis",
                passed=random.choice([True, False]),
                details="Transaction patterns appear normal" if random.random() > 0.3 
                        else "Unusual transaction patterns detected"
            )
        ]
        
        # Determine if document is valid based on checks
        is_valid = all(check.passed for check in checks)
        
        # Calculate risk score (0-100)
        risk_score = 10  # Base risk
        for check in checks:
            if not check.passed:
                risk_score += 20
        
        # Add random variation to risk score
        risk_score += random.randint(-10, 10)
        risk_score = max(0, min(100, risk_score))  # Ensure within 0-100 range
        
        # Generate anomalies for failed checks
        anomalies = []
        for check in checks:
            if not check.passed:
                if check.check_type == "Balance Calculation":
                    anomalies.append("Balance discrepancy: Opening balance + transactions does not equal closing balance")
                elif check.check_type == "Transaction Pattern Analysis":
                    anomalies.append("Unusual pattern: Multiple large round-sum deposits detected")
        
        # Generate recommendations
        recommendations = []
        if is_valid:
            recommendations.append("Document appears valid - proceed with standard processing")
        else:
            recommendations.append("Request additional verification from customer")
            if any(c.check_type == "Balance Calculation" and not c.passed for c in checks):
                recommendations.append("Verify transaction history with issuing bank")
        
        return ValidationResult(
            document=document,
            is_valid=is_valid,
            risk_score=risk_score,
            checks=checks,
            anomalies=anomalies,
            recommendations=recommendations
        )
    
    def _validate_payslip(self, document: Document) -> ValidationResult:
        """Mock validation for payslips."""
        checks = [
            ValidationCheck(
                check_type="Employer Verification",
                passed=random.choice([True, True, False]),
                details="Employer details match registered business" if random.random() > 0.2 
                        else "Employer details could not be verified"
            ),
            ValidationCheck(
                check_type="Tax Calculation",
                passed=random.choice([True, True, False]),
                details="Tax calculations are correct" if random.random() > 0.2 
                        else "Discrepancies found in tax calculations"
            ),
            ValidationCheck(
                check_type="Salary Consistency",
                passed=random.choice([True, True, False]),
                details="Salary figures are consistent throughout document" if random.random() > 0.2 
                        else "Inconsistent salary figures detected"
            ),
            ValidationCheck(
                check_type="Document Format",
                passed=True,
                details="Document format matches standard payslip format"
            )
        ]
        
        is_valid = all(check.passed for check in checks)
        
        risk_score = 15  # Base risk for payslips
        for check in checks:
            if not check.passed:
                risk_score += 25
        
        risk_score += random.randint(-10, 10)
        risk_score = max(0, min(100, risk_score))
        
        anomalies = []
        for check in checks:
            if not check.passed:
                if check.check_type == "Employer Verification":
                    anomalies.append("Employer not found in registered business database")
                elif check.check_type == "Tax Calculation":
                    anomalies.append("Tax calculation does not match standard rates for income level")
                elif check.check_type == "Salary Consistency":
                    anomalies.append("Gross salary does not match sum of net pay and deductions")
        
        recommendations = []
        if is_valid:
            recommendations.append("Payslip appears valid - proceed with standard processing")
        else:
            recommendations.append("Request additional verification from customer")
            if any(c.check_type == "Employer Verification" and not c.passed for c in checks):
                recommendations.append("Verify employer existence through Companies Registration Office")
        
        return ValidationResult(
            document=document,
            is_valid=is_valid,
            risk_score=risk_score,
            checks=checks,
            anomalies=anomalies,
            recommendations=recommendations
        )
    
    def _validate_irp(self, document: Document) -> ValidationResult:
        """Mock validation for Irish Residency Permits."""
        checks = [
            ValidationCheck(
                check_type="Document Format",
                passed=True,
                details="Document format matches official IRP card format"
            ),
            ValidationCheck(
                check_type="Security Features",
                passed=random.choice([True, True, False]),
                details="Security features present and valid" if random.random() > 0.2 
                        else "One or more security features could not be verified"
            ),
            ValidationCheck(
                check_type="Expiration Date",
                passed=random.choice([True, True, False]),
                details="IRP is current and not expired" if random.random() > 0.2 
                        else "IRP appears to be expired"
            ),
            ValidationCheck(
                check_type="GNIB Number Format",
                passed=True,
                details="GNIB number format is valid"
            )
        ]
        
        is_valid = all(check.passed for check in checks)
        
        risk_score = 20  # Base risk for identity documents
        for check in checks:
            if not check.passed:
                risk_score += 25
        
        risk_score += random.randint(-10, 10)
        risk_score = max(0, min(100, risk_score))
        
        anomalies = []
        for check in checks:
            if not check.passed:
                if check.check_type == "Security Features":
                    anomalies.append("Missing or altered security features detected")
                elif check.check_type == "Expiration Date":
                    anomalies.append("Document appears to be expired or date has been altered")
        
        recommendations = []
        if is_valid:
            recommendations.append("IRP appears valid - proceed with standard processing")
        else:
            recommendations.append("Request physical verification of original document")
            if any(c.check_type == "Security Features" and not c.passed for c in checks):
                recommendations.append("Escalate to fraud department for detailed investigation")
        
        return ValidationResult(
            document=document,
            is_valid=is_valid,
            risk_score=risk_score,
            checks=checks,
            anomalies=anomalies,
            recommendations=recommendations
        )
    
    def _validate_ppsn(self, document: Document) -> ValidationResult:
        """Mock validation for PPSN documents."""
        # In Ireland, PPS Numbers follow the format of 7 digits followed by 1-2 letters
        checks = [
            ValidationCheck(
                check_type="PPSN Format",
                passed=True,
                details="PPSN format is valid (7 digits + 1-2 letters)"
            ),
            ValidationCheck(
                check_type="Document Format",
                passed=True,
                details="Document format matches official PPSN documentation"
            ),
            ValidationCheck(
                check_type="Name Matching",
                passed=random.choice([True, True, False]),
                details="Name on document matches application name" if random.random() > 0.2 
                        else "Name discrepancy detected"
            ),
            ValidationCheck(
                check_type="DOB Consistency",
                passed=random.choice([True, True, False]),
                details="Date of birth is consistent with other documents" if random.random() > 0.2 
                        else "Date of birth discrepancy detected"
            )
        ]
        
        is_valid = all(check.passed for check in checks)
        
        risk_score = 15  # Base risk
        for check in checks:
            if not check.passed:
                risk_score += 25
        
        risk_score += random.randint(-10, 10)
        risk_score = max(0, min(100, risk_score))
        
        anomalies = []
        for check in checks:
            if not check.passed:
                if check.check_type == "Name Matching":
                    anomalies.append("Name on PPSN document does not match name on application")
                elif check.check_type == "DOB Consistency":
                    anomalies.append("Date of birth on PPSN document does not match other provided documents")
        
        recommendations = []
        if is_valid:
            recommendations.append("PPSN document appears valid - proceed with standard processing")
        else:
            recommendations.append("Request additional identification documents")
            if any(c.check_type == "Name Matching" and not c.passed for c in checks):
                recommendations.append("Verify name change documentation if applicable")
        
        return ValidationResult(
            document=document,
            is_valid=is_valid,
            risk_score=risk_score,
            checks=checks,
            anomalies=anomalies,
            recommendations=recommendations
        )
    
    def _validate_tax_record(self, document: Document) -> ValidationResult:
        """Mock validation for tax records."""
        checks = [
            ValidationCheck(
                check_type="Document Format",
                passed=True,
                details="Document format matches official tax record format"
            ),
            ValidationCheck(
                check_type="Tax Year Verification",
                passed=True,
                details="Tax year is current or recent"
            ),
            ValidationCheck(
                check_type="Income Consistency",
                passed=random.choice([True, True, False]),
                details="Income figures are consistent with other documents" if random.random() > 0.2 
                        else "Income discrepancies detected"
            ),
            ValidationCheck(
                check_type="Tax Calculation",
                passed=random.choice([True, True, False]),
                details="Tax calculations appear correct" if random.random() > 0.2 
                        else "Tax calculation anomalies detected"
            ),
            ValidationCheck(
                check_type="Official Stamps/Watermarks",
                passed=random.choice([True, True, False]),
                details="Official stamps/watermarks verified" if random.random() > 0.2 
                        else "Official stamps/watermarks could not be verified"
            )
        ]
        
        is_valid = all(check.passed for check in checks)
        
        risk_score = 25  # Base risk for tax documents
        for check in checks:
            if not check.passed:
                risk_score += 20
        
        risk_score += random.randint(-10, 10)
        risk_score = max(0, min(100, risk_score))
        
        anomalies = []
        for check in checks:
            if not check.passed:
                if check.check_type == "Income Consistency":
                    anomalies.append("Reported income does not match income on other documents")
                elif check.check_type == "Tax Calculation":
                    anomalies.append("Tax amounts do not align with standard calculation for reported income")
                elif check.check_type == "Official Stamps/Watermarks":
                    anomalies.append("Document lacks proper official authentication markers")
        
        recommendations = []
        if is_valid:
            recommendations.append("Tax record appears valid - proceed with standard processing")
        else:
            recommendations.append("Request additional verification from tax authority")
            if any(c.check_type == "Income Consistency" and not c.passed for c in checks):
                recommendations.append("Cross-verify income with payslips and bank statements")
        
        return ValidationResult(
            document=document,
            is_valid=is_valid,
            risk_score=risk_score,
            checks=checks,
            anomalies=anomalies,
            recommendations=recommendations
        )