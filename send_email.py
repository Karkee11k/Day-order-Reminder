"""
Module to send mail using Gmail SMTP server.

This module provides a class to send mail.

Classes:
	GMailer: Class to send mail using Gmail SMTP server.
"""

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from typing import List 


class GMailer:
	"""A class to send mail using Gmail SMTP server."""

	__server = "smtp.gmail.com"
	__port = 465
	__context = ssl.create_default_context()

	def __init__(self, mail_id: str, password: str) -> None:
		"""Initializes the GMailer with given mail id and password.
		
		Args:
			mail_id (str): The sender's email address.
			password (str): The sender's email password. 
		"""
		self.__from = mail_id
		self.__password = password

	
	def send(self, recipients: List[str], subject: str, message: str) -> None:
		"""Sends the mail to the given recipients.
		
		Args:
			recipients (list): List of recipients.
			subject (str): Subject of the mail.
			message (str): Content of the mail.
		"""
		email = MIMEMultipart()
		email['From'] = self.__from
		email['To'] = ', '.join(recipients)
		email['Subject'] = Header(subject, 'utf-8').encode()
		email_content = MIMEText(message, 'plain', 'utf-8')
		email.attach(email_content)

		with smtplib.SMTP_SSL(GMailer.__server, GMailer.__port, context=GMailer.__context) as server:
			server.login(self.__from, self.__password)
			server.sendmail(self.__from, recipients, email.as_string())