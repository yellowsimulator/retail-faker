import io
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from PyPDF2 import PdfWriter, PdfReader
from reportlab.platypus import SimpleDocTemplate, Preformatted, Spacer
from pygments import highlight
from pygments.lexers import PythonLexer
#from pygments.formatters import PdfFormatter



from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter
from PIL import Image
from reportlab.platypus import SimpleDocTemplate, Spacer, Image as RL_Image
from reportlab.lib.pagesizes import letter

# def append_code_to_pdf(code_text, pdf_filename):
#     # Create a buffer to build the new PDF content
#     buffer = io.BytesIO()

#     # Create a PDF document
#     doc = SimpleDocTemplate(buffer, pagesize=letter)

#     # Set up styles for the PDF
#     styles = getSampleStyleSheet()

#     # Create a Preformatted flowable for the code text
#     code_flowable = Preformatted(code_text, styles['Code'], dedent=0)

#     # Add content to the PDF
#     flowables = [Spacer(1, 12), code_flowable]
#     doc.build(flowables)

#     # Open the existing PDF and the new PDF content
#     with open(pdf_filename, 'rb') as f:
#         input_pdf = PdfReader(f)
#         buffer.seek(0)
#         new_content = PdfReader(buffer)

#         # Merge the new content with the existing PDF
#         output = PdfWriter()
#         for i in range(len(input_pdf.pages)):
#             output.add_page(input_pdf.pages[i])

#         for i in range(len(new_content.pages)):
#             output.add_page(new_content.pages[i])

#         # Save the merged PDF
#         with open(pdf_filename, 'wb') as f:
#             output.write(f)


def append_code_to_pdf(code_text, pdf_filename):
    # Create a buffer to build the new PDF content
    buffer = io.BytesIO()

    # Create a PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Highlight the code using Pygments and create an image
    img_buffer = io.BytesIO()
    highlight(code_text, PythonLexer(), ImageFormatter(line_numbers=True), outfile=img_buffer)
    img_buffer.seek(0)
    code_image = Image.open(img_buffer)

    # Convert the image to a reportlab.platypus.Image
    code_image_buffer = io.BytesIO()
    code_image.save(code_image_buffer, format='PNG')
    code_image_buffer.seek(0)
    code_rl_image = RL_Image(code_image_buffer, width=doc.width, height=doc.height, kind='proportional')

    # Add content to the PDF
    flowables = [Spacer(1, 12), code_rl_image]
    doc.build(flowables)

    # Open the existing PDF and the new PDF content
    with open(pdf_filename, 'rb') as f:
        input_pdf = PdfReader(f)
        buffer.seek(0)
        new_content = PdfReader(buffer)

        # Merge the new content with the existing PDF
        output = PdfWriter()
        for i in range(len(input_pdf.pages)):
            output.add_page(input_pdf.pages[i])

        for i in range(len(new_content.pages)):
            output.add_page(new_content.pages[i])

        # Save the merged PDF
        with open(pdf_filename, 'wb') as f:
            output.write(f)


def text_to_pdf(input_text, output_filename, title=None, is_append=False):
    # Split the input text into paragraphs using newline characters
    paragraphs = input_text.split('\n')

    # Create a buffer to build the new PDF content
    buffer = io.BytesIO()

    # Create a PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Set up styles for the PDF
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles['Title'].fontName = 'Helvetica-Bold'
    styles['Title'].fontSize = 24
    styles['Title'].alignment = TA_CENTER
    styles['Title'].spaceAfter = 20

    # Add content to the PDF
    flowables = []

    if title:
        flowables.append(Paragraph(title, styles['Title']))
        flowables.append(Spacer(1, 12))

    for text in paragraphs:
        if text.strip():
            flowables.append(Paragraph(text, styles['Justify']))
            flowables.append(Spacer(1, 12))  # Add space between paragraphs

    doc.build(flowables)

    # If is_append is True, merge the new content with the existing PDF
    if is_append and os.path.exists(output_filename):
        buffer.seek(0)
        output = PdfWriter()
        input_pdf = PdfReader(output_filename)

        # Add all pages from the existing PDF
        for i in range(len(input_pdf.pages)):
            output.add_page(input_pdf.pages[i])

        # Append the new content
        new_content = PdfReader(buffer)
        for i in range(len(new_content.pages)):
            output.add_page(new_content.pages[i])
            flowables.append(Spacer(1, 12))  # Add space between paragraphs

        # Save the merged PDF
        with open(output_filename, 'wb') as f:
            output.write(f)
    else:
        # Save the new PDF
        with open(output_filename, 'wb') as f:
            f.write(buffer.getvalue())



if __name__ == "__main__":
    long_text = "This is a sample paragraph.\n\nThis is another paragraph.\n\nThis is the third paragraph."
    output_file = "output.pdf"
    section_title = "Sample Title"

    text_to_pdf(long_text, output_file, section_title, is_append=False)
