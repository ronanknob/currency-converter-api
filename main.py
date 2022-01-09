from flask import Flask, request

import controller

app = Flask(__name__)

@app.route('/currency_convert', methods=['POST'])
def convertCurrencies():
    return controller.handle_post(request.data)