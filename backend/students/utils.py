import tempfile
import pypdf
from pypdf import PdfReader, PdfWriter
import re
from datetime import datetime, date

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import os
from django.conf import settings
from .models import Product, FuturePlan
from reportlab.lib.units import inch
from fpdf import FPDF
import time
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Image
from reportlab.graphics.shapes import Drawing
from reportlab.lib.styles import getSampleStyleSheet
from fpdf import FPDF
import matplotlib.pyplot as plt
import os
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


plt.switch_backend('Agg')  # Use the Agg backend for Matplotlib

class PDF(FPDF):
    pass
def insert_products_between_pages(initial_pdf_buffer, products_pdf_buffer):
    # Create a PDF writer for the output PDF
    pdf_writer = PdfWriter()

    initial_pdf = PdfReader(initial_pdf_buffer)
    products_pdf = PdfReader(products_pdf_buffer)

    # Add the first page from the initial PDF
    pdf_writer.add_page(initial_pdf.pages[0])

    # Add all pages from the products PDF
    for page in products_pdf.pages:
        pdf_writer.add_page(page)

    # Add the remaining pages from the initial PDF
    for page in initial_pdf.pages[1:]:
        pdf_writer.add_page(page)
    disclaimer_pdf = PdfReader('Disclaimer.pdf') 
    for page in disclaimer_pdf.pages:
        pdf_writer.add_page(page)
    # Output to a new BytesIO buffer
    output_pdf_buffer = BytesIO()
    pdf_writer.write(output_pdf_buffer)
    output_pdf_buffer.seek(0)  # Reset buffer cursor

    return output_pdf_buffer

def merge_headers_with_document(main_pdf_buffer, header1_buffer, header2_buffer):
    main_pdf = PdfReader(main_pdf_buffer)
    header1_pdf = PdfReader(header1_buffer)
    header2_pdf = PdfReader(header2_buffer)

    pdf_writer = PdfWriter()

    # Merge header1 with the first page of the main document
    page1 = main_pdf.pages[0]
    page1.merge_page(header1_pdf.pages[0])
    pdf_writer.add_page(page1)

    # Check if there's a second page and merge header2 with it
    if len(main_pdf.pages) > 1:
        page2 = main_pdf.pages[1]
        page2.merge_page(header2_pdf.pages[0])
        pdf_writer.add_page(page2)

    # Add any remaining pages from the main document
    for page in main_pdf.pages[2:]:
        pdf_writer.add_page(page)

    # Output to a new BytesIO buffer
    output_pdf_buffer = BytesIO()
    pdf_writer.write(output_pdf_buffer)
    output_pdf_buffer.seek(0)

    return output_pdf_buffer


def load_pdf_into_buffer(pdf_file_path):
    """
    Loads a PDF file from the given path into a BytesIO buffer.
    
    Args:
        pdf_file_path (str): The file path to the PDF to load.
        
    Returns:
        BytesIO: A buffer containing the PDF content.
    """
    with open(pdf_file_path, 'rb') as pdf_file:
        return BytesIO(pdf_file.read())

def queryset_to_list_of_dicts(queryset):
    list_of_dicts = []
    for product in queryset:
        product_dict = {}
        for field in product._meta.fields:
            field_name = field.name
            field_value = getattr(product, field_name)

            # Special handling for date and datetime fields to format them as strings
            if isinstance(field_value, (date, datetime)):
                product_dict[field_name] = field_value.strftime('%Y-%m-%d')
            else:
                product_dict[field_name] = field_value

        list_of_dicts.append(product_dict)
    return list_of_dicts

