from fpdf import FPDF
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import os

def save_bar_graph(sums, filename="bar_graph.png"):
    categories = list(sums.keys())
    values = list(sums.values())

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(categories, values, color='#293486', width=0.5) 
    
    ax.tick_params(axis='x', labelsize=13, pad=13)
    ax.tick_params(axis='y', labelsize=12, pad=10)
    ax.set_title('Total Sum Assured', fontsize=20, fontname='Arial', fontweight='bold', pad=25, loc='center')


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
def add_bar_graph_to_pdf(pdf, sums):
    header_path = "CPHeader.png"
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

    add_table(pdf, sums)

    # Remove the temporary graph image file
    os.remove(graph_filename)


def add_table(pdf, sums):
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


# Example usage
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
sums = {'Total Death\nCoverage': 15000, 'Total Permanent\nDisability': 21722, 'Early Critical\nIllness': 250000, 'Critical Illness': 10000, 'Accidental': 100000}
add_bar_graph_to_pdf(pdf, sums)
pdf.output("example.pdf")
