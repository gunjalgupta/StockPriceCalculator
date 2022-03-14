from flask import Flask
from flask import render_template
from flask import request
import requests
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        #Taking input symbol from user
        symbol = request.form['symbol'].upper()

        # Make API CALL with the symbol
        #Used fpm cloud api to fetch data
        datum = requests.get('https://fmpcloud.io/api/v3/quote/'+symbol+'?apikey=7eacbf4424fba9a4ec4952e6584e0ee6')
        result_data = json.loads(datum.text)
        #print(data)

        #Error message for incorrect symbol by checking length of data returned from api
        if len(result_data) < 1:
            ResData = {'msg' : "No such stock symbol found! Sorry :( Please enter correct symbol!"}
            return render_template('index.html', **ResData)
        else:
            dateTimeNow = datetime.now()
            NameofStock = result_data[0]["name"]
            price = result_data[0]["price"]
            valueChange = result_data[0]["change"]
            perChange = result_data[0]["changesPercentage"]
            ResData = {'dateTimeNow': dateTimeNow, 'NameofStock': NameofStock, 'price': price, 'valueChange' : valueChange, 'perChange': perChange }
            return render_template('output.html', **ResData)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=3000)
