from fpdf import FPDF
import os

# Initialize FPDF class
class PDF(FPDF):
    pass

# Create a PDF instance
pdf = PDF(orientation='L', unit='mm', format='A4')

# Add a page
pdf.add_page()

# Calculate the script directory and image path
script_dir = os.path.dirname(os.path.abspath(__file__))
header_path = os.path.join(script_dir, "img", "LHTable2.png")  # Ensure this is the correct path

# Add the header image
pdf.image(header_path, x=0, y=0, w=297)  # A4 width in portrait is 210mm

# Output the PDF
output_path = os.path.join(script_dir, "header2.pdf")
pdf.output(output_path)

print(f"PDF with header image created: {output_path}")
