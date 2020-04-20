import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fpdf import FPDF
import time

def print_receipt(name , email):
    """
    Print receipts related to specified Student
    Contain all three amounts paid - mess fees, room rent, amenities charge
    """

    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page('P')
    pdf.set_font('arial', '', 18)
    pdf.image('/home/anirudh/Downloads/AI_Startup_Prototype-master/flaskSaaS-master/app/views/logo.png', x = 50, y = None, w = 100, h = 38.5, type = '', link = '')
    pdf.ln()
    pdf.multi_cell(0, 5, ' ')
    pdf.ln()

    pdf.multi_cell(0, 5, 'Medisync Payment Receipt')
    pdf.ln()
    pdf.set_font('arial', '', 10)
    pdf.multi_cell(0, 5, ('Customer Name: %s' % name), border= 1,align='C')
    pdf.ln()

    pdf.multi_cell(0, 5, ('Email: %s' % email), border= 1,align='C')
    pdf.ln()

    pdf.multi_cell(0, 5, ('Total Amount Paid: %s' % '10$'), border= 1,align='C')
    pdf.ln()

    pdf.multi_cell(0, 5, ('Payment Method: %s' % 'Stripe Online'), border= 1,align='C')
    pdf.ln()
    pdf.ln()
    pdf.ln()
    pdf.ln()
    pdf.ln()
    pdf.ln()
    pdf.ln()
    pdf.ln()
    pdf.ln()
    pdf.ln()
    pdf.ln()
    pdf.ln()
    pdf.ln()
    pdf.ln()
    pdf.ln()
    pdf.ln()
    pdf.ln()
    pdf.ln()
    pdf.set_font('arial','', 6)

    pdf.multi_cell(0, 5, 'Copyright @Medisync 2020')





    # Write generated output file to PDF
    pdf.output('report.pdf' , 'F') 


def write_email(name, email, prob):
    print_receipt(name, email)

    subject = 'Results of MediSync Scan'
    body = """\
    Hey {}, 

    Your results from MediSync's Chest X-ray Scan are ready. 

    Our system predicts that there is a {}% chance that you have pneumonia.

    Please have a look at our website for more information about this disease.

    Seek immediate medical help if your symptoms worsen.


    Take care.


    Regards,

    The MediSync Team
    """

    email_text = """\
    From: {}
    To: {}
    Subject: {}

    {}
    """
    newbody = body.format(name, prob)
    sender_email = 'medisync.rvce@gmail.com'
    receiver_email = "anirudhk2510@gmail.com"
    password = 'medisync2020'

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(newbody, "plain"))

    filename = "report.pdf"  # In same directory as script

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

