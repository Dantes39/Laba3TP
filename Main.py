from logic.currency.analyzer import CurrencyAnalyzer
from logic.currency.forecast import ForecastService
from logic.currency.plotter import CurrencyPlotter
from flask import Flask, render_template, request
import pandas as pd
from logic.price.analyzer import InflationAnalyzer
from logic.price.forecast import ForecastServicePrice
from logic.price.plotter import InflationPlotter

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    chart_url = None
    result = None
    table_data = None

    if request.method == 'POST':
        file = request.files['datafile']
        period = int(request.form['period'])
        df = pd.read_csv(file, encoding='cp1251')

        analyzer = CurrencyAnalyzer(df)
        max_gain, max_loss = analyzer.max_gain_loss()

        currencies = [col for col in df.columns if col not in ['Date']]
        result = {
            'max_gain': {},
            'max_loss': {}
        }
        for currency in currencies:
            result['max_gain'][currency] = (max_gain[currency][0], round(max_gain[currency][1], 2))
            result['max_loss'][currency] = (max_loss[currency][0], round(max_loss[currency][1], 2))

        forecast = ForecastService()
        df_forecast = forecast.forecast(df, period)
        original_dates = df['Date'].unique().tolist()
        plotter = CurrencyPlotter()
        chart_url = plotter.plot(df_forecast, original_dates)

        table_data = df.to_dict(orient='records')

    return render_template('currency.html', chart_url=chart_url, result=result, table_data=table_data)


@app.route('/price', methods=['GET', 'POST'])
def price():
    result, chart_url, table_data, future_price = None, None, None, None

    if request.method == 'POST':
        file = request.files['datafile']
        years_to_forecast = int(request.form['period'])
        current_price = float(request.form['price'])

        df = pd.read_csv(file)
        df['Year'] = df['Year'].astype(int)

        analyzer = InflationAnalyzer(df)
        result = analyzer.max_gain_loss()

        forecaster = ForecastServicePrice()
        df_forecast = forecaster.forecast(df, years_to_forecast)

        original_years = df['Year'].tolist()
        plotter = InflationPlotter()
        chart_url = plotter.plot(df_forecast, original_years)

        # Расчёт будущей стоимости
        forecasted = df_forecast[df_forecast['Year'] > max(original_years)]
        inflation_factors = [(1 + (inf / 100)) for inf in forecasted['Inflation']]
        cumulative_multiplier = 1
        for f in inflation_factors:
            cumulative_multiplier *= f
        future_price = round(current_price * cumulative_multiplier, 2)

        table_data = df_forecast[df_forecast['Year'].isin(original_years)].to_dict(orient='records')

    return render_template('price.html',
                           chart_url=chart_url,
                           result=result,
                           table_data=table_data,
                           future_price=future_price)

@app.route('/population')
def populationStart():
    return render_template('population.html')

if __name__ == '__main__':
    app.run(debug=True, port=5555)