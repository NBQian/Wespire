import re
import datetime
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
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Image
from reportlab.graphics.shapes import Drawing
from reportlab.lib.styles import getSampleStyleSheet
from fpdf import FPDF
import matplotlib.pyplot as plt
import os

plt.switch_backend('Agg')  # Use the Agg backend for Matplotlib

class PDF(FPDF):
    pass

def queryset_to_list_of_dicts(queryset):
    list_of_dicts = []
    for product in queryset:
        product_dict = {}
        for field in product._meta.fields:
            field_name = field.name
            field_value = getattr(product, field_name)

            # Special handling for date and datetime fields to format them as strings
            if isinstance(field_value, (datetime.date, datetime.datetime)):
                product_dict[field_name] = field_value.strftime('%Y-%m-%d')
            else:
                product_dict[field_name] = field_value

        list_of_dicts.append(product_dict)
    return list_of_dicts

def generate_pdf(student_summary):
    filename = f"client_{student_summary.student.FirstName}_{student_summary.student.LastName}_{student_summary.date_created}.pdf"
    pdf_dir = os.path.join(settings.MEDIA_ROOT, 'client_summaries')
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
    pdf_path = os.path.join(pdf_dir, filename)

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
    add_tables_to_pdf(products, pdf)

    # Bar Graph Page
    add_bar_graph_to_pdf(pdf, products)

    # Pie Chart Page
    pdf.add_page()
    generate_pie_charts(student_summary, pdf, pdf_dir, plans)


    pdf.output(pdf_path)

    return os.path.join('client_summaries', filename)
######
def add_tables_to_pdf(products, pdf):
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=9)  # Adjust the font size as needed
    
    excluded_fields = ['unique_code', 'id', 'Type']
    filtered_fields = [field for field in list(products[0].keys()) if field not in excluded_fields]

    custom_headers = {
        "TotalPermanentDisability": "TPD SA",
        "TotalDeathCoverage": "Death SA",
        "OtherBenefitsRemarks": "Remarks",
    }

    def get_custom_header(field):
        """Transform field names into custom headers or default to camel case words."""
        return custom_headers.get(field, camel_case_to_words(field))

    first_half_fields = filtered_fields[:12]
    second_half_fields = filtered_fields[12:]

    first_half_headers = ["No."] + [get_custom_header(field) for field in first_half_fields]
    second_half_headers = ["No."] + [get_custom_header(field) for field in second_half_fields]

    def calculate_column_widths(headers, data):
        """Calculate column widths based on the content."""
        pdf.set_font("Arial", size=9)  # Ensure the font is set for width calculations
        header_widths = [pdf.get_string_width(header) + 2 for header in headers]  # Add a small margin
        data_widths = [max(pdf.get_string_width(str(row[i])) for row in data) + 2 for i in range(len(headers))]
        column_widths = [max(header, data) for header, data in zip(header_widths, data_widths)]
        total_width = sum(column_widths)
        if total_width < (pdf.w - 30):  # If total width of columns is less than page width
            extra_space = (pdf.w - 30 - total_width) / len(headers)
            column_widths = [w + extra_space for w in column_widths]  # Distribute extra space among columns
        return column_widths

    def add_table(headers, data, start_y, header_path):
        """Add a table to the PDF, centering it on the page."""
        pdf.image(header_path, x=0, y=0, w=297)  # Add the header image
        pdf.set_y(start_y)
        column_widths = calculate_column_widths(headers, data)
        table_width = sum(column_widths)
        start_x = (pdf.w - table_width) / 2  # Calculate start_x to center the table
        pdf.set_x(start_x)

        # Header
        pdf.set_fill_color(41, 52, 134)  # Header background color
        pdf.set_text_color(255, 255, 255)  # Header text color
        for i, header in enumerate(headers):
            pdf.cell(column_widths[i], 10, header, border=1, fill=True)
        pdf.ln(10)

        # Rows
        pdf.set_text_color(0, 0, 0)  # Reset text color for rows
        fill = False
        for row in data:
            pdf.set_x(start_x)  # Align rows with the header
            if fill:
                pdf.set_fill_color(230, 230, 230)  # Light gray for alternating rows
            else:
                pdf.set_fill_color(255, 255, 255)  # White for non-alternating rows
            for i, cell in enumerate(row):
                pdf.cell(column_widths[i], 10, str(cell), border=1, fill=fill)
            pdf.ln(10)
            fill = not fill 

    data = [[i+1] + [str(product[field]) for field in filtered_fields] for i, product in enumerate(products)]

    # Paths for header images
    script_dir = os.path.dirname(os.path.abspath(__file__))
    header_path1 = os.path.join(script_dir, "img", "LHTable1.png")
    header_path2 = os.path.join(script_dir, "img", "LHTable2.png")

    # Add the tables with headers
    pdf.add_page(orientation='L')
    add_table(first_half_headers, [[row[0]] + row[1:len(first_half_fields)+1] for row in data], 40, header_path1)
    
    pdf.add_page(orientation='L')
    add_table(second_half_headers, [[row[0]] + row[len(first_half_fields)+1:] for row in data], 40, header_path2)
