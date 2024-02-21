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
    # generate_product_tables(products, "products_tables.pdf")
    # add_tables_to_pdf(products, pdf)
    # generate_product_tables_matplotlib(products)
    create_pdf_with_tables(products, "plswork.pdf")

    # Bar Graph Page
    add_bar_graph_to_pdf(pdf, products)

    # Pie Chart Page
    pdf.add_page()
    generate_pie_charts(student_summary, pdf, pdf_dir, plans)


    pdf.output(pdf_path)

    return os.path.join('client_summaries', filename)
# ######
# def add_tables_to_pdf(products, pdf):
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.set_font("Arial", size=9)  # Adjust the font size as needed
    
#     excluded_fields = ['unique_code', 'id', 'Type']
#     filtered_fields = [field for field in list(products[0].keys()) if field not in excluded_fields]

#     custom_headers = {
#         "TotalPermanentDisability": "TPD SA",
#         "TotalDeathCoverage": "Death SA",
#         "OtherBenefitsRemarks": "Remarks",
#     }

#     def get_custom_header(field):
#         """Transform field names into custom headers or default to camel case words."""
#         return custom_headers.get(field, camel_case_to_words(field))

#     first_half_fields = filtered_fields[:12]
#     second_half_fields = filtered_fields[12:]

#     first_half_headers = ["No."] + [get_custom_header(field) for field in first_half_fields]
#     second_half_headers = ["No."] + [get_custom_header(field) for field in second_half_fields]

#     def calculate_column_widths(headers, data):
#         """Calculate column widths based on the content."""
#         pdf.set_font("Arial", size=9)  # Ensure the font is set for width calculations
#         header_widths = [pdf.get_string_width(header) + 2 for header in headers]  # Add a small margin
#         data_widths = [max(pdf.get_string_width(str(row[i])) for row in data) + 2 for i in range(len(headers))]
#         column_widths = [max(header, data) for header, data in zip(header_widths, data_widths)]
#         total_width = sum(column_widths)
#         if total_width < (pdf.w - 30):  # If total width of columns is less than page width
#             extra_space = (pdf.w - 30 - total_width) / len(headers)
#             column_widths = [w + extra_space for w in column_widths]  # Distribute extra space among columns
#         return column_widths

#     def add_table(headers, data, start_y, header_path):
#         """Add a table to the PDF, centering it on the page."""
#         pdf.image(header_path, x=0, y=0, w=297)  # Add the header image
#         pdf.set_y(start_y)
#         column_widths = calculate_column_widths(headers, data)
#         table_width = sum(column_widths)
#         start_x = (pdf.w - table_width) / 2  # Calculate start_x to center the table
#         pdf.set_x(start_x)

#         # Header
#         pdf.set_fill_color(41, 52, 134)  # Header background color
#         pdf.set_text_color(255, 255, 255)  # Header text color
#         for i, header in enumerate(headers):
#             pdf.cell(column_widths[i], 10, header, border=1, fill=True)
#         pdf.ln(10)

#         # Rows
#         remarks_index = headers.index("Remarks") if "Remarks" in headers else None
#         fill = False
#         for row in data:
#             pdf.set_x(start_x)  # Align rows with the header
#             max_height = 10  # Default height, adjust based on text wrapping
            
#             # First, determine the maximum height needed for this row
#             for i, cell in enumerate(row):
#                 if i == remarks_index:  # Apply wrap_text for "Remarks" column
#                     wrapped_text = wrap_text(str(cell), column_widths[i], pdf)
#                     # Estimate height needed for the wrapped text
#                     num_lines = len(wrapped_text.split('\n'))
#                     cell_height = num_lines * 10  # Assuming 10 is height per line, adjust as needed
#                     max_height = max(max_height, cell_height)

#             if fill:
#                 pdf.set_fill_color(230, 230, 230)  # Light gray for alternating rows
#             else:
#                 pdf.set_fill_color(255, 255, 255)  # White for non-alternating rows

#             # Then, render each cell with the determined height
#             for i, cell in enumerate(row):
#                 if i == remarks_index and remarks_index is not None:  # Again, special handling for "Remarks"
#                     wrapped_text = wrap_text(str(cell), column_widths[i], pdf)
#                     pdf.multi_cell(column_widths[i], 10, wrapped_text, border=1, fill=fill, align='L')
#                     pdf.set_x(start_x + sum(column_widths[:i+1]))  # Move X to the next cell start position
#                     pdf.set_y(pdf.get_y() - max_height)  # Reset Y to the top of the current row
#                 else:
#                     # For other cells, use the original text but adjust the height as needed
#                     pdf.cell(column_widths[i], max_height, str(cell), border=1, fill=fill, ln=0)
            
