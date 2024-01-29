from googleapiclient.discovery import build 

class GSheet: 
	def __init__(self, sheet_id, api_key): 
		self.__spreadsheetId = sheet_id
		self.__service = build('sheets', 'v4', developerKey=api_key)  
		
	def fetch(self, sheet_range):
		sheet = self.__service.spreadsheets()
		result = (sheet.values().get(spreadsheetId=self.__spreadsheetId, range=sheet_range).execute())
		return result.get("values", [])

      
