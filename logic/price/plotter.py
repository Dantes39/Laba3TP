import os


class InflationPlotter:
    def __init__(self, static_folder='static'):
        import os
        self.path = os.path.abspath(static_folder)
        os.makedirs(self.path, exist_ok=True)

    def plot(self, df, original_years):
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(10, 5))

        actual = df[df['Year'].isin(original_years)]
        forecast = df[~df['Year'].isin(original_years)]

        ax.plot(actual['Year'], actual['Inflation'], label='Фактическая инфляция', linewidth=2)
        if not forecast.empty:
            ax.plot(forecast['Year'], forecast['Inflation'], '--', label='Прогноз', linewidth=2, color='orange')

        ax.set_xlabel('Год')
        ax.set_ylabel('Инфляция (%)')
        ax.set_title('Инфляция в России')
        ax.legend()
        plt.grid(True)
        plt.tight_layout()

        filepath = os.path.join(self.path, 'inflation.png')
        plt.savefig(filepath)
        plt.close()
        return 'inflation.png'
