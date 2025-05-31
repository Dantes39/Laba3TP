class ForecastService:
    def forecast(self, df, n_years, window=5):
        df = df.sort_values('Year')
        infl = df['Inflation'].tolist()
        last_year = int(df['Year'].iloc[-1])
        forecast = []

        for i in range(n_years):
            if len(infl) >= window:
                next_val = sum(infl[-window:]) / window
            else:
                next_val = infl[-1]
            next_year = last_year + i + 1
            forecast.append({'Year': next_year, 'Inflation': next_val})
            infl.append(next_val)

        return pd.concat([df, pd.DataFrame(forecast)], ignore_index=True)
