from googleapiclient.discovery import build 

class GSheet: 
	"""Class to get data from public google sheets""" 
	
	def __init__(self, sheet_id, api_key): 
		"""Sets the spreadsheet id, API key and builds the service"""
		self.__spreadsheetId = sheet_id
		self.__service = build('sheets', 'v4', developerKey=api_key)  
		
	def fetch(self, sheet_range): 
		"""Returns the list of sheet's data in the specified range"""
		sheet = self.__service.spreadsheets()
		result = (sheet.values().get(spreadsheetId=self.
		__spreadsheetId, range=sheet_range).execute())
		return result.get("values", [])

      
