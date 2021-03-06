import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def get_files_in_current_directory():
    """Returns a list of filenames in the current directory."""
    path = '.'
    files = os.listdir(path)
    return files

files = get_files_in_current_directory()

class Email:
    default_message = "This is an important message. Please take a look at the file. If there are any errors, please reply back."
    
    def __init__(self, from_address, to_address):
        self.from_address = from_address
        self.to_address = to_address

        self.msg = MIMEMultipart()
        self.msg['From'] = from_address
        self.msg['To'] = to_address

    def set_subject(self, file_data):
        self.msg['Subject'] = "Load sheet " + file_date

    def set_default_message(self):
        html = f"<html><head></head><body><p>{self.default_message}</p></body></html>"
        self.msg.attach(MIMEText(html, 'html'))

    def attach_file(self, path):
        part = MIMEBase('application', "octet-stream") 
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition', 'attachment; filename="{}"'.format(
                os.path.basename(path)
            )
        )
        self.msg.attach(part)

    def get_as_string(self):
        return self.msg.to_string()

def set_from_email():
    return input("Your Email: ")

def set_password():
    return input("Password: ")

from_address = set_from_email()
password = set_password()

server = smtplib.SMTP('smtp.outlook.com', 587) #10 used to be 587, idk what the 587 is for
server.ehlo()
server.starttls()
server.ehlo()
server.login(from_address, password)

def get_email_metadata_from_path(path):
    split_path = path.split('_')
    local_part = split_path[0]
    file_date = split_path[1]
    to_address = local_part + "@spu.edu"
    print("attempting to send email to " + to_address) # Python will assume this is a str
    return to_address, file_date
    # This will need more cleaning up, but it works for now. 

for path in files:
    to_address, file_date = get_email_metadata_from_path(path)
    email = Email(from_address, to_address)
    email.set_subject(file_date)
    email.set_default_message()
    email.attach_file(path)
    print("sending email to " + to_address)
    text = email.get_as_string()
    server.sendmail(from_address, email.to_address, text)
    print("sent email to " + to_address)


# You are verifying that these are email addresses?
# We can look at including this in tests later.

server.quit()

    
