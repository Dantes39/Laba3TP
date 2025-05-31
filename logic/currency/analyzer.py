class CurrencyAnalyzer:
    def __init__(self, df):
        self.df = df

    def max_gain_loss(self):
        currencies = [col for col in self.df.columns if col not in ['Date']]
        max_gain = {}
        max_loss = {}

        for currency in currencies:
            df_sorted = self.df.sort_values('Date')
            daily_change = df_sorted[currency].diff().dropna()

            if daily_change.empty:
                max_gain[currency] = (df_sorted['Date'].iloc[0], 0.0)
                max_loss[currency] = (df_sorted['Date'].iloc[0], 0.0)
            else:
                max_gain_idx = daily_change.idxmax()
                max_loss_idx = daily_change.idxmin()

                max_gain[currency] = (df_sorted.loc[max_gain_idx, 'Date'], daily_change[max_gain_idx])
                max_loss[currency] = (df_sorted.loc[max_loss_idx, 'Date'], daily_change[max_loss_idx])

        return max_gain, max_loss