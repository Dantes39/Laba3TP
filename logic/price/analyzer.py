class InflationAnalyzer:
    def __init__(self, df):
        self.df = df

    def max_gain_loss(self):
        df_sorted = self.df.sort_values('Year')
        change = df_sorted['Inflation'].diff().dropna()

        max_gain_year = df_sorted.iloc[change.idxmax()]['Year']
        max_loss_year = df_sorted.iloc[change.idxmin()]['Year']

        return {
            'max_gain': (max_gain_year, change.max()),
            'max_loss': (max_loss_year, change.min())
        }
