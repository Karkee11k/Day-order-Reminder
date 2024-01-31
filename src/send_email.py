import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header 

class GMailer: 
	"""class to send mail""" 
	
	def __init__(self, mail_id, password): 
		"""Sets the mail id and the password"""
		self.__from = mail_id 
		self.__password = password
		
	def send(self, recipients, subject, message): 
		"""sends the message to the given recipients"""
		email = MIMEMultipart()
		email['From'] = self.__from
		email['To'] = ', '.join(recipients)
		email['Subject'] = Header(subject, 'utf-8').encode()
		email_content = MIMEText(message, 'plain', 'utf-8')
		email.attach(email_content)
		
		context = ssl.create_default_context()
		with smtplib.SMTP_SSL("smtp.gmail.com", 465,       
		context=context) as server:
		  		server.login(self.__from, self.__password) 
		  		server.sendmail(self.__from, recipients, email.
		  		as_string())  
		  		

    		