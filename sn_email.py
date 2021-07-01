import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string

def send_email(name, email, subject, body):

    smtp_server = "smtp.gmail.com"
    port = 587

    #REMOVE BEFORE FINAL DELIVERY ##########################################################################################
    login_creds = open("creds.txt", "r")
    login_email = login_creds.readline()
    login_password = login_creds.readline()
    receiver_email = "kenan.alnakoula@hva.nl"
    #REMOVE BEFORE FINAL DELIVERY ##########################################################################################

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = login_email
    message["To"] = receiver_email

    letters = string.ascii_lowercase + string.digits + string.ascii_uppercase
    code =  ''.join(random.choice(letters) for i in range(20))

    text = f"Name: {name}\nE-mail: {email}\n\n{body}\n\nYour reference code is: {code}"

    part1 = MIMEText(text, "plain")

    message.attach(part1)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(login_email, login_password)
        server.sendmail(
            login_email, receiver_email, message.as_string()
        )