#             pdf.ln(max_height)  # Move to the next line after the tallest cell in the row
#             fill = not fill

#     def wrap_text(text, max_width, pdf):
#         """
#         Wrap text to fit within the specified width.
#         Args:
#             text (str): The text to wrap.
#             max_width (float): The maximum width of the text area.
#             pdf (FPDF): The PDF object for measuring text width.
#         Returns:
#             str: The wrapped text with newline characters inserted as necessary.
#         """
#         words = text.split()
#         if not words:
#             return text

#         wrapped_text = words[0]
#         current_width = pdf.get_string_width(words[0])

#         for word in words[1:]:
#             space_width = pdf.get_string_width(' ')
#             word_width = pdf.get_string_width(word)
#             if current_width + space_width + word_width <= max_width:
#                 wrapped_text += ' ' + word
#                 current_width += space_width + word_width
#             else:
#                 wrapped_text += '\n' + word
#                 current_width = word_width

#         return wrapped_text


#     data = [[i+1] + [str(product[field]) for field in filtered_fields] for i, product in enumerate(products)]

#     # Paths for header images
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     header_path1 = os.path.join(script_dir, "img", "LHTable1.png")
#     header_path2 = os.path.join(script_dir, "img", "LHTable2.png")

#     # Add the tables with headers
#     pdf.add_page(orientation='L')
#     add_table(first_half_headers, [[row[0]] + row[1:len(first_half_fields)+1] for row in data], 40, header_path1)
    
#     pdf.add_page(orientation='L')
#     add_table(second_half_headers, [[row[0]] + row[len(first_half_fields)+1:] for row in data], 40, header_path2)
# ######

# def create_pdf_with_tables(products, pdf_path):
#     # Assuming 'products' is a list of dictionaries
#     # Dynamically excluding 'unique_code' and 'id' and then adding a "No." column
#     excluded_fields = ['unique_code', 'id', 'Type']
#     filtered_fields = [field for field in list(products[0].keys()) if field not in excluded_fields]

#     first_half_fields = filtered_fields[:len(filtered_fields)//2]
#     second_half_fields = filtered_fields[len(filtered_fields)//2:]

#     # Adding "No." as the first header for both tables
#     first_half_headers = ["No."] + [camel_case_to_words(field) for field in first_half_fields]
#     second_half_headers = ["No."] + [camel_case_to_words(field) for field in second_half_fields]

#     # Adding row numbers to the data for both tables
#     first_half_data = [[i+1] + [product[field] for field in first_half_fields] for i, product in enumerate(products)]
#     second_half_data = [[i+1] + [product[field] for field in second_half_fields] for i, product in enumerate(products)]

#     # Setup the document in landscape orientation
#     doc = SimpleDocTemplate(pdf_path, pagesize=landscape(A4))

#     # Define table styles with header color modifications
#     table_style = TableStyle([
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#         ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
#         ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
#         ('FONTSIZE', (0, 0), (-1, -1), 8),
#         ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#293486")),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
#     ])

#     # Create and style the first table
#     first_table = Table([first_half_headers] + first_half_data)
#     first_table.setStyle(table_style)

#     # Create and style the second table
#     second_table = Table([second_half_headers] + second_half_data)
#     second_table.setStyle(table_style)

