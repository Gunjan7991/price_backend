import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .config import EMAIL, PASSWORD

def send_email(to_email, subject, message):
    sender_email = EMAIL  # Replace with your Gmail address
    sender_password = PASSWORD  # Use the generated App Password

    # Create the email
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject

    # Add message body
    msg.attach(MIMEText(message, "plain"))

    try:
        # Connect to Gmail SMTP Server (SSL)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)  # Login with App Password
            server.sendmail(sender_email, to_email, msg.as_string())  # Send email

        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


