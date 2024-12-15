import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email(receiver_emails, dataframe, password):
    sender_email = "sharmakshitij48@gmail.com"
    subject = "Property Data"
    body = "Please find the attached CSV file."
    
    # Create MIME message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    
    # Convert dataframe to CSV and attach as a MIMEBase object
    csv_data = dataframe.to_csv(index=False)
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(csv_data.encode('utf-8'))
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={subject}.csv')
    message.attach(part)
    
    try:
        # Connect to SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            
            # Send email to each recipient
            for receiver_email in receiver_emails:
                message['To'] = receiver_email
                server.sendmail(sender_email, receiver_email, message.as_string())
                
        print("Emails sent successfully.")
    except Exception as e:
        print(f"Failed to send emails: {e}")


def send_email_with_dataframe(receiver_emails, dataframe, password):
    sender_email = "sharmakshitij48@gmail.com"
    subject = "Failure Report"
    
    # Convert DataFrame to HTML
    df_html = dataframe.to_html(index=False, border=0)
    
    # Email body with a heading
    body = f"""
    <html>
    <body>
        <h2>Failure Report</h2>
        {df_html}
    </body>
    </html>
    """
    
    # Create MIME message
    message = MIMEMultipart("alternative")
    message['From'] = sender_email
    message['Subject'] = subject
    
    # Attach the HTML body
    message.attach(MIMEText(body, 'html'))
    
    try:
        # Connect to SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            
            # Send email to each recipient
            for receiver_email in receiver_emails:
                message['To'] = receiver_email
                server.sendmail(sender_email, receiver_email, message.as_string())
                
        print("Emails sent successfully.")
    except Exception as e:
        print(f"Failed to send emails: {e}")


