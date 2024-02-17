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



from matplotlib.patches import Circle
import matplotlib.pyplot as plt
import os
from matplotlib.patches import Patch


def generate_pie_charts(student_summary, pdf, pdf_dir, plans):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    header_path = os.path.join(script_dir, "img", "LHPie.png")
    pdf.image(header_path, x = 0, y = 0, w = 210)
    chart_width_mm = 70  # Define the chart's width in mm for PDF placement
    x_positions = [20, 110]  # X positions for charts on the PDF
    y_positions = [20, 110, 200]  # Y positions for charts on the PDF

    labels = ['Current Coverage', 'Shortfall']
    colors = ['#293486', '#ebbb36']
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