def generate_pdf(student_summary, dob):
    print(student_summary)
    filename = f"client_{student_summary.student.FirstName}_{student_summary.student.LastName}_{student_summary.date_created}.pdf"

    pdf_dir = os.path.join(settings.MEDIA_ROOT, 'client_summaries')
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)

    products_queryset = Product.objects.filter(unique_code=student_summary.unique_code)
    products = queryset_to_list_of_dicts(products_queryset)

    plans = FuturePlan.objects.filter(unique_code=student_summary.unique_code)

    current_dir = os.path.dirname(__file__)
    cover_img_path = os.path.join(current_dir, 'img', 'Cover.png')

    
    pdf = PDF(orientation='P', unit='mm', format='A4')
    
    # Cover Page
    pdf.add_page()
    pdf.set_auto_page_break(auto=False)
    pdf.image(cover_img_path, 0, 0, 210, 297)
    client_name = f"{student_summary.student.FirstName} {student_summary.student.LastName}"
    user_name = student_summary.DisplayedName
    email = student_summary.DisplayedEmail
    MAS = student_summary.MAS
    title = student_summary.DisplayedTitle
    phone = student_summary.DisplayedPhoneNumber
    add_cover_page_text(pdf, client_name, user_name, email, MAS, title, phone)

    # Products Page
    product_table_buffer = generate_product_table(products)

    header1_path = 'header1.pdf'
    header2_path = 'header2.pdf'

    header1_buffer = load_pdf_into_buffer(header1_path)
    header2_buffer = load_pdf_into_buffer(header2_path)
    
    merged_buffer = merge_headers_with_document(product_table_buffer, header1_buffer, header2_buffer)


    # Bar Graph Page
    add_bar_graph_to_pdf(pdf, products)

    # Line Graph Page
    pdf.add_page()
    create_line_graphs(products, dob, pdf)
    # Pie Chart Page
    pdf.add_page()
    generate_pie_charts(pdf, pdf_dir, plans)

    pdf_content = pdf.output(dest='S').encode('latin1')  # Get PDF data as a byte string

    # Create a BytesIO object from the PDF byte string
    main_buffer = BytesIO(pdf_content)
    main_buffer.seek(0)
    
    final_buffer = insert_products_between_pages(main_buffer, merged_buffer)

    pdf_file = ContentFile(final_buffer.read(), name=filename)

    # Return the ContentFile, no need to manually save it to S3 or generate a URL here
    return pdf_file

