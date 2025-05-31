import pandas as pd

class PopulationAnalyzer:
    def __init__(self, df):
        self.df = df

    def max_growth_decline(self):
        # Ensure DataFrame is sorted by Year
        df_sorted = self.df.sort_values('Year')
        # Calculate yearly percentage change
        yearly_change = df_sorted['Population'].pct_change().dropna() * 100  # Convert to percentage

        if yearly_change.empty:
            max_growth = (df_sorted['Year'].iloc[0], 0.0)
            max_decline = (df_sorted['Year'].iloc[0], 0.0)
        else:
            max_growth_idx = yearly_change.idxmax()
            max_decline_idx = yearly_change.idxmin()

            max_growth = (df_sorted.loc[max_growth_idx, 'Year'], yearly_change[max_growth_idx])
            max_decline = (df_sorted.loc[max_decline_idx, 'Year'], yearly_change[max_decline_idx])

        return max_growth, max_decline