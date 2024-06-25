"""
Main Program: Daily Day Order and the Scheduled Classes Reminder.

A python script for managing workday schedules and sending emails with
the day order, periods and staffs.

Environment Variables:
    ME (str): Admin's or Developer's email address.
    SHEET_ID (str): Google Sheets ID.
    API_KEY (str): Google Sheets API key.
    MAIL_ID (str): Sender's email address.
    PASSWORD (str): Sender's email password.

Functions:
    - main():
        Gets today date and sends the appropriate day order, periods and
        staffs to the specified email ID(s).
"""

import os
from datetime import date 
from dotenv import load_dotenv

from gsheets import GSheet 
from send_email import GMailer
from utils import get_day_order, make_message


"""Load environment variables"""
load_dotenv() 
ME = [os.getenv('ME')]         
SHEET_ID = os.getenv('SHEET_ID') 
API_KEY = os.getenv('API_KEY') 
MAIL_ID = os.getenv('MAIL_ID') 
PASSWORD = os.getenv('PASSWORD')


def main() -> None:
    """Gets today date, retrieves day order, periods and staff, then 
    sends the appropriate information to the recipients."""
    
    today = date.today().strftime('%d/%m/%Y')     # today date 
    sheet = GSheet(SHEET_ID, API_KEY)             # sheet object to read data 
    mailer = GMailer(MAIL_ID, PASSWORD)           # Gmailer object to send mail
    calendar = sheet.fetch('AGAC Calendar')       # College calendar 
	
    # if calendar is empty, sends an info and terminates the program
    if not calendar:  
        mailer.send(ME, 'info', 'no data found') 
        return
	
    day_order = get_day_order(today, calendar)    # today day order

    # if day order is none, sends an info and terminates the program
    if not day_order: 
        mailer.send(ME, 'info', 'might be a holiday')
        return 
	 		
    _range = f'Periods!A{day_order}:E{day_order}' # periods range for the day order
    periods = sheet.fetch(_range)[0]              # classes for the day order
    _range = f'Staffs!A{day_order}:E{day_order}'  # staffs range for the day order 
    staffs = sheet.fetch(_range)[0]               # staffs for the day order
    _range = 'Mail ID!A:A'                      # range for the mail id
    mail_id = sheet.fetch(_range)                 # Student's mail id
		
    # if any of them is empty, sends an info and terminates the program
    if not periods or not mail_id or not staffs:
        mailer.send(ME, 'info', 'no data found')
        return 
    
    recipient = [id[0] for id in mail_id]
    subject = f'Today Day Order {today}'
    message = make_message(day_order, periods, staffs) 	
    mailer.send(recipient, subject, message)      # mail sent	


if __name__ == '__main__':
    try:
        main() 
    except Exception as e: 
        print(f'Error: {e}')