import matplotlib.pyplot as plt
import os

class InflationPlotter:
    def __init__(self, path='static'):
        self.path = path

    def plot(self, df_forecast, original_years):
        plt.figure(figsize=(10, 5))

        # Исторические данные
        historical = df_forecast[df_forecast['Year'].isin(original_years)]
        plt.plot(historical['Year'], historical['Inflation'], label='Фактическая инфляция', marker='o')

        # Прогнозные данные
        forecast = df_forecast[~df_forecast['Year'].isin(original_years)]
        if not forecast.empty:
            plt.plot(forecast['Year'], forecast['Inflation'], label='Прогноз инфляции', marker='o', linestyle='--')

            # Соединение последней точки истории с первой точкой прогноза
            last_hist = historical.iloc[-1]
            first_fore = forecast.iloc[0]
            plt.plot([last_hist['Year'], first_fore['Year']],
                     [last_hist['Inflation'], first_fore['Inflation']],
                     color='gray', linestyle='--', linewidth=1)

        plt.title('Инфляция: история и прогноз')
        plt.xlabel('Год')
        plt.ylabel('Инфляция (%)')
        plt.legend()
        plt.grid(True)

        filepath = os.path.join(self.path, 'inflation.png')
        plt.tight_layout()
        plt.savefig(filepath)
        plt.close()

        return filepath
