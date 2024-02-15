import time
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import os
from django.conf import settings
from .models import Product, FuturePlan
from reportlab.lib.units import inch
import fpdf
from fpdf import FPDF
import time
import pandas as pd
import matplotlib.pyplot as plt
import dataframe_image as dfi
from matplotlib.backends.backend_pdf import PdfPages
from reportlab.graphics.charts.piecharts import Pie
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.graphics.shapes import Drawing
from reportlab.lib.styles import getSampleStyleSheet





# def generate_pdf(student_summary):
    # filename = f"client_{student_summary.student.FirstName}_{student_summary.student.LastName}_{student_summary.date_created}.pdf"
    # pdf_dir = os.path.join(settings.MEDIA_ROOT, 'client_summaries')
    # if not os.path.exists(pdf_dir):
    #     os.makedirs(pdf_dir)
    # pdf_path = os.path.join(pdf_dir, filename)
    
#     doc = SimpleDocTemplate(pdf_path, pagesize=landscape(letter))
#     elements = []
#     styles = getSampleStyleSheet()

    
#     # Fetch products and future plans
#     products = Product.objects.filter(unique_code=student_summary.unique_code)
#     plans = FuturePlan.objects.filter(unique_code=student_summary.unique_code)

#     # # Tables for product sections
#     # sections = [
#     #     [("Company", "Company"), ("Product Number", "ProductNumber"), ("Product Name", "ProductName"), ("Type", "Type")],
#     #     [("Whole Life", "WholeLife"), ("Endowment", "Endowment"), ("Term", "Term"), ("Inv.Linked", "InvLinked"), ("Total Death Coverage", "TotalDeathCoverage"), ("Total Permanent Disability", "TotalPermanentDisability")],
#     #     [("Early Critical Illness", "EarlyCriticalIllness"), ("Accidental", "Accidental"), ("Other Benefits/Remarks", "OtherBenefitsRemarks"), ("Mode", "Mode"), ("Monthly", "Monthly"), ("Quarterly", "Quarterly")],
#     #     [("Semi-Annual", "SemiAnnual"), ("Yearly", "Yearly"), ("Maturity/Premium End Date", "MaturityPremiumEndDate"), ("Current Value", "CurrentValue"), ("Total Premiums Paid", "TotalPremiumsPaid")]
#     # ]
    
#     # for section in sections:
#         # header = [col[0] for col in section]
#         # product_data = [header]
        
#         # for product in products:
#         #     row = [getattr(product, col[1]) for col in section]
#         #     product_data.append(row)
        
#         # table = Table(product_data)
#         # table.setStyle(TableStyle([
#         #     ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         #     ('GRID', (0, 0), (-1, -1), 1, colors.black),
#         # ]))
#         # elements.append(table)
    
#     # Generate pie charts for future plans
#     for plan in plans:
#         # Convert Decimal to float for compatibility with ReportLab
#         data = [float(plan.CurrentSumAssured), float(plan.RecommendedSumAssured)]
#         labels = ['Current', 'Recommended']

#         drawing = Drawing(200, 100)  # Adjust size as needed
#         pie = Pie()
#         pie.x = 65
#         pie.y = 15
#         pie.width = 70
#         pie.height = 70
#         pie.data = data
#         pie.labels = labels
#         pie.slices.strokeWidth = 0.5
#         pie.slices[0].popout = 10
#         pie.slices[1].popout = 5
#         pie.slices[0].strokeWidth = 2
#         pie.slices[1].strokeWidth = 2
#         pie.slices[0].fillColor = colors.lightblue
#         pie.slices[1].fillColor = colors.lightgreen

#         drawing.add(pie)
        
#         elements.append(Paragraph(plan.Type, styles['Heading2']))
#         elements.append(drawing)
#         elements.append(Spacer(1, 20))  # Adds space between each chart


#     # Write the document to disk
#     doc.build(elements)
#     return os.path.join('client_summaries', filename)

#     # Write the document to disk
#     doc.build(elements)
#     return os.path.join('client_summaries', filename)
from fpdf import FPDF
import matplotlib.pyplot as plt
import os

plt.switch_backend('Agg')  # Use the Agg backend for Matplotlib

class PDF(FPDF):
    pass