from datetime import datetime
def create_line_graphs(products, dob, pdf):
    print(products)
    start_age = 20
    end_age = 100
    def calculate_annual_payments(start_age, end_age):
        annual_payments = {age: 0 for age in range(start_age, end_age + 1)}

        for product in products:
            start_date = datetime.strptime(product['Date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(product['PaymentEndDate'], '%Y-%m-%d').date()
            mode = product['Mode']
            single_payment_amount = float(product['SinglePaymentAmount'])
            yearly_payment_amount = float(product['YearlyPaymentAmount']) if mode != "Single" else 0

            if "Single" in mode:
                payment_year = start_date.year
                age_at_payment = payment_year - dob.year
                if start_age <= age_at_payment <= end_age:
                    annual_payments[age_at_payment] += single_payment_amount
            else:
                for year in range(start_date.year, end_date.year + 1):
                    age_at_year = year - dob.year
                    if start_age <= age_at_year <= end_age:
                        if "Monthly" in mode:
                            annual_payments[age_at_year] += yearly_payment_amount * 12
                        elif "Yearly" in mode:
                            annual_payments[age_at_year] += yearly_payment_amount
        return annual_payments


    annual_payments = calculate_annual_payments(start_age, end_age)

    df_annual_payments = pd.DataFrame(list(annual_payments.items()), columns=['Age', 'Annual Payment'])
    ax = df_annual_payments.plot(kind='line', x='Age', y='Annual Payment', marker='o', linestyle='-', color='#293486', markersize=3.5, figsize=(10, 6))  # Adjust markersize as needed

    # Customizing the plot
    ax.set_xlabel("Age", fontsize=14, labelpad=20)
    ax.set_ylabel("Annual Payment (S$)", fontsize=14, labelpad=20)
    plt.xticks(range(start_age, end_age + 1, 10))
    plt.legend(['Annual Payment'], fontsize=12)

    # Adjusting tick parameters as per the new requirements
    ax.tick_params(axis='x', labelsize=13, pad=13)
    ax.tick_params(axis='y', labelsize=12, pad=13)

    # Setting the title with custom font size, font name, font weight, and padding
    ax.set_title('Annual Payment Outflow', fontsize=20, fontname='Arial', fontweight='bold', pad=25)

    # Remove grid
    ax.grid(False)

    # Remove top and right border lines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Before showing the plot, save it to a file
    plt.savefig('payment.png', dpi=300, bbox_inches='tight')

    def calculate_premium_payouts(start_age, end_age):
        premium_payouts = {age: 0 for age in range(start_age, end_age + 1)}
        for product in products:
            if product['PremiumPayoutMode'] == 'Single':
                payout_year = int(product['PremiumPayoutEndYear'])
                payout_age = payout_year - dob.year
                if start_age <= payout_age <= end_age:
                    premium_payouts[payout_age] += float(product['PremiumPayoutAmount'])
            elif product['PremiumPayoutMode'] == 'Yearly':
                start_year = int(product['PremiumPayoutYear'])
                end_year = int(product['PremiumPayoutEndYear'])
                for year in range(start_year, end_year + 1):
                    age = year - dob.year
                    if start_age <= age <= end_age:
                        premium_payouts[age] += float(product['PremiumPayoutAmount'])
        return premium_payouts

    # Calculate premium payouts
    premium_payouts = calculate_premium_payouts(20, 100)

    # Convert to DataFrame
    df_premium_payouts = pd.DataFrame(list(premium_payouts.items()), columns=['Age', 'Premium Payout'])

    # Plot
    ax = df_premium_payouts.plot(kind='line', x='Age', y='Premium Payout', color='#293486', marker='o', linestyle='-', markersize=3.5, figsize=(10, 6))
    ax.set_xlabel("Age", fontsize=14, labelpad=20)
    ax.set_ylabel("Premium Payout (S$)", fontsize=14, labelpad=20)
    plt.xticks(range(20, 101, 10))
    ax.tick_params(axis='x', labelsize=13, pad=13)
    ax.tick_params(axis='y', labelsize=12, pad=10)
    ax.set_title('Premium Payout Flow', fontsize=20, fontname='Arial', fontweight='bold', pad=25)
    ax.grid(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.legend(['Premium Payout'])

    # Save the graph as a PNG image
    plt.savefig('premium.png', dpi=300, bbox_inches='tight')

    payment_image = 'payment.png'
    premium_image = 'premium.png'
    
    # Add images to the PDF. Adjust x, y, w, h as needed.
    pdf.image(payment_image, x=10, y=20, w=180)  # Place the first image near the top
    pdf.image(premium_image, x=10, y=140, w=180)  # Place the second image lower, adjust 'y' as needed
    os.remove(payment_image)
    os.remove(premium_image)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    header_path = os.path.join(script_dir, "img", "CPPHeader.png")
    pdf.image(header_path, x = 0, y = 0, w = 210)



from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.colors import white
from reportlab.lib.enums import TA_CENTER

def create_inflow_outflow_page(pdf, products):
    # Add a portrait page
    pdf.add_page()

def generate_product_table(products):
    buffer = BytesIO()
    custom_headers = {
    "TotalPermanentDisability": "TPD SA",
    "TotalDeathCoverage": "Death SA",
    "OtherBenefitsRemarks": "Remarks",
    "MaturityPremiumEndDate": "Maturity Date"
    }
    excluded_fields = ['unique_code', 'id', 'Type', "PremiumPayoutMode", "PremiumPayoutYear", "PremiumPayoutAmount", "PaymentEndDate"]
    filtered_fields = [field for field in list(products[0].keys()) if field not in excluded_fields]

    first_half_fields = filtered_fields[:12]
    second_half_fields = filtered_fields[12:]

    stylesheet = getSampleStyleSheet()
    normal_style = stylesheet['Normal']

    title_style = ParagraphStyle('Title', parent=normal_style, fontSize=10, leading=12, spaceBefore=6, spaceAfter=6, textColor=white, alignment=TA_CENTER)

    # Process headers to use Paragraph for increased height
    def process_headers(headers):
        return [Paragraph('<b>{}</b>'.format(header), title_style) for header in headers]


    first_half_headers = process_headers(["No."] + [custom_headers.get(field, camel_case_to_words(field)) for field in first_half_fields])
    second_half_headers = process_headers(["No."] + [custom_headers.get(field, camel_case_to_words(field)) for field in second_half_fields])

    remarks_style = ParagraphStyle('remarks_style', parent=normal_style, fontSize=8, spaceBefore=0, spaceAfter=0, leftIndent=0, rightIndent=0, firstLineIndent=0, leading=9, wordWrap='CJK')

    # Process second table data to use Paragraph for "OtherBenefitsRemarks"
    def process_second_table_data(products, fields):
        processed_data = []
        for i, product in enumerate(products):
            row = [i+1]  # Adding row number
            for field in fields:
                if field == 'OtherBenefitsRemarks':
                    text = product.get(field, "")
                    row.append(Paragraph(text, remarks_style))
                else:
                    row.append(product.get(field, ""))
            processed_data.append(row)
        return processed_data

    first_half_data = [[i+1] + [product[field] for field in first_half_fields] for i, product in enumerate(products)]
    second_half_data = process_second_table_data(products, second_half_fields)

    
    # Create the document with custom canvas method
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    light_grey = colors.Color(0.784, 0.784, 0.784)

    def get_table_style():
        return TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, light_grey),
            ('BOX', (0, 0), (-1, -1), 0.25, light_grey),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#293486")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('TOPPADDING', (0, 0), (-1, 0), 14),  # Adds top padding to the title cells
            ('BOTTOMPADDING', (0, 0), (-1, 0), 14), 
            ('LEFTPADDING', (0, 0), (-1, 0), 8), 
            ('RIGHTPADDING', (0, 0), (-1, 0), 8), 
        ] + [
            ('BACKGROUND', (0, i), (-1, i), colors.white if i % 2 == 1 else colors.HexColor("#e6e6e6"))
            for i in range(1, max(len(first_half_data), len(second_half_data)) + 1)
        ])
    table_style = get_table_style()
    # Specify column widths for the second table, fixed width for "OtherBenefitsRemarks"
    col_widths_second_half = [None] + [45 * mm] + [None] * (len(second_half_headers) - 2)

    first_table = Table([first_half_headers] + first_half_data)
    second_table = Table([second_half_headers] + second_half_data, colWidths=col_widths_second_half)

    first_table.setStyle(table_style)
    second_table.setStyle(table_style)

    elements = [first_table, PageBreak(), second_table]
    doc.build(elements)
    buffer.seek(0)
    return buffer

