# Currency converter App

The idea in this exercise was to create a simple API using Flask. This API only receives POST requests in the /currency_converter route, and must contain an object of the following format:

```json
{
    "origin_currency": "USD",
    "destination_currency": "BRL",
    "value": 100.00
}
```
Where:
* origin_currency: Abbreviation of the origin currency (ex: USD)
* destination_currency: Abbreviation of desired currency after conversion (ex: BRL)
* value: value to be converted, with up to two decimal places (ex: 100.00)

A response object will be only a value, like this:
```json
"492.00"
```

## How to execute (Linux/Mac-based commands):
* Make sure you have [Python 3+](https://www.python.org/downloads/) installed and pip package manager;
* Set the prompt inside this directory;
* Install the requirements with the command:
```bash
python3 -m pip install -r requirements.txt
```
* Run the application with the following command:
```bash
FLASK_APP=main.py flask run
```
* Make a post request to localhost:5000 with cURL or other client (like Postman), like this:
```bash
curl -XPOST -H "Content-type: application/json" -d '{"origin_currency": "USD", "destination_currency": "BRL", "value": 100.00}' '127.0.0.1:5000/currency_convert'
```
## Tests
This project relies on tests. They cover the unit parts of the data_parser.py file and the last test covers all the flow end-to-end. To run the tests, execute the command:
```bash
python3 tests.py
```

## Execution flow steps (overview)
* Receive input
* Analyze if the input is valid
     * Check if the data types entered are correct
     * Get the list of countries available in BCB for conversion and compare the two currencies received in the input
* Request conversion to BCB API
     * Request the date of the last available quote
     * Request conversion of values
* Inform result in route

## Technology stack - decisions
* The application is developed in Python language, with the help of the Flask Framework, as it has good documentation and is easy to use.
* Analyzing the source structure I noticed that requests are made to BCB API via GET methods. As there are few flow controls, I used the library [requests](https://docs.python-requests.org/en/master/) to make the requests flow, but most feature-rich frameworks, like scrappy can be more useful to scrap data from the web.
* Input validation was done through [jsonschema](https://json-schema.org/), where the expected input was parameterized and the received data was validated based on this schema parameters.
* The handling of the data received from the requests was done with the library [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), popular web data scraping tool.
* During execution, the pattern [return Early](https://medium.com/swlh/return-early-pattern-3d18a41bba8) is used, in which validations are always done before to avoid errors and unnecessary processing.


## Classes objectives
* main.py -> Start the Flask server, and start routes for receiving data. As a POST is made to /currency_convert, it sends to the controller class.
* controller.py -> Responsible for handle the requests from main and communicate with other modules. Communicate with http_handler and data_parser modules to make simple data validations and request the parsed data.
* http_handler.py -> Control Web requests when its needed, get data from source and requests data_parser module to parse the response data to send to the controller.
* data_parser -> responsible for raw data manipulation. Make validations with data, parse the web documents into structured data. Also, query model.py to do schema validation
* model.py -> store the schemas to be used in schema validations.