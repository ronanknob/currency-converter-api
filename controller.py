import http_handler
import data_parser


def handle_post(content):
    if not content:
        return "Requests needs a valid body to proceed", 400
    
    if not data_parser.validate_input(content):
        return "Request input data is not valid", 400

    if not http_handler.validate_currency(content):
        return "One or more currencies informed not exist or cant be converted by the source", 404
    
    converted_value = http_handler.convert_currency(content)
    if not converted_value:
        return "An error occoured in the currency conversion", 500
    return converted_value