import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Smtp:
    def __init__(self, host, port, sender, password):
        self._host = host
        self._port = port
        self._sender = sender
        self._password = password

    def validate(self):
        """Validate smtp connection"""
        try:
            with smtplib.SMTP_SSL(self._host, self._port) as server:
                server.login(self._sender, self._password)
            return True, None
        except Exception as e:
            return False, e

    def send_email(self, recipient, subject, body, attach=None):
        """Send email"""
        # create message
        message = MIMEMultipart()
        message["From"] = self._sender
        message["To"] = recipient
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # attach file
        if attach is not None:
            with open(attach, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {os.path.basename(attach)}",
            )
            message.attach(part)

        # send email
        with smtplib.SMTP_SSL(self._host, self._port) as server:
            server.login(self._sender, self._password)
            server.sendmail(self._sender, recipient, message.as_string())
