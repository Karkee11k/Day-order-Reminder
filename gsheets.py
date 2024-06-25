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
	"""A class to read public Google Sheets using Google Sheets API."""

	def __init__(self, sheet_id: str, api_key: str) -> None:
		"""Initializes the GSheet with spreadsheet ID and API key.
		
		Args:
			sheet_id (str): The spreadsheet ID.
			api_key (str): The API key used to authenticate with Google Sheets API.
		"""
		self.__sheet_id = sheet_id
		self.__service = build('sheets', 'v4', developerKey=api_key)

	
	def fetch(self, sheet_range: str) -> List[List[str]]:
		"""Returns the sheet's data in the given range.
		
		Args:
			sheet_range (str): The range of cells to retrieve date.

		Returns:
			list: List of data in the given range.
		"""
		sheet = self.__service.spreadsheets()
		result = sheet.values().get(spreadsheetId=self.__sheet_id, range=sheet_range).execute()
		return result.get('values', [])