######


def add_bar_graph_to_pdf(pdf, products):
    # Generate data for the bar graph
    categories, values = create_bar_graph_data(products)
    
    # Create the bar graph image
    create_bar_graph(categories, values)
    
    # Ensure the bar graph image is saved to a known location
    bar_graph_image_path = 'bar_graph.png'
    
    # Add a new horizontal page for the bar graph
    pdf.add_page(orientation='L')
    
    # Calculate image position to center it (assuming A4 landscape)
    pdf_width = 297  # A4 width in mm
    pdf_height = 210  # A4 height in mm
    img_width = 200  # Adjust based on your image size
    img_height = 100  # Adjust based on your image size
    x_centered = (pdf_width - img_width) / 2
    y_centered = (pdf_height - img_height) / 2
    
    # Insert the bar graph image into the PDF
    pdf.image(bar_graph_image_path, x=x_centered, y=y_centered, w=img_width, h=img_height)





from reportlab.lib import pagesizes, colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import mm
import re
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, PageBreak
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.colors import HexColor
from reportlab.pdfgen.canvas import Canvas


# Assuming 'products' is your list of product dictionaries

def create_bar_graph_data(products):
    # Initialize sums for each category
    categories = ['TotalDeathCoverage', 'TotalPermanentDisability', 'EarlyCriticalIllness', 'CriticalIllness', 'Accidental']
    sums = {category: 0 for category in categories}
    
    # Sum up the amounts for each category
    for product in products:
        for category in categories:
            sums[category] += product.get(category, 0)
    
    return categories, list(sums.values())

def create_bar_graph(categories, decimal_values):
    values = [float(val) for val in decimal_values]
    drawing_width = 842
    drawing_height = 400
    chart_width = 500
    # Increased width for better separation of field names
    drawing = Drawing(drawing_width, drawing_height)  # Adjusted width to 600
    bc = VerticalBarChart()
    bc.x = (drawing_width - chart_width) / 2
    bc.y = 50
    bc.height = 300
    bc.width = chart_width  # Adjusted width to 500 for the chart itself

    bc.data = [values]
    bc.barWidth = 10
    bc.categoryAxis.categoryNames = [camel_case_to_words(cat) for cat in categories]
    bc.categoryAxis.labels.boxAnchor = 'n'
    # bc.categoryAxis.labels.angle = 45  # Optional: Rotate labels if still cramped

    max_value = max(values)
    valueMax = max_value + (10 - max_value % 10)
    valueStep = valueMax / 10

    bc.barSpacing = 15
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = valueMax
    bc.valueAxis.valueStep = valueStep
    bc.barLabelFormat = '$%d'
    bc.barLabels.nudge = 10

    # Set the bar color to #293486
    bc.bars[0].fillColor = HexColor("#293486")

    drawing.add(bc)
    
    return drawing

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def create_bar_graph(categories, values):
    plt.figure(figsize=(10, 6))

    # Make the bars narrower by specifying the width
    bars = plt.bar(categories, values, color='#293486', width=0.4)  # Adjust width as needed

    # Remove top and right spines
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    # Format y-axis with dollar sign
    formatter = FuncFormatter(lambda x, _: f'${x}')
    plt.gca().yaxis.set_major_formatter(formatter)

    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height}', ha='center', va='bottom')

    plt.ylabel('Sum Assured', labelpad=20)
    plt.title('Current Protections', pad=10)
    plt.xticks(rotation=45, ha='right')  # Rotate labels for better fit
    plt.tight_layout()
    plt.savefig('bar_graph.png', dpi = 300)
    plt.close()


    

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





from matplotlib.patches import Circle
import matplotlib.pyplot as plt
import os
from matplotlib.patches import Patch

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


def generate_pie_charts(student_summary, pdf, pdf_dir, plans):
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

        # Assuming you have a function `generate_table_image(plan, table_img_path)` defined elsewhere
        table_img_path = os.path.join(pdf_dir, f"table_{i}.png")
        generate_table_image(plan, table_img_path)

        table_y_position = y_positions[i // 2] + 65  # Adjust based on the actual size of the pie charts
        pdf.image(table_img_path, x=x_position, y=table_y_position, w=chart_width_mm)
        os.remove(table_img_path)

    # Place the legend on the PDF
    pdf.image(legend_path, x=160, y=260, w=40)
    os.remove(legend_path)