import jsonschema
import json
import re

from bs4 import BeautifulSoup
from jsonschema import validate

import model
'''
Check if the input is valid using jsonschema validation based on a json expected model.
Tip: If you want to see jsonschema output for each error you can put a print(err) above except line.
'''
def validate_input(content):
    json_content = get_json_content(content)
    print(json_content)
    if not json_content:
        return False
    try:
        validate(instance=json_content, schema=model.input_schema)
        return True
    except jsonschema.exceptions.ValidationError as err:
        return False

'''
Transform bytes in json when its possible
'''
def get_json_content(data):
    try:
        return json.loads(data)
    except:
        return False

'''
Transform raw data in BeautifulSoup object
'''
def get_soup(page):
    try:
        return BeautifulSoup(page, 'html.parser')
    except:
        return False

def parse_currencies(page):
    # Transform the response in a soup object
    soup = get_soup(page)
    if not soup:
        return False
    
    # Create the result dict to store the results
    result = {}

    # Create result list, wich contain the currency id and the system code
    currency_list = soup.find_all('moeda')
    for currency in currency_list:
        currency_code = currency.find('codigo')
        currency_name = currency.find('sigla')
        if all([currency_code, currency_name]):
            result[currency_name.text] = currency_code.text
    
    if not result:
        return False
    return result

def parse_content_currencies(content):
    json_content = get_json_content(content)
    if not json_content:
        return False
    return [json_content.get('origin_currency'),json_content.get('destination_currency')]

def parse_currency_codes(current_currencies, valid_currencies):
    codes = []
    for i in current_currencies:
        # valid_currencies is a key value list. If the key (ex. USD) is a match, add the code (ex. 5) to codes.
        for k,v in valid_currencies.items():
            if i == k:
                codes.append(v)
    
    # We expect validations for the origin and destination currencies
    # So the validations len must be equal 2 
    if codes and len(codes) == 2:
        return codes
    return False



'''
validate_currencies check if the currencies in the input data exist on the
currencies list received from the source, necessary to be converted.
'''
def validate_currencies(current_currencies, valid_currencies):
    validations = []
    for i in valid_currencies:
        if i in [i for i in current_currencies]:
            validations.append(True)
    
    # We expect validations for the origin and destination currencies
    # So the validations len must be equal 2 
    if validations and len(validations) == 2:
        return True
    return False

def parse_last_quote_date(page):
    match = re.search("<dataHoraCotacao>([0-9]{4}-[0-9]{2}-[0-9]{2})T", page.decode())
    if not match:
        return False
    
    return match.group(1)
        

def get_input_value(content):
    json_content = get_json_content(content)
    return json_content.get('value')

def parse_converted_currency(page):
    # Transform the response in a soup object
    soup = get_soup(page)
    if not soup:
        return False
    
    converted_value = soup.find('valor-convertido')
    if not converted_value:
        return False
    
    return converted_value.text, 200