from reportlab.lib import pagesizes, colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import mm
import re
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, PageBreak, Paragraph
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.colors import HexColor
from reportlab.pdfgen.canvas import Canvas
from matplotlib.ticker import FuncFormatter

# Assuming 'products' is your list of product dictionaries
def create_bar_graph_data(products):
    # Initialize sums for each category
    categories = ['TotalDeathCoverage', 'TotalPermanentDisability', 'EarlyCriticalIllness', 'CriticalIllness', 'Accidental']
    headers = {'TotalDeathCoverage': "Total Death\nCoverage", 'TotalPermanentDisability': 'Total Permanent\nDisability',
               'EarlyCriticalIllness': 'Early Critical\nIllness', 'CriticalIllness': 'Critical Illness', 'Accidental': 'Accidental'}
    sums = {header: 0 for header in headers.values()}
    
    # Sum up the amounts for each category
    for product in products:
        for category in categories:
            sums[headers[category]] += product.get(category, 0)
    
    return sums

def save_bar_graph(sums, filename="bar_graph.png"):
    categories = list(sums.keys())
    values = list(sums.values())

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(categories, values, color='#293486', width=0.5) 
    
    ax.tick_params(axis='x', labelsize=13, pad=13)
    ax.tick_params(axis='y', labelsize=12, pad=10)
    ax.set_title('Total Sum Assured', fontsize=20, fontname='Arial', fontweight='bold', pad=25)


    # Custom formatter to add "S$" in front of y-axis values
    def currency(x, pos):
        return 'S$ ' + str(int(x))
    ax.yaxis.set_major_formatter(FuncFormatter(currency))

    # Remove top and right lines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Set y-axis label further away from the scales
    ax.set_ylabel('Sum Assured', labelpad=20, fontsize=12)


    # Adding value labels on top of each bar with adjusted font size
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'S${height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=12)  # Adjust the fontsize as needed

    plt.tight_layout()
    plt.savefig(filename)
    # plt.savefig(filename, dpi = 300)
    plt.close()
