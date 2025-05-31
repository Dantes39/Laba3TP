import pandas as pd

class ForecastService:
    def forecast(self, df, period, window_size=5):
        df_result = df.copy()
        result_rows = []

        # Ensure the input DataFrame is sorted by year
        df_result = df_result.sort_values('Year')

        last_year = df_result['Year'].max()
        population_data = df_result[df_result['Population'].notna()]
        values = population_data['Population'].tolist()

        for i in range(period):
            if len(values) >= window_size:
                next_val = sum(values[-window_size:]) / window_size
            else:
                next_val = values[-1]

            new_year = last_year + i + 1
            result_rows.append({'Year': new_year, 'Population': next_val})
            values.append(next_val)

        # Combine original and forecast data
        df_forecast = pd.concat([df_result, pd.DataFrame(result_rows)], ignore_index=True)
        # Ensure years are in integer format and sorted
        df_forecast['Year'] = df_forecast['Year'].astype(int)
        df_forecast = df_forecast.sort_values('Year').reset_index(drop=True)
        return df_forecast