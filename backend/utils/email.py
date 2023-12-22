# -*- coding: utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Environment, PackageLoader, select_autoescape

from ..config import config


def send_email(to, subject, template_file, **kwargs):
    if not all([config.MAIL_SERVER, config.MAIL_USERNAME, config.MAIL_PASSWORD]):
        return

    env = Environment(
        loader=PackageLoader("backend"),
        autoescape=select_autoescape(["html", "xml"]),
    )

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = config.MAIL_FROM
    msg["To"] = to
    template = env.get_template(template_file)
    msg.attach(MIMEText(template.render(**kwargs), "html"))

    with smtplib.SMTP(config.MAIL_SERVER, config.MAIL_PORT) as smtp:
        # smtp.set_debuglevel(True)
        smtp.ehlo()  # send the extended hello to our server
        if config.MAIL_STARTTLS:
            smtp.starttls()  # tell server we want to communicate with TLS encryption
            smtp.ehlo()  # send the extended hello to our server
        smtp.esmtp_features["auth"] = "LOGIN PLAIN"
        smtp.login(config.MAIL_USERNAME, config.MAIL_PASSWORD)
        smtp.send_message(msg)
        smtp.quit()
