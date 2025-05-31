import matplotlib.pyplot as plt
import os
import pandas as pd

plt.switch_backend('Agg')


class CurrencyPlotter:
    def __init__(self, static_folder='static'):
        self.static_path = os.path.abspath(static_folder)
        os.makedirs(self.static_path, exist_ok=True)
        self.chart_filename = 'chart.png'

    def plot(self, df: pd.DataFrame, original_dates: list[str]) -> str:
        fig, ax = plt.subplots(figsize=(10, 5))

        # Ensure DataFrame is sorted by date
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date').reset_index(drop=True)

        currencies = [col for col in df.columns if col not in ['Date']]

        for currency in currencies:
            currency_data = df[df[currency].notna()]
            actual = currency_data[currency_data['Date'].astype(str).isin(original_dates)]
            forecast = currency_data[~currency_data['Date'].astype(str).isin(original_dates)]

            # Plot actual data
            ax.plot(
                actual['Date'], actual[currency],
                label=f"{currency} (actual)", linewidth=2
            )

            # Plot forecast data, ensuring continuity
            if not forecast.empty:
                joined = pd.concat([actual.tail(1), forecast])
                joined = joined.sort_values('Date')
                ax.plot(
                    joined['Date'], joined[currency],
                    label=f"{currency} (forecast)", linestyle='--',
                    linewidth=2, alpha=0.8
                )

        ax.set_xlabel('Date')
        ax.set_ylabel('Exchange Rate (RUB)')
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        full_path = os.path.join(self.static_path, self.chart_filename)
        plt.savefig(full_path)
        plt.close()

        return self.chart_filename