def add_bar_graph_to_pdf(pdf, products):
    sums = create_bar_graph_data(products)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    header_path = os.path.join(script_dir, "img", "CPHeader.png")
    # Save the bar graph to an image
    graph_filename = "temp_bar_graph.png"
    save_bar_graph(sums, graph_filename)

    # Add a portrait page
    pdf.add_page()
    pdf.image(header_path, x = 0, y = 0, w = 210)  # Assume the header fits in the top part

    header_height = 30  # Adjust according to your header's actual height

    # Insert the bar graph image slightly below the header
    pdf.image(graph_filename, x=4, y=header_height + 10, w=pdf.w - 20, h=(pdf.h / 2) - 20 - header_height)

    # Adjust the Y position for the table to start below the bar graph, considering header height
    pdf.set_y(pdf.h / 2 + header_height / 2)

    add_bar_graph_table(pdf, sums)

    # Remove the temporary graph image file
    os.remove(graph_filename)


def add_bar_graph_table(pdf, sums):
    pdf.set_font('Arial', 'B', 12)  # Set font to Arial, bold, size 12 for the header
    line_height = pdf.font_size * 3
    col_width = (pdf.w - pdf.l_margin - pdf.r_margin) / 2.5  # Adjust for 2 columns in full page width

    total_table_width = col_width * 2  # Total table width for 2 columns

    # Calculate starting x position to center the table
    start_x = (pdf.w - total_table_width) / 2

    pdf.set_x(start_x)
    
    # Header with background color #293486 and white text
    pdf.set_fill_color(41, 52, 134)  # RGB equivalent of #293486
    pdf.set_text_color(255, 255, 255)  # Set text color to white
    pdf.cell(col_width, line_height, " Category", border=1, fill=True, align='C')
    pdf.cell(col_width, line_height, " Coverage", border=1, fill=True, align='C')
    pdf.ln(line_height)
    
    pdf.set_font('Arial', '', 12)  # Reset font to Arial, normal, size 12 for row data
    row_fill = False
    for key, value in sums.items():
        pdf.set_x(start_x)
        # Alternate row color between white and grey (#e6e6e6)
        if row_fill:
            pdf.set_fill_color(230, 230, 230)  # RGB equivalent of #e6e6e6
        else:
            pdf.set_fill_color(255, 255, 255)  # Set fill color back to white for alternating rows
        
        pdf.set_text_color(0, 0, 0)  # Reset text color to black for row data
        pdf.cell(col_width, line_height, str(f' {key}'), border=1, fill=row_fill, align='C')
        pdf.cell(col_width, line_height, f" S$ {value}", border=1, fill=row_fill, align='C')
        pdf.ln(line_height)
        row_fill = not row_fill  # Toggle the fill for the next row

