import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email details
sender_email = "sharmakshitij48@gmail.com"
receiver_email = "1719kshitij@gmail.com"
password = "your_email_password"
subject = "Test Email"
body = "This is a test email sent from Python."

# Create MIME object
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

# Attach the body with the message
message.attach(MIMEText(body, "plain"))

try:
    # Connect to the server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:  # Use the appropriate SMTP server and port
        server.starttls()  # Secure the connection
        server.login(sender_email, password)  # Log in to the email account
        server.send_message(message)  # Send the email
        print("Email sent successfully.")
except Exception as e:
    print(f"Failed to send email: {e}")
