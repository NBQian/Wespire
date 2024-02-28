# send_email.py

import os
import django
from django.core.mail import EmailMessage

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# Load HTML content from a file
with open('test.html', 'r') as file:
    html_content = file.read()

# Create and send email
email = EmailMessage(
    subject='Please freaking tell me what is going on',
    body=html_content,
    from_email='wespireutilities@gmail.com',
    to=['niuboqianabraham@gmail.com'],
)
email.content_subtype = "html"  # Specify the subtype as HTML
email.send()

print("Email sent successfully!")

