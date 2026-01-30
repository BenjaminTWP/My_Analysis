from helpers.data import get_df_from_csv
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def running_filter(df, from_year=2020, to_year=3000):
    df = df[(df['year'] >= from_year) & (df['year'] <= to_year)]
    df = df[(df['workout'] == "lopband") | (df['workout'] == "lopning")]
    return df.copy()

def pace_formatter(x, pos):
    minutes = int(x)
    seconds = int(round((x - minutes) * 60))
    return f"{minutes}:{seconds:02d}"

def running_regression(degree=1, start_year=2020, end_year=2030):
    df = get_df_from_csv()

    df = df[df['year'] >= start_year]
    df = df[df['year'] <= end_year]

    # Filter for running workouts
    df = df[df['workout'].isin(['lopning', 'lopband'])].copy()
    df['pace'] = df['duration_(min)'] / df['distance_(km)']

    plt.figure(figsize=(16, 6))

    has_all = df[df['distance_(km)'].notna() & df['heart_rate'].notna()]
    missing_hr = df[df['heart_rate'].isna()]

    # Exponential distance scaling for size
    scaled_size = np.exp(has_all['distance_(km)'] / 8) * 2  # Tweak /8 and *2 as needed

    # Plot full-data points
    scatter = plt.scatter(
        has_all['date'], has_all['pace'],
        s=scaled_size,
        c=has_all['heart_rate'],
        cmap='rainbow',
        alpha=0.8,
        label='Valid data'
    )

    plt.scatter(
        missing_hr['date'], missing_hr['pace'],
        s=10,
        edgecolor='gray',
        facecolor='none',
        linewidth=1,
        label='Missing heart rate'
    )

    # Average pace lines per year
    for year, group in df.groupby('year'):
        avg = group['pace'].mean()
        minutes, seconds = divmod(avg * 60, 60)
        pace_str = f"{int(minutes)}:{int(seconds):02d}"
        start, end = group['date'].min(), group['date'].max()
        plt.hlines(avg, xmin=start, xmax=end, linestyles='--', linewidth=1.5,
                label=f'{year} avg: {pace_str} min/km')

    # Add regression line
    df_valid = df[df['pace'].notna()]
    x = df_valid['date'].map(pd.Timestamp.toordinal)
    y = df_valid['pace']
    coeffs = np.polyfit(x, y, deg=degree)
    reg_line = np.poly1d(coeffs)
    plt.plot(df_valid['date'], reg_line(x), color='magenta', linewidth=0.8, alpha=0.8, label='Trend line')

    cbar = plt.colorbar(scatter)
    cbar.set_label('Heart rate (bpm)')
    plt.xlabel('Date')
    plt.ylabel('Pace (min/km)')
    plt.title(f'Paces from running over the years (polynomial regression of degree {degree}) \n  \n Note: Size = distance, Color = heart rate')
    plt.legend()
    plt.tight_layout()
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(pace_formatter))
    plt.show()