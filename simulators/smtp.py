import smtplib
from email.message import EmailMessage
import getpass

# Create an EmailMessage object
msg = EmailMessage()

# Set the sender and recipient email addresses
msg['From'] = 'abahp22@gmail.com'  # Replace with your email address
msg['To'] = 'ripplepete@example.com'  # Replace with the recipient's email address
msg['Subject'] = 'Email with Attachment'

# Add the email body
msg.set_content('Hello, this is an email with an attachment.')

# Add the attachment

with open("attachment.txt", 'rb') as file:
    attachment_data = file.read()
msg.add_attachment(attachment_data, filename='attachment.txt', maintype='application', subtype='octet-stream')

# Set up the SMTP server and login
smtp_server = 'smtp.gmail.com'  # Replace with the SMTP server of your email provider
smtp_port = 587  # For Gmail, use 587 with TLS
smtp_username = 'your_email@gmail.com'  # Replace with your email address
smtp_password = getpass.getpass('Enter your email password: ')

# Connect to the SMTP server
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()  # Enable TLS encryption
    server.login(smtp_username, smtp_password)
    server.send_message(msg)

print('Email sent successfully.')
