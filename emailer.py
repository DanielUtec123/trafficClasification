from email.mime.text import MIMEText
from smtplib import SMTP

from config import *



import random
import string 


def generateText():
    n = random.randint(10, 300)
    
    text = ""

    for i in range(n):
        l = random.randint(3,11)
        word = "".join( [random.choice(string.ascii_letters) for i in range(l)] )
        text += word + " "
    return text


def sendRandomEmail():
    text = generateText()

    from_address = EMAIL
    to_address = "danieljulianrojascruz@gmail.com"
    message = text
    mime_message = MIMEText(message, "plain")

    mime_message['From'] = from_address
    mime_message['To'] = to_address
    mime_message['Subject'] = "Recolecting Data"

    smtp = SMTP("smtp.gmail.com","587")
    smtp.starttls()
    smtp.login(from_address, PASSWORD)
    smtp.sendmail(from_address, to_address, mime_message.as_string())
    smtp.quit()

sendRandomEmail()