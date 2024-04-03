from fpdf import FPDF

# Create instance of FPDF class
pdf = FPDF()

# Add a page
pdf.add_page()

# Set auto page break
pdf.set_auto_page_break(auto=True, margin=0)

# Remove margins
pdf.set_margins(0, 0, 0)

# Specify the path to your PNG image
image_path = 'disclaimer.png'

# Add the image to the PDF, specify x, y, width, and height
# A4 size in mm (adjust slightly if needed to fit the whole page due to default margins)
pdf.image(image_path, x=0, y=0, w=210, h=297)

# Save the PDF to a file
pdf.output('output.pdf')

