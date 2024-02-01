import os
from datetime import date 
from dotenv import load_dotenv

from gsheets import GSheet 
from send_email import GMailer

"""loading environment variables"""
load_dotenv() 

SHEET_ID = os.getenv('SHEET_ID') 
API_KEY = os.getenv('API_KEY') 
MAIL_ID = os.getenv('MAIL_ID') 
PASSWORD = os.getenv('PASSWORD')
ME = os.getenv('ME')


def get_day_order(date, calendar): 
    """Gives the day order, if date is a working day, else None"""
    for row in calendar: 
	if row[0] != date: 
	    continue 
	return row[2] if 'y' in row[1] else None
		

def make_message(day_order, periods): 
    """Makes a message with the periods""" 
    message = f'Day {day_order} order:\n' 
    suffices = ['st', 'nd', 'rd', 'th']	
    
    for i in range(5):
    	suffix = suffices[min(i, 3)]
    	message += f'\t{str(i+1)}{suffix} period - {periods[i]}\n' 
    return message	
		
		
def main(me=[ME]):
    """Gets today date and sends the appropriate day order and periods to the mail id"""
    today = date.today().strftime('%d/%m/%Y')
    sheet = GSheet(SHEET_ID, API_KEY) 
    mailer = GMailer(MAIL_ID, PASSWORD)
    calendar = sheet.fetch('AGAC Calendar') 
	
    if not calendar:  
        mailer.send(me, 'info', 'no data found') 
	return  
	
    day_order = get_day_order(today, calendar)		
    if not day_order: 
	mailer.send(me, 'info', 'might be a holiday')
	return 
			
    _range = f'Periods!A{day_order}:E{day_order}'
    periods = sheet.fetch(_range)[0]
    _range = 'Mail ID!A:A'
    mail_id = sheet.fetch(_range) 
		
    if not periods or not mail_id:
        mailer.send(me, 'info', 'no data found') 
	return 
    
    recipient = [id[0] for id in mail_id]
    subject = f'Today Day Order {today}'
    message = make_message(day_order, periods)		
    mailer.send(recipient, subject, message) 	    


if __name__ == '__main__':
    try: 
	main() 
    except Exception as e: 
	print(e)
	    
	    	    
	    	    	   	    
	    	    	   		
		
		
		