def generate_table_image(plan, table_img_path):
    plt.rcParams.update({'font.family':'monospace'})
    
    fig, ax = plt.subplots(figsize=(4, 1))
    ax.axis('off')  # Hide the axes

    cell_text = [
        [f"Current Coverage:    S${plan.CurrentSumAssured:,.2f}"],
        [f"Suggested Coverage:  S${plan.RecommendedSumAssured:,.2f}"],
        [f"Shortfall:           S${plan.Shortfall:,.2f}"]
    ]

    table = ax.table(cellText=cell_text, loc='center', cellLoc='left', edges='horizontal')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)

    grey_color = "#808080"
    for pos, cell in table.get_celld().items():
        cell.set_edgecolor(grey_color)

    plt.savefig(table_img_path, dpi=300, bbox_inches="tight", pad_inches=0.05)
    plt.close()
    plt.rcdefaults()



def generate_pdf(student_summary, user):
    filename = f"client_{student_summary.student.FirstName}_{student_summary.student.LastName}_{student_summary.date_created}.pdf"
    pdf_dir = os.path.join(settings.MEDIA_ROOT, 'client_summaries')
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
    pdf_path = os.path.join(pdf_dir, filename)

    plans = FuturePlan.objects.filter(unique_code=student_summary.unique_code)[:5]

    current_dir = os.path.dirname(__file__)
    cover_img_path = os.path.join(current_dir, 'img', 'Cover.png')

    
    pdf = PDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.image(cover_img_path, 0, 0, 210, 297)
    client_name = f"{student_summary.student.FirstName} {student_summary.student.LastName}"
    user_name = user.name
    add_text_annotations(pdf, client_name, user_name)



    pdf.add_page()
    
    generate_pie_charts(student_summary, pdf, pdf_dir, plans)

    pdf.output(pdf_path)

    return os.path.join('client_summaries', filename)


def add_text_annotations(pdf, client_name, user_name):
    text1 = f"For {client_name}"
    # Prepare text2 as before; its positioning remains unchanged
    text2 = f"Prepared by {user_name}"

    # Convert 4.25 cm to mm (FPDF unit), as FPDF's default unit is mm
    y1 = 107.95  # 4.25 cm

    # Set font before calculating text width for accurate measurement
    pdf.set_font('Times', 'B', 20)

    # Calculate width of text1 to center it
    text1_width = pdf.get_string_width(text1)
    page_width = pdf.w  # Width of the current page
    x1 = (page_width - text1_width) / 2  # Center the text

    # Set vertical position and add the centered text1
    pdf.set_xy(x1, y1)
    pdf.cell(text1_width, 10, text1, 0, 1, 'C')  # The 'C' align parameter centers the text in the cell

    r, g, b = 255, 255, 255

    pdf.set_text_color(r, g, b)
    # For text2, position as previously defined (unchanged from your original)
    x2, y2 = 50.8, 259.08  # Assuming y2 is also in mm

    pdf.set_xy(x2, y2)
    pdf.cell(text1_width, 10, text2, 0, 1, 'C')




def generate_pie_charts(student_summary, pdf, pdf_dir, plans):
    

    chart_width_mm = 70
    x_positions = [20, 110]
    y_positions = [20, 110, 200]

    labels = ['CurrentSumAssured', 'Shortfall']
    colors = ['#1E62AB','#F2BE37']
    plt.figure(figsize=(2, 2))  # Dummy figure for legend
    plt.pie([1, 1], labels=labels, colors=colors)
    plt.legend(loc="center")
    legend_path = os.path.join(pdf_dir, "legend.png")
    plt.savefig(legend_path, bbox_inches='tight', pad_inches=0)
    plt.close()

    for i, plan in enumerate(plans):
        x_position = x_positions[i % 2]
        y_position = y_positions[i // 2]

        sizes = [float(plan.CurrentSumAssured), float(plan.Shortfall)]
        fig, ax = plt.subplots(figsize=(4, 3))  # Increased figure size
        ax.pie(sizes, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.annotate(plan.Type, xy=(0.5, 0.95), xycoords='axes fraction', ha='center', fontsize=7, fontweight="bold")
        img_path = os.path.join(pdf_dir, f"pie_chart_{i}.png")
        plt.savefig(img_path, dpi=300, bbox_inches='tight', pad_inches=0)

        plt.close()
        
        pdf.image(img_path, x=x_position, y=y_position, w=chart_width_mm)
        os.remove(img_path)

        table_img_path = os.path.join(pdf_dir, f"table_{i}.png")
        generate_table_image(plan, table_img_path)

        table_y_position = y_positions[i // 2] + 65
        pdf.image(table_img_path, x=x_positions[i % 2], y=table_y_position, w=chart_width_mm)
        os.remove(table_img_path)

    pdf.image(legend_path, x=160, y=260, w=40)
    os.remove(legend_path)