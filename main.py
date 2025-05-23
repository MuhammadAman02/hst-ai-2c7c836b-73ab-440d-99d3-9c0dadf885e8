import os
import sys
from datetime import datetime
from nicegui import ui, app
import asyncio
from pathlib import Path

# Add the current directory to the path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our validation services and models
from app.services.validator import DocumentValidator
from app.models.document import Document, DocumentType, ValidationResult

# Configure app
app.title = "HST Secure Document Validation"
app.favicon = "🔐"

# Create upload directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Initialize validator
validator = DocumentValidator()

@ui.page('/')
def index():
    ui.add_head_html('<link rel="stylesheet" href="/static/css/styles.css">')
    
    with ui.column().classes('full-width'):
        ui.label('HST Secure Document Validation').classes('text-h3 text-center q-mb-xl')
        
        with ui.card().classes('full-width'):
            ui.label('Upload Documents for Validation').classes('text-h5')
            ui.label('Upload bank statements, payslips, identity documents, or tax records for validation').classes('text-subtitle1')
            
            # Document type selection
            doc_type = ui.select(
                label='Document Type',
                options=[
                    {'label': 'Bank Statement', 'value': DocumentType.BANK_STATEMENT},
                    {'label': 'Payslip', 'value': DocumentType.PAYSLIP},
                    {'label': 'Irish Residency Permit (IRP)', 'value': DocumentType.IRP},
                    {'label': 'PPSN Document', 'value': DocumentType.PPSN},
                    {'label': 'Tax Record', 'value': DocumentType.TAX_RECORD},
                ],
                value=DocumentType.BANK_STATEMENT
            ).classes('full-width')
            
            # File upload
            file_upload = ui.upload(
                label='Upload Document',
                auto_upload=True,
                max_files=1,
                max_file_size=10_000_000,  # 10MB
                on_upload=lambda e: handle_upload(e, doc_type.value)
            ).classes('full-width')
            
            # Customer information
            ui.label('Customer Information').classes('text-h6 q-mt-md')
            customer_name = ui.input(label='Customer Name').classes('full-width')
            customer_id = ui.input(label='Customer ID').classes('full-width')
            
            # Validation results container
            results_container = ui.column().classes('full-width q-mt-lg')
            
            async def handle_upload(e, document_type):
                # Clear previous results
                results_container.clear()
                
                with results_container:
                    ui.spinner(size='lg')
                    await asyncio.sleep(0.1)  # Allow UI to update
                
                try:
                    # Save the uploaded file
                    file_path = UPLOAD_DIR / e.name
                    with open(file_path, 'wb') as f:
                        f.write(e.content.read())
                    
                    # Create document object
                    document = Document(
                        file_path=str(file_path),
                        document_type=document_type,
                        customer_name=customer_name.value or "Unknown",
                        customer_id=customer_id.value or "Unknown",
                        upload_date=datetime.now()
                    )
                    
                    # Validate the document
                    await asyncio.sleep(1)  # Simulate processing time
                    validation_result = validator.validate_document(document)
                    
                    # Clear spinner
                    results_container.clear()
                    
                    # Display results
                    with results_container:
                        display_validation_results(validation_result)
                        
                except Exception as e:
                    results_container.clear()
                    with results_container:
                        ui.label(f'Error: {str(e)}').classes('text-negative')
            
            def display_validation_results(result: ValidationResult):
                with ui.card().classes('full-width validation-result'):
                    ui.label('Validation Results').classes('text-h5')
                    
                    # Overall status
                    status_color = 'positive' if result.is_valid else 'negative'
                    with ui.row().classes('full-width items-center'):
                        ui.icon('check_circle' if result.is_valid else 'error').classes(f'text-{status_color} text-h4')
                        ui.label(f"Status: {'Valid' if result.is_valid else 'Invalid'} Document").classes(f'text-{status_color} text-h5')
                    
                    # Risk score
                    risk_color = 'positive' if result.risk_score < 30 else 'warning' if result.risk_score < 70 else 'negative'
                    ui.label(f'Risk Score: {result.risk_score}/100').classes(f'text-{risk_color}')
                    
                    # Validation details
                    ui.separator()
                    ui.label('Validation Checks').classes('text-h6')
                    
                    with ui.table().classes('full-width'):
                        ui.table.header(
                            'Check Type',
                            'Status',
                            'Details'
                        )
                        for check in result.checks:
                            status_icon = '✅' if check.passed else '❌'
                            ui.table.row(
                                check.check_type,
                                status_icon,
                                check.details
                            )
                    
                    # Anomalies and red flags
                    if result.anomalies:
                        ui.separator()
                        ui.label('Detected Anomalies').classes('text-h6 text-negative')
                        with ui.list().classes('full-width'):
                            for anomaly in result.anomalies:
                                with ui.list_item():
                                    ui.icon('warning').classes('text-negative')
                                    ui.label(anomaly)
                    
                    # Recommendations
                    ui.separator()
                    ui.label('Recommendations').classes('text-h6')
                    with ui.list().classes('full-width'):
                        for recommendation in result.recommendations:
                            with ui.list_item():
                                ui.icon('lightbulb').classes('text-primary')
                                ui.label(recommendation)

# Run the app
ui.run(title="HST Secure Document Validation", port=8000)