#     categories, sums = create_bar_graph_data(products)
#     # graph = create_bar_graph([camel_case_to_words(cat) for cat in categories], sums)
#     elements = [first_table, PageBreak(), second_table]
#     doc.build(elements)
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
def create_pdf_with_tables(products, pdf_path):
    custom_headers = {
    "TotalPermanentDisability": "TPD SA",
    "TotalDeathCoverage": "Death SA",
    "OtherBenefitsRemarks": "Remarks",
    }
    excluded_fields = ['unique_code', 'id', 'Type']
    filtered_fields = [field for field in list(products[0].keys()) if field not in excluded_fields]

    first_half_fields = filtered_fields[:12]
    second_half_fields = filtered_fields[12:]

    first_half_headers = ["No."] + [custom_headers.get(field, camel_case_to_words(field)) for field in first_half_fields]
    second_half_headers = ["No."] + [custom_headers.get(field, camel_case_to_words(field)) for field in second_half_fields]

    stylesheet = getSampleStyleSheet()
    remarks_style = ParagraphStyle('remarks_style', parent=stylesheet['Normal'], fontSize=8, spaceBefore=0, spaceAfter=0, leftIndent=0, rightIndent=0, firstLineIndent=0, leading=9, wordWrap='CJK')

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

    doc = SimpleDocTemplate(pdf_path, pagesize=landscape(A4))
    # table_style = TableStyle([
    #     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    #     ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    #     ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
    #     ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    #     ('FONTSIZE', (0, 0), (-1, -1), 8),
    #     ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#293486")),
    #     ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    # ])
    def get_table_style():
        return TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#293486")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ] + [
            ('BACKGROUND', (0, i), (-1, i), colors.white if i % 2 == 1 else colors.HexColor("#e6e6e6"))
            for i in range(1, max(len(first_half_data), len(second_half_data)) + 1)
        ])
    table_style = get_table_style()
    # Specify column widths for the second table, fixed width for "OtherBenefitsRemarks"
    col_widths_second_half = [None] + [35 * mm] + [None] * (len(second_half_headers) - 2)

    first_table = Table([first_half_headers] + first_half_data)
    second_table = Table([second_half_headers] + second_half_data, colWidths=col_widths_second_half)

    first_table.setStyle(table_style)
    second_table.setStyle(table_style)

    elements = [first_table, PageBreak(), second_table]
    doc.build(elements)
# ***

# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.colors import Color, black, white, grey
# from reportlab.lib.pagesizes import A4, landscape
# from reportlab.lib.units import mm
# from reportlab.platypus import PageBreak
# from reportlab.lib.units import mm
# import math

# def generate_product_tables(products, filename):
#     doc = SimpleDocTemplate(filename, pagesize=landscape(A4))
#     stylesheet = getSampleStyleSheet()
#     cell_style = ParagraphStyle('cell_style',
#                                 parent=stylesheet['Normal'],
#                                 fontSize=10,
#                                 wordWrap='CJK')

#     # Filter and prepare data for tables
#     excluded_fields = ['Type', 'id', 'unique_code']
#     filtered_fields = [field for field in products[0].keys() if field not in excluded_fields]
#     first_half_fields = filtered_fields[:12]
#     second_half_fields = filtered_fields[12:]
    
#         # Helper function to process product dict into table data, handling paragraph fields
#     def process_product(product, fields):
#         return [Paragraph(product[field], cell_style) if field == "OtherBenefitsRemarks" else product[field] for field in fields]
#     # Now, when preparing table data, use these updated headers for the first row
#     table1_data = [first_half_fields] + [process_product(product, first_half_fields) for product in products]
#     table2_data = [second_half_fields] + [process_product(product, second_half_fields) for product in products]



#     def calculate_column_widths(data, headers, fixed_widths):
#         # Assuming an average character width for a 10-point font is around 2mm for simplicity
#         # This is a rough approximation and might need adjustment for more accuracy
#         char_width = 2 * mm
#         # Initialize column widths with header lengths
#         col_widths = [len(header) * char_width for header in headers]

#         # Adjust column widths based on data
#         for row in data[1:]:  # Skip header row
#             for i, cell in enumerate(row):
#                 if isinstance(cell, Paragraph):
#                     # Estimate text width within the Paragraph, assuming no line breaks for simplicity
#                     text_width = len(cell.text) * char_width
#                 else:
#                     text_width = len(str(cell)) * char_width
#                 col_widths[i] = max(col_widths[i], text_width)

#         # Apply fixed widths for specific fields
#         for i, header in enumerate(headers):
#             if header in fixed_widths:
#                 col_widths[i] = fixed_widths[header]

#         # Add a small buffer to each column width to ensure content fits well
#         col_widths = [width + 5 * mm for width in col_widths]

#         return col_widths
    
#     # Calculate column widths based on content
#     col_widths_1 = calculate_column_widths(table1_data, first_half_fields, {"OtherBenefitsRemarks": 30*mm})
#     col_widths_2 = calculate_column_widths(table2_data, second_half_fields, {"OtherBenefitsRemarks": 30*mm})

#     # Create and style the tables
#     table1 = Table(table1_data, colWidths=col_widths_1, repeatRows=1)
#     table2 = Table(table2_data, colWidths=col_widths_2, repeatRows=1)

