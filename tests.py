import unittest

import data_parser
import controller

class Exercicio1TestSuite(unittest.TestCase):

    def open_reference_file(self, filename):
        in_file = open(f"./reference_files/{filename}", "rb")
        data = in_file.read()
        in_file.close()
        
        return data

    def test_should_validate_input_correctly(self):
        # A origin_currency or destination currency with more than 3 characters
        self.assertFalse(data_parser.validate_input(b'{"origin_currency": "USDE", "destination_currency": "BRL", "value": 100.00}'))
        # A value that is not a number
        self.assertFalse(data_parser.validate_input(b'{"origin_currency": "USDE", "destination_currency": "BRL", "value": "a"}'))
        # A currency that is not a string
        self.assertFalse(data_parser.validate_input(b'{"origin_currency": True, "destination_currency": "BRL", "value": 100.00}'))
        # Missing one field
        self.assertFalse(data_parser.validate_input(b'{"origin_currency": "USD", "value": 100.00}'))
        # A valid input
        self.assertTrue((data_parser.validate_input(b'{"origin_currency": "USD", "destination_currency": "BRL", "value": 100.00}')))
    
    def test_should_parse_currencies_list_correctly(self):
        data = self.open_reference_file("currencies_list.xml")
        currencies = data_parser.parse_currencies(data)
        self.assertEqual('790', currencies["BRL"])
    
    def test_should_parse_quote_date_correcly(self):
        data = self.open_reference_file("quote_date.xml")
        quote_date = data_parser.parse_last_quote_date(data)
        self.assertEqual('2021-06-25', quote_date)
    
    def test_should_get_input_value_correctly(self):
        self.assertEqual('25.50', data_parser.get_input_value(b'{"value":"25.50"}'))
    
    def test_should_get_converted_value_correctly(self):
        data = self.open_reference_file("converted_value.xml")
        converted_value = data_parser.parse_converted_currency(data)
        self.assertEqual(('492.0000000', 200), converted_value)
    
    # Test the whole flow and verify if 100 USD converted in BRL is a value greater than 300
    def test_should_get_value_correctly(self):
        value_converted = controller.handle_post(b'{"origin_currency": "USD", "destination_currency": "BRL", "value": 100.00}')
        self.assertGreater(float(value_converted[0]), 300)
    
if __name__ == '__main__':
    unittest.main()