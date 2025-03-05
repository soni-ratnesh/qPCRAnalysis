from app.core.config import Config
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns

PLOT_OUTPUT_DIR = Config.UPLOAD_DIR 
os.makedirs(PLOT_OUTPUT_DIR, exist_ok=True)

# Function to generate different types of plots

def generate_plots(pow2: pd.DataFrame, delta_ct: pd.DataFrame, normalized: pd.DataFrame) -> list[str]:
    plot_paths = []

    # Bar Plot for Mean Values
    for column in normalized.columns:
        plt.figure()  # Create a new figure for each plot
        normalized[column].plot(kind='bar', title=f'Bar plot of {column}')
        plot_path = os.path.join(PLOT_OUTPUT_DIR, f'plots_{column}.png')

        plt.xlabel(column)
        plt.ylabel('Norm')
        plt.tight_layout()
        plt.savefig(plot_path)
        plt.close()
        plot_paths.append(plot_path)


    return plot_paths

