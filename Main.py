from logic.currency.analyzer import CurrencyAnalyzer
from logic.currency.forecast import ForecastCurrency
from logic.currency.plotter import CurrencyPlotter
from flask import Flask, render_template, request
import pandas as pd
from logic.population.analyzer import PopulationAnalyzer
from logic.population.forecast import ForecastService
from logic.population.plotter import PopulationPlotter
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

        forecast = ForecastCurrency()
        df_forecast = forecast.forecast(df, period)
        original_dates = df['Date'].unique().tolist()
        plotter = CurrencyPlotter()
        chart_url = plotter.plot(df_forecast, original_dates)

        table_data = df.to_dict(orient='records')

    return render_template('currency.html', chart_url=chart_url, result=result, table_data=table_data)

@app.route('/price')
def priceStart():
    return render_template('price.html')

@app.route('/population', methods=['GET', 'POST'])
def populationStart():
    chart_url = None
    result = None
    table_data = None

    if request.method == 'POST':
        file = request.files['datafile']
        period = int(request.form['period'])
        df = pd.read_excel(file, sheet_name='Лист1')

        analyzer = PopulationAnalyzer(df)
        max_growth, max_decline = analyzer.max_growth_decline()

        result = {
            'max_growth': (max_growth[0], round(max_growth[1], 2)),
            'max_decline': (max_decline[0], round(max_decline[1], 2))
        }

        forecast = ForecastService()
        df_forecast = forecast.forecast(df, period)
        original_years = df['Year'].unique().tolist()
        plotter = PopulationPlotter()
        chart_url = plotter.plot(df_forecast, original_years)

        table_data = df.to_dict(orient='records')

    return render_template('population.html', chart_url=chart_url, result=result, table_data=table_data)


if __name__ == '__main__':
    app.run(debug=True, port=5555)