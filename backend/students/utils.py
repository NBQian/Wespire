from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import os
from django.conf import settings
from .models import Product, FuturePlan
from reportlab.lib.units import inch

def generate_pdf(student_summary):
    filename = f"client_{student_summary.student.FirstName}_{student_summary.student.LastName}_{student_summary.date_created}.pdf"
    pdf_dir = os.path.join(settings.MEDIA_ROOT, 'client_summaries')
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
    pdf_path = os.path.join(pdf_dir, filename)
    
    doc = SimpleDocTemplate(pdf_path, pagesize=landscape(letter))
    elements = []
    
    # Fetch products and future plans
    products = Product.objects.filter(unique_code=student_summary.unique_code)
    
    # Tables for product sections
    sections = [
        [("Company", "Company"), ("Product Number", "ProductNumber"), ("Product Name", "ProductName"), ("Type", "Type")],
        [("Whole Life", "WholeLife"), ("Endowment", "Endowment"), ("Term", "Term"), ("Inv. Linked", "InvLinked"), ("Total Death Coverage", "TotalDeathCoverage"), ("Total Permanent Disability", "TotalPermanentDisability")],
        [("Early Critical Illness", "EarlyCriticalIllness"), ("Accidental", "Accidental"), ("Other Benefits/Remarks", "OtherBenefitsRemarks"), ("Mode", "Mode"), ("Monthly", "Monthly"), ("Quarterly", "Quarterly")],
        [("Semi-Annual", "SemiAnnual"), ("Yearly", "Yearly"), ("Maturity/Premium End Date", "MaturityPremiumEndDate"), ("Current Value", "CurrentValue"), ("Total Premiums Paid", "TotalPremiumsPaid")]
    ]
    
    for section in sections:
        header = [col[0] for col in section]
        product_data = [header]
        
        for product in products:
            row = [getattr(product, col[1]) for col in section]
            product_data.append(row)
        
        table = Table(product_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)
    
    # Future Plan table remains unchanged
    # (Include the Future Plan table code here as it was, without changes)
    
    # Write the document to disk
    doc.build(elements)
    return os.path.join('client_summaries', filename)
