import smtplib, ssl #just this for plain text email
from email.mime.text import MIMEText #for fancy email
from email.mime.multipart import MIMEMultipart  #for fancy email
from email.mime.image import MIMEImage

#for attachment
from email import encoders
from email.mime.base import MIMEBase


#https://myaccount.google.com/lesssecureapps make sure this is on

def plaintextemail():
    port = 465
    password = input("password here: ")

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("cdcoldem99@gmail.com", password)

        sender_email = "cdcoldem99@gmail.com"
        receiver_email = "colleen.demaris@gmail.com"
        message = """\
            Subject: hi there

            This message is from python"""


        server.sendmail(sender_email, receiver_email, message)


def fancyemail():
    sender_email = "cdcoldem99@gmail.com"
    receiver_email = "colleen.demaris@gmail.com"
    password = input("password here: ")
    port = 465
    context = ssl.create_default_context()

    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email

    html = """\
    <html>
        <body>
            <p>Hi,<br>
                How are you?<br>
                <img src="cid:image1" alt="puppy">
            </p>
        </body>
    </html>
    """

    part2 = MIMEText(html, "html")
    message.attach(part2)

    fp = open('test.jpg', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    msgImage.add_header('Content-ID', '<image1>')
    message.attach(msgImage)

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def emailattach():
    subject = "An email with attachment from Python"
    body = "This is an email with attachment sent from Python"
    sender_email = "cdcoldem99@gmail.com"
    receiver_email = "colleen.demaris@gmail.com"
    password = input("Type your password and press enter:")

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = "test.pdf"  # In same directory as script

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


def imageemail():
    # Define these once; use them twice!
    strFrom = 'cdcoldem99@gmail.com'
    strTo = 'colleen.demaris@gmail.com'

    # Create the root message and fill in the from, to, and subject headers
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = 'test message'
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot.preamble = 'This is a multi-part message in MIME format.'

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText('This is the alternative plain text message.')
    msgAlternative.attach(msgText)

    # We reference the image in the IMG SRC attribute by the ID we give it below
    msgText = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>Nifty!', 'html')
    msgAlternative.attach(msgText)

    # This example assumes the image is in the current directory
    fp = open('test.jpg', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)

    # Send the email (this example assumes SMTP authentication is required)
    import smtplib
    smtp = smtplib.SMTP()
    smtp.connect('smtp.example.com')
    smtp.login('exampleuser', 'examplepass')
    smtp.sendmail(strFrom, strTo, msgRoot.as_string())
    smtp.quit()

plaintextemail()