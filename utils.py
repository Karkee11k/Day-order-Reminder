"""
Provides some utility funtions.

This module has functions to getting day order and to generating a message
with periods and staffs.

Functions:
    - get_day_order(date, calendar):
        Returns the day order if the date is a working day, otherwise None.
    
    - make_message(day_order, periods, staffs):
        Constructs a message with the periods and corresponding staffs for 
        the given day order.
"""

from typing import List, Union


def get_day_order(date: str, calendar: List[List[str]]) -> Union[str, None]: 
    """Returns the day order from the calendar for the given date, if
    it's a working day.

    Examples:
        >>> calendar = [['03/03/2024', 'y', '2'], ['04/03/2024', 'n', None]]
        >>> get_day_order('03/03/2024', calendar)
        2
        >>> get_dat_order('04/03/2024', calendar)
        None
    
    Args:
        date (str): The date for which the day order is requested.
        calendar (list): List of lists representing the calendar, where
        each sub list contains date, working day indicator and day order.

    Returns:
        str or None: The day order if the given date is a working day;
        otherwise, None.
    """
    for row in calendar: 
        if row[0] != date: 
            continue 
        return row[2] if 'y' in row[1] else None
    

def make_message(day_order: str, periods: List[str], staffs: List[str]) -> str: 
    """Creates and returns a message with the periods and the staffs.
    
    Examples:
        >>> make_message(3, ['DSA', 'Java'], ['KK', 'YY'])
        Day 3 order:
            1st period - DSA by KK
            2nd period - Java by YY

    Args:
        day_order (str): The day order.
        periods (list): The classes for the day order.
        staffs (list): The staffs for the classes.
    
    Returns:
        str: A message with day order, classes and the staffs.
    """ 
    message = f'Day {day_order} order:\n' 
    suffices = ['st', 'nd', 'rd', 'th']	
	
    for i in range(len(periods)):
        suffix = suffices[min(i, 3)]
        message += f'\t{str(i+1)}{suffix} period - {periods[i]} by {staffs[i]}\n' 
    return message	