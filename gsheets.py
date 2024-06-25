"""
Module to interact with the public Google Sheets using Google Sheets API.

This module provides a class GSheet to fetch data from public Google Sheet.

Classes:
	GSheet: Class to interact with public Google Sheets using Google
	Sheets API.
"""

from googleapiclient.discovery import build 
from typing import List


class GSheet: 
	"""Class to read from public Google Sheets using Google Sheets API.""" 
	
	def __init__(self, sheet_id: str, api_key: str) -> None: 
		"""Initailizes the GSheet with the spreadsheet ID, API key and
		builds the service.
		
		Args:
			sheet_id (str): The ID of the Google Sheets spreadsheet.
			api_key (str): The API key used to authenticate with the
			Google Sheets API.
		"""
		self.__spreadsheetId = sheet_id
		self.__service = build('sheets', 'v4', developerKey=api_key)  


	def fetch(self, sheet_range: str) -> List[List[str]]: 
		"""Fetches and Returns the sheet's data in the specified range.
		
		Args:
			sheet_range (str): The range of cells to retrieve data from,
			e.g., 'Sheet!A1:B2'.

		Returns:
			list: The list of data from the specified range.
		"""
		sheet = self.__service.spreadsheets()
		result = sheet.values().get(spreadsheetId=self.__spreadsheetId, range=sheet_range).execute()	
		return result.get("values", [])