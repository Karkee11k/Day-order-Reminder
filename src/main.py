import os
from datetime import date 
from dotenv import load_dotenv

from gsheets import GSheet 
from send_email import GMailer


"""loading environment variables"""
load_dotenv() 
ME = os.getenv('ME')         
SHEET_ID = os.getenv('SHEET_ID') 
API_KEY = os.getenv('API_KEY') 
MAIL_ID = os.getenv('MAIL_ID') 
PASSWORD = os.getenv('PASSWORD')


def get_day_order(date, calendar): 
    """Gives the day order, if date is a working day, else None"""
    for row in calendar: 
        if row[0] != date: 
            continue 
        return row[2] if 'y' in row[1] else None
        
		

def make_message(day_order, periods, staffs): 
    """Makes a message with the periods""" 
    message = f'Day {day_order} order:\n' 
    suffices = ['st', 'nd', 'rd', 'th']	
	
    for i in range(5):
        suffix = suffices[min(i, 3)]
        message += f'\t{str(i+1)}{suffix} period - {periods[i]} by {staffs[i]}\n' 
    return message	
		
		
def main(me=[ME]):
    """Gets today date and sends the appropriate day order and periods to 
	the mail id"""
    today = date.today().strftime('%d/%m/%Y')     # today date 
    sheet = GSheet(SHEET_ID, API_KEY)             # sheet object to read data 
    mailer = GMailer(MAIL_ID, PASSWORD)           # Gmailer object to send mail
    calendar = sheet.fetch('AGAC Calendar')       # College calendar 
	
    # if calendar is empty, sends an info and terminates the program
    if not calendar:  
        mailer.send(me, 'info', 'no data found') 
        return  
	
    day_order = get_day_order(today, calendar)    # today day order

    # if day order is none, sends an info and terminates the program
    if not day_order: 
        mailer.send(me, 'info', 'might be a holiday')
        return 
	 		
    _range = f'Periods!A{day_order}:E{day_order}' # periods range for the day order
    periods = sheet.fetch(_range)[0]              # classes for the day order
    _range = f'Staffs!A{day_order}:E{day_order}'  # staffs range for the day order 
    staffs = sheet.fetch(_range)[0]               # staffs for the day order
    _range = 'Mail ID!A1:A1'                      # range for the mail id
    mail_id = sheet.fetch(_range)                 # Student's mail id
		
    # if any of them is empty, sends an info and terminates the program
    if not periods or not mail_id or not staffs:
        mailer.send(me, 'info', 'no data found')
        return 
    
    recipient = [id[0] for id in mail_id]
    subject = f'Today Day Order {today}'
    message = make_message(day_order, periods, staffs) 	
    print(message)	
    mailer.send(recipient, subject, message)      # mail sent	    


if __name__ == '__main__':
    try:
        main() 
    except Exception as e: 
        print(e)
	    
	    	    
	    	    	   	    
	    	    	   		
		
		
		