#     # Define common table style
#     common_style = [('BACKGROUND', (0,0), (-1,0), grey),
#                     ('TEXTCOLOR', (0,0), (-1,-1), black),
#                     ('ALIGN', (0,0), (-1,-1), 'LEFT'),
#                     ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
#                     ('BOTTOMPADDING', (0,0), (-1,-1), 6),
#                     ('GRID', (0,0), (-1,-1), 1, black)]
#     # Apply alternating row colors and common styles
#     def style_table(table):
#         style = TableStyle(common_style + [('BACKGROUND', (0,row), (-1,row), white if row % 2 == 0 else Color(230/255, 230/255, 230/255)) for row in range(1, len(table._cellvalues))])
#         table.setStyle(style)

#     style_table(table1)
#     style_table(table2)

#     # Build the document with the tables on separate pages
#     elements = [table1, PageBreak(), table2]
#     doc.build(elements)

# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.colors import Color, black, white, grey
# from reportlab.lib.pagesizes import A4, landscape
# from reportlab.lib.units import mm
# import math

# def generate_product_tables(products, filename):
#     doc = SimpleDocTemplate(filename, pagesize=landscape(A4))
#     stylesheet = getSampleStyleSheet()
#     cell_style = ParagraphStyle('cell_style',
#                                 parent=stylesheet['Normal'],
#                                 fontSize=10,
#                                 wordWrap='CJK')

#     # Custom headers mapping
#     custom_headers = {
#         "TotalPermanentDisability": "TPD SA",
#         "TotalDeathCoverage": "Death SA",
#         "OtherBenefitsRemarks": "Remarks",
#     }

#     # Filter and prepare data for tables
#     excluded_fields = ['Type', 'id', 'unique_code']
#     filtered_fields = [field for field in products[0].keys() if field not in excluded_fields]
#     # Apply custom headers mapping
#     display_fields = [custom_headers.get(field, field) for field in filtered_fields]
#     first_half_fields = display_fields[:12]
#     second_half_fields = display_fields[12:]

#     # Helper function to process product dict into table data, including applying custom headers for Paragraph fields
#     def process_product(product, original_fields):
#         return [Paragraph(product[field] if field in product else '', cell_style) if custom_headers.get(field, field) == "Remarks" else product.get(field, '') for field in original_fields]

#     # Adjust table data preparation to use original field names but apply custom headers for display
#     original_fields_first_half = filtered_fields[:12]
#     original_fields_second_half = filtered_fields[12:]

#     table1_data = [first_half_fields] + [process_product(product, original_fields_first_half) for product in products]
#     table2_data = [second_half_fields] + [process_product(product, original_fields_second_half) for product in products]

#     def calculate_column_widths(data, headers, fixed_widths):
#         char_width = 2 * mm
#         col_widths = [len(header) * char_width for header in headers]

#         for row in data[1:]:  # Skip header row
#             for i, cell in enumerate(row):
#                 if isinstance(cell, Paragraph):
#                     text_width = len(cell.text) * char_width
#                 else:
#                     text_width = len(str(cell)) * char_width
#                 col_widths[i] = max(col_widths[i], text_width)

#         for i, header in enumerate(headers):
#             if header in fixed_widths:
#                 col_widths[i] = fixed_widths[header]

#         col_widths = [width + 5 * mm for width in col_widths]
#         return col_widths

#     col_widths_1 = calculate_column_widths(table1_data, first_half_fields, {"Remarks": 30*mm, "ProductName": 30*mm})
#     col_widths_2 = calculate_column_widths(table2_data, second_half_fields, {"Remarks": 30*mm})

#     table1 = Table(table1_data, colWidths=col_widths_1, repeatRows=1)
#     table2 = Table(table2_data, colWidths=col_widths_2, repeatRows=1)

#     def style_table(table):
#         style = TableStyle([('BACKGROUND', (0,0), (-1,0), grey),
#                             ('TEXTCOLOR', (0,0), (-1,-1), black),
#                             ('ALIGN', (0,0), (-1,-1), 'LEFT'),
#                             ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
#                             ('BOTTOMPADDING', (0,0), (-1,-1), 6),
#                             ('GRID', (0,0), (-1,-1), 1, black)] +
#                            [('BACKGROUND', (0,row), (-1,row), white if row % 2 == 0 else Color(230/255, 230/255, 230/255)) for row in range(1, len(table._cellvalues))])
#         table.setStyle(style)

#     style_table(table1)
#     style_table(table2)

#     elements = [table1, PageBreak(), table2]
#     doc.build(elements)
#*#!$!()&%^#*&@$^@#*&$I^!_@$@~$~(&#(&!))
# ***
    
# # (((((())))))
#         # Function to generate a table
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_pdf import PdfPages
# from matplotlib.colors import to_rgba

