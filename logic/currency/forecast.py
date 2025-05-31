import pandas as pd

class ForecastCurrency:
    def forecast(self, df, period, window_size=5):
        df_result = df.copy()
        result_rows = []

        currencies = [col for col in df.columns if col not in ['Date']]
        last_date = pd.to_datetime(df['Date'].max())

        # Ensure the input DataFrame is sorted by date
        df_result = df_result.sort_values('Date')

        for currency in currencies:
            currency_data = df_result[df_result[currency].notna()]
            values = currency_data[currency].tolist()

            for i in range(period):
                if len(values) >= window_size:
                    next_val = sum(values[-window_size:]) / window_size
                else:
                    next_val = values[-1]

                new_date = (last_date + pd.Timedelta(days=i + 1)).strftime('%Y-%m-%d')
                result_rows.append({'Date': new_date, currency: next_val})
                values.append(next_val)

        # Combine original and forecast data
        df_forecast = pd.concat([df_result, pd.DataFrame(result_rows)], ignore_index=True)
        # Ensure dates are in string format and sorted
        df_forecast['Date'] = pd.to_datetime(df_forecast['Date']).dt.strftime('%Y-%m-%d')
        df_forecast = df_forecast.sort_values('Date').reset_index(drop=True)
        return df_forecast