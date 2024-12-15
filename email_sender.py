import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd



def load_email_data(json_file):
    try:
        with open(json_file, 'r') as file:
            email_data = json.load(file)
        return email_data
    except FileNotFoundError:
        print("Error: The specified JSON file was not found.")
        return None
    except json.JSONDecodeError:
        print("Error: The JSON file is not properly formatted.")
        return None

def send_email(email_data, smtp_server, smtp_port, smtp_user, smtp_password, dataframe=None):
    msg = MIMEMultipart("alternative")  # Use 'alternative' to handle plain and HTML content
    msg['From'] = email_data['from']
    msg['To'] = ", ".join(email_data['to'])
    msg['Cc'] = ", ".join(email_data['cc']) if 'cc' in email_data else ""
    msg['Bcc'] = ", ".join(email_data['bcc']) if 'bcc' in email_data else ""
    msg['Subject'] = email_data['subject']

    # Add plain text body
    plain_body = email_data['body']
    msg.attach(MIMEText(plain_body, 'plain'))

    # If a DataFrame is provided, convert it to an HTML table and embed it
    if dataframe is not None:
        df_html = dataframe.to_html(index=False, border=0)
        html_body = f"""
        <html>
        <body>
            <h2>{email_data.get('heading', 'Report')}</h2>
            {df_html}
        </body>
        </html>
        """
        msg.attach(MIMEText(html_body, 'html'))
    else:
        # Provide a fallback if no dataframe is passed
        html_body = f"""
        <html>
        <body>
            <h2>{email_data.get('heading', 'Report')}</h2>
            <p>No data available.</p>
        </body>
        </html>
        """
        msg.attach(MIMEText(html_body, 'html'))

    # Consolidate all recipients
    recipients = email_data['to'] + email_data.get('cc', []) + email_data.get('bcc', [])
    
    try:
        # Establish a connection with the SMTP server
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(email_data['from'], recipients, msg.as_string())
            print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")


df = pd.read_excel('read.xlsx')
email_data = load_email_data('email_data.json')
send_email(
    email_data,
    smtp_server='smtp.gmail.com',
    smtp_port=465,
    smtp_user='sharmakshitij48@gmail.com',
    smtp_password="your pass",
    dataframe=df,
)
