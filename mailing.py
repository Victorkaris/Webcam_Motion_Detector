import smtplib
from email.message import EmailMessage

# use mimetypes for many files that you are not sure of the type
# import mimetypes
PASSWORD = "ceri qjzo hykm ezpb"
SENDER = "iamawinner188@gmail.com"
RECEIVER = "iamawinner188@gmail.com"

def send_email(image_path):
    email_message = EmailMessage()
    email_message['Subject']= "New customer showed up"
    email_message.set_content("hey, we just saw a new customer!")

    with open(image_path, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype="png")

    # mime_type = mimetypes.guess_type("image/{count}.png")[0]
    # maintype, subtype = mime_type.split("/")

    # email_message.add_attachment(content, maintype=maintype, subtype=subtype)


    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()


if __name__ == "__main__":
    send_email(image_path="images/1.png")