def camel_case_to_words(s):
    """Convert CamelCase to words with spaces."""
    return ' '.join(re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', s))


def add_cover_page_text(pdf, client_name, user_name, email, MAS, title, phone):
    text1 = f"For {client_name}"
    text2 = f"{user_name}"

    text3 = f"{title}"
    text4 = f"MAS Number: {MAS}"
    text5 = f"{phone}"
    text6 = f"{email}"

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
    x2, y2, lineDiff, linediff = 25, 265, 10, 7  # Assuming y2 is also in mm
    
    pdf.set_xy(x2, y2)
    pdf.set_font('Arial', 'B', 20)
    pdf.cell(text1_width, 10, text2, 0, 1, 'L')

    pdf.set_xy(x2, y2 + lineDiff)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(text1_width, 10, text3, 0, 1, 'L')


    pdf.set_font('Arial', 'B', 9.7)

    pdf.set_xy(140, y2)
    pdf.cell(text1_width, 10, text5, 0, 1, 'R')

    pdf.set_xy(140, y2 + linediff)
    pdf.cell(text1_width, 10, text6, 0, 1, 'R')

    pdf.set_xy(140, y2 + 2 * linediff)
    pdf.cell(text1_width, 10, text4, 0, 1, 'R')


def camel_case_to_title(camel_case_str):
    # Convert camelCase to Title Case
    title_str = ''.join([' ' + i if i.isupper() else i for i in camel_case_str]).title()
    return title_str.strip()





from matplotlib.patches import Circle, Patch
import matplotlib.pyplot as plt
import os
def generate_pie_chart_tables(plan, table_img_path):
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


def generate_pie_charts(pdf, pdf_dir, plans):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    header_path = os.path.join(script_dir, "img", "LHPie.png")
    pdf.image(header_path, x = 0, y = 0, w = 210)
    chart_width_mm = 70  # Define the chart's width in mm for PDF placement
    x_positions = [20, 110]  # X positions for charts on the PDF
    y_positions = [20, 110, 200]  # Y positions for charts on the PDF

    labels = ['Current Coverage', 'Shortfall']
    colors = ['#293486', '#808080']
    legend_path = os.path.join(pdf_dir, "legend.png")

    patches = [Patch(color=color, label=label) for label, color in zip(labels, colors)]

    # Create a new figure
    fig = plt.figure(figsize=(2, 2))
    # Add a legend to the figure, not to an Axes
    fig.legend(handles=patches, loc='center', frameon=False)

    # Save just the legend as an image
    fig.savefig(legend_path, bbox_inches='tight', pad_inches=0, transparent=True, dpi = 300)
    plt.close(fig)

    for i, plan in enumerate(plans):
        if i == 4:
            x_position = 65
            y_position = y_positions[i // 2]
        else:
            x_position = x_positions[i % 2]
            y_position = y_positions[i // 2]

        # Generate pie chart
        sizes = [float(plan.CurrentSumAssured), float(plan.Shortfall)]
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.pie(sizes, colors=colors, startangle=90)

        # Add a white circle in the middle to create a donut-like appearance
        centre_circle = Circle((0,0),0.60,fc='white')
        fig.gca().add_artist(centre_circle)

        ax.annotate(plan.Type, xy=(0.5, 0.95), xycoords='axes fraction', ha='center', fontsize=7, fontweight="bold")
        pie_chart_img_path = os.path.join(pdf_dir, f"pie_chart_{i}.png")
        plt.savefig(pie_chart_img_path, dpi=300, bbox_inches='tight', pad_inches=0)
        plt.close()

        # Add pie chart image to PDF
        pdf.image(pie_chart_img_path, x=x_position, y=y_position, w=chart_width_mm)
        os.remove(pie_chart_img_path)  # Clean up the pie chart image file
        
        # Overlay the wheelchair image at the center of the donut
        center_img_path = os.path.join(script_dir, "img", f"img{i}.png")
        img_size = chart_width_mm * 0.3  # Adjust size as needed
        img_x = x_position + (chart_width_mm - img_size) / 2
        img_y = y_position + (chart_width_mm - img_size) / 2
        pdf.image(center_img_path, x=img_x, y=img_y, w=img_size, h=img_size)

        # Assuming you have a function `generate_pie_chart_tables(plan, table_img_path)` defined elsewhere
        table_img_path = os.path.join(pdf_dir, f"table_{i}.png")
        generate_pie_chart_tables(plan, table_img_path)

        table_y_position = y_positions[i // 2] + 65  # Adjust based on the actual size of the pie charts
        pdf.image(table_img_path, x=x_position, y=table_y_position, w=chart_width_mm)
        os.remove(table_img_path)

    # Place the legend on the PDF
    pdf.image(legend_path, x=160, y=260, w=40)
    os.remove(legend_path)