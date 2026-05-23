from flask import Flask, render_template, request
from stock_data import get_stock_data, create_chart

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    data    = None
    chart   = None
    symbol  = ''

    if request.method == 'POST':
        symbol = request.form.get('symbol', '').strip().upper()

        # Block empty or too-long inputs
        if not symbol:
            data = {'error': 'Please enter a stock symbol.'}
        elif len(symbol) > 20:
            data = {'error': 'Symbol too long. Please enter a valid stock symbol like TCS.NS or AAPL.'}
        elif not symbol.replace('.', '').replace('-', '').isalnum():
            data = {'error': 'Invalid symbol. Only letters, numbers, dots and hyphens are allowed.'}
        else:
            data = get_stock_data(symbol)
            if data['error'] is None:
                chart = create_chart(data['history'], symbol)

    return render_template('index.html', data=data, chart=chart, symbol=symbol)


@app.errorhandler(404)
def not_found(e):
    return render_template('index.html', data=None, chart=None, symbol=''), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('index.html',
        data={'error': 'Server error. Please try again in a moment.'},
        chart=None, symbol=''), 500


if __name__ == '__main__':
    app.run(debug=True)



    

    