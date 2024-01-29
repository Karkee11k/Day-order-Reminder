from datetime import date 
from dotenv import dotenv_values
from gsheets import GSheet 
from send_email import GMailer

		
def main(me=['keyan9329@gmail.com']):
	today = date.today().strftime('%d/%m/%Y') 
	config = dotenv_values('.env') 
	sheet = GSheet(config['SHEET_ID'], config['API_KEY']) 
	mailer = GMailer(config['MAIL_ID'], config['PASSWORD'])
	calendar = sheet.fetch('AGAC Calendar') 
	day_order = None
	
	if calendar == None or len(calendar) == 0:  
		mailer.send(me, 'info', 'no data found') 
		return  
	
	for row in calendar: 
		if row[0] != today: 
			continue 
		if 'y' in row[1]: 
			day_order = row[2] 
		break   
		
	if not day_order: 
		mailer.send(me, 'info', 'might be a holiday')
		return 
			
	_range = f'Periods!A{day_order}:E{day_order}'
	periods = sheet.fetch(_range)[0]
	_range = 'Mail ID!A:A'
	mail_id = sheet.fetch(_range) 
		
	if mail_id == periods or not len(periods)*len(mail_id):
		 mailer.send(me, 'info', 'no data found') 
		 return 
    
	recipient = [id[0] for id in mail_id]
	subject = f'Today Day Order {today}'
	message = f'Day {day_order} order:\n' 
	suffices = ['st', 'nd', 'th']
		
	for i in range(5):
		suffix = suffices[min(i, 2)]
		message += f'\t{str(i+1)}{suffix} period - {periods[i]}\n'
			
	mailer.send(recipient, subject, message) 
	    


if __name__ == '__main__':
	try: 
		main() 
	except Exception as e: 
		print(e)
	    
	    	    
	    	    	   	    
	    	    	   		
		
		
		
