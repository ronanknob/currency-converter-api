import data_parser

import requests
from datetime import date

def validate_currency(content):
    valid_currencies = get_valid_currencies()
    if not valid_currencies:
        return False
    
    current_currencies = data_parser.parse_content_currencies(content)
    return data_parser.validate_currencies(current_currencies, valid_currencies)


'''
Get the currencies list from the Banco Central website and return 
a Key/Value list with the acronyms and system values of each item
'''
def get_valid_currencies():
    try:
        data = requests.get('https://www3.bcb.gov.br/bc_moeda/rest/moeda/data')
        return data_parser.parse_currencies(data.content)
    except:
        return False


def convert_currency(content):
    # get the last cotation date
    last_quote_date = get_latest_quote_date()
    if not last_quote_date:
        print('Error getting last quote date')
        return False

    # Get the input data, converting the acronyms to correspondent codes and getting the value
    current_currencies_codes = get_current_currencies_codes(content)
    value = data_parser.get_input_value(content)
    if not all([current_currencies_codes, value]):
        print('Error getting currencies codes or value to conversion')
        return False

    # Convert value
    return request_conversion(last_quote_date, current_currencies_codes, value)


'''
The last quote date is needed for do the conversion. Generally is the last business day.
The curency 220 (USD DOLAR) is used by example, seems to work the same date with all currencies.
'''
def get_latest_quote_date():
    actual_date = date.today().strftime("%Y-%m-%d")
    try:
        data = requests.get(f'https://www3.bcb.gov.br/bc_moeda/rest/cotacao/fechamento/ultima/1/220/{actual_date}')
        return data_parser.parse_last_quote_date(data.content)
    except:
        return False

'''
With the currencies informed on input, get the correspondent codes do make the convert request in BC API.
'''
def get_current_currencies_codes(content):
    # I've already validated the data before, so i don't do this here.
    current_currencies = data_parser.parse_content_currencies(content)
    valid_currencies = get_valid_currencies()
    if not all([current_currencies, valid_currencies]):
        return False

    return data_parser.parse_currency_codes(current_currencies, valid_currencies)


def request_conversion(last_quote_date, current_currencies, value):
    if not all([last_quote_date, current_currencies, value]):
        return False
    try:
        url = f"https://www3.bcb.gov.br/bc_moeda/rest/converter/{value}/1/{current_currencies[0]}/{current_currencies[1]}/{last_quote_date}"
        print(f'Requesting follow conversion: {url}')
        data = requests.get(url)
        return data_parser.parse_converted_currency(data.content)
    except:
        return False