# def generate_product_tables_matplotlib(products):
#     custom_headers = {
#         "TotalPermanentDisability": "TPD SA",
#         "TotalDeathCoverage": "Death SA",
#         "OtherBenefitsRemarks": "Remarks",
#     }

#     # Exclude specified fields
#     excluded_fields = ['Type', 'id', 'unique_code']
#     all_fields = [field for field in products[0].keys() if field not in excluded_fields]
    
#     # Apply custom headers to fields for display
#     display_fields = [custom_headers.get(field, field) for field in all_fields]
    
#     # Split fields into first 12 and remaining for display
#     first_half_display_fields = display_fields[:12]
#     second_half_display_fields = display_fields[12:]

#     # Split original fields into first 12 and remaining for data extraction
#     first_half_fields = all_fields[:12]
#     second_half_fields = all_fields[12:]

#     def wrap_text(text, max_width):
#         """Wrap text to the specified width."""
#         words = text.split()
#         wrapped_text = ""
#         line = ""
#         for word in words:
#             if len(line) + len(word) <= max_width:
#                 line += word + " "
#             else:
#                 wrapped_text += line.rstrip() + "\n"
#                 line = word + " "
#         wrapped_text += line.rstrip()
#         return wrapped_text

#     def prepare_table_data(fields, display_fields, wrap_fields=None, max_width=30):
#         """Prepare table data with text wrapping for specified fields."""
#         wrap_fields = wrap_fields or []
#         data = []
#         for product in products:
#             row = []
#             for field in fields:
#                 text = product.get(field, '')
#                 if field in wrap_fields:
#                     text = wrap_text(text, max_width)
#                 row.append(text)
#             data.append(row)
#         return display_fields, data



#     def adjust_row_heights(table, wrapped_field_indexes, default_height=0.05, height_per_line=0.05):
#         """Adjust the row heights in a table based on the number of lines in wrapped fields."""
#         cell_dict = table.get_celld()
#         for i in range(1, len(cell_dict)//len(wrapped_field_indexes)):  # Skip header row
#             max_lines = 1  # Default minimum lines
#             for j in wrapped_field_indexes:
#                 cell = cell_dict[(i, j)]
#                 text = cell.get_text().get_text()
#                 lines = text.count("\n") + 1  # Count lines based on line breaks
#                 max_lines = max(max_lines, lines)
            
#             # Calculate new height based on the number of lines
#             new_height = default_height + (max_lines - 1) * height_per_line
#             for j in range(len(wrapped_field_indexes)):
#                 cell_dict[(i, j)].set_height(new_height)

#     def generate_table(headers, data, filename, wrap_fields):
#         with PdfPages(filename) as pdf:
#             fig, ax = plt.subplots(figsize=(11.69, 8.27))  # A4 landscape dimensions in inches
#             ax.axis('off')
#             table = ax.table(cellText=data, colLabels=headers, loc='center', cellLoc='center')
#             table.auto_set_font_size(False)
#             table.set_fontsize(8)
#             table.auto_set_column_width(col=list(range(len(headers))))
            
#             # Find indexes of fields that have wrapped text
#             wrapped_field_indexes = [headers.index(field) for field in wrap_fields if field in headers]

#             # Correctly set header style and adjust row heights
#             for key, cell in table.get_celld().items():
#                 if key[0] == 0:  # Header row
#                     cell.set_text_props(color='white')
#                     cell.set_facecolor('darkblue')
#                 else:
#                     bg_color = 'white' if key[0] % 2 == 0 else to_rgba((230/255, 230/255, 230/255))
#                     cell.set_facecolor(bg_color)
#                     cell.set_edgecolor('black')
            
#             # Adjust row heights based on wrapped text
#             adjust_row_heights(table, wrapped_field_indexes)
            
#             plt.tight_layout()
#             pdf.savefig(fig)
#             plt.close()

#     # Generate tables with corrected headers
#     wrap_fields = ['OtherBenefitsRemarks']  # Specify which fields to wrap
#     first_headers, first_data = prepare_table_data(first_half_fields, first_half_display_fields, wrap_fields)
#     generate_table(first_headers, first_data, 'first_table.pdf', wrap_fields)
    
    
#     second_headers, second_data = prepare_table_data(second_half_fields, second_half_display_fields, wrap_fields)
#     generate_table(second_headers, second_data, 'second_table.pdf', wrap_fields)

# # (((((())))))

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
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, PageBreak, Paragraph
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