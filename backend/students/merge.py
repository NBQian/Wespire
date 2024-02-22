import pypdf

def merge_headers_with_document(main_pdf_path, header1_path, header2_path, output_pdf_path):
    # Open the main document and the header PDFs
    with open(main_pdf_path, "rb") as main_pdf_file, \
         open(header1_path, "rb") as header1_file, \
         open(header2_path, "rb") as header2_file:
        
        main_pdf = pypdf.PdfReader(main_pdf_file)
        header1_pdf = pypdf.PdfReader(header1_file)
        header2_pdf = pypdf.PdfReader(header2_file)
        
        # Prepare a PDF writer for the output document
        pdf_writer = pypdf.PdfWriter()

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
        for i in range(2, len(main_pdf.pages)):
            pdf_writer.add_page(main_pdf.pages[i])

        # Write the modified document to a new file
        with open(output_pdf_path, "wb") as output_pdf_file:
            pdf_writer.write(output_pdf_file)

# Specify the paths to your files
main_pdf_path = "plswork.pdf"
header1_path = "header1.pdf"
header2_path = "header2.pdf"
output_pdf_path = "plswork.pdf"


merge_headers_with_document(main_pdf_path, header1_path, header2_path, output_pdf_path)
