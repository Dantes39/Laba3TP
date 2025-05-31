import matplotlib.pyplot as plt
import os
import pandas as pd

plt.switch_backend('Agg')

class PopulationPlotter:
    def __init__(self, static_folder='static'):
        self.static_path = os.path.abspath(static_folder)
        os.makedirs(self.static_path, exist_ok=True)
        self.chart_filename = 'population_chart.png'

    def plot(self, df: pd.DataFrame, original_years: list[int]) -> str:
        fig, ax = plt.subplots(figsize=(10, 5))

        # Ensure DataFrame is sorted by year
        df = df.sort_values('Year').reset_index(drop=True)

        # Plot actual data
        actual = df[df['Year'].isin(original_years)]
        ax.plot(
            actual['Year'], actual['Population'],
            label="Population (actual)", linewidth=2, color='blue'
        )

        # Plot forecast data, ensuring continuity
        forecast = df[~df['Year'].isin(original_years)]
        if not forecast.empty:
            joined = pd.concat([actual.tail(1), forecast])
            joined = joined.sort_values('Year')
            ax.plot(
                joined['Year'], joined['Population'],
                label="Population (forecast)", linestyle='--',
                linewidth=2, color='red', alpha=0.8
            )

        ax.set_xlabel('Year')
        ax.set_ylabel('Population (millions)')
        ax.set_title('Population of Russia Over Time')
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        full_path = os.path.join(self.static_path, self.chart_filename)
        plt.savefig(full_path)
        plt.close()

        return self.chart_filename