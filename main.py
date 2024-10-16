import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


load_dotenv()

email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

url = "https://www.amazon.fr/GIGABYTE-GeForce-Gaming-NVIDIA-GDDR6X/dp/B0BH8MK76C/ref=sr_1_2?crid=3A70G42OHW9PB&dib=eyJ2IjoiMSJ9.eP_1N8F2KbSzRN2z_Re3W_QkkP5RlhpdiM5LLNMJy9vKWMIVpHJ9mL0JxtxRQG2IaVREmANfgGbfnRjC9UcwsJIQjUMQ8979lNSxLWLnyUcR3IbI4OUJV174pmTeqr4Zso9DsRqMP3gcZu_UlLsNnmSIdEox7aPhiTzeHd67fx3NDbaKSpXvIYUGGJcLOk-UfPXBcy0DQyFOfIyeUCADRll06jGk6A3Mng0bv7D2_f9q-c93sFjDpHn_WOuxDOOV1xRKCIzsOckBF257iKjnoK8aBxHI3Jy1mp2QHMbD2K8.az0mWjDkr_7NUchOKVZSepIh7m-g8zJ8sPlCtUnCjsw&dib_tag=se&keywords=rtx+4090&qid=1729098471&sprefix=rtx%2Caps%2C110&sr=8-2"

response = requests.get(url)

html_doc = response.content

soup = BeautifulSoup(html_doc, "html.parser")

price = soup.find(class_="a-offscreen").get_text()

price_cleaned = price.replace("\u202f", "").replace(",",".")

price_as_float = float(price_cleaned[:-1])

title = soup.find(id="productTitle").get_text().strip()

message = f"{title} is now {price_as_float}{price_cleaned[-1]}\n{url}"

if price_as_float < 2000:

    msg = MIMEMultipart()
    msg["From"] = email
    msg["To"] = email
    msg["Subject"] = "Amazon Price Alert"

    msg.attach(MIMEText(message, 'plain', 'utf-8'))

    s = smtplib.SMTP("smtp.gmail.com", 587)

    s.starttls()
    s.login(email, password)

    s.sendmail(email, email, msg.as_string())

    s.quit()



