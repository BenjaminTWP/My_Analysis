from helpers.data import get_df_from_csv
import matplotlib.ticker as ticker 
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd
import numpy as np


def format_mmss(x, pos): 
    m = int(x // 60) 
    s = int(x % 60) 
    return f"{m}:{s:02d}"

def crawl_filter(df, from_year=2025, to_year=3000):
    df = df[(df['year'] >= from_year) & (df['year'] <= to_year)]
    df = df[df['workout'] == "simning"]
    return df.copy()

def swimming_speed(unit="km/h"):
    df = crawl_filter(get_df_from_csv())
    tot_swim = df.shape[0]

    df = df.dropna(subset=["distance_(km)", "duration_(min)"])
    df['date'] = pd.to_datetime(df['date'])

    if unit == "100m/min:sec":
        # compute pace in seconds per 100m
        total_seconds = df["duration_(min)"] * 60
        pace_100m_sec = total_seconds / (df["distance_(km)"] * 1000) * 100
        df["pace_sec"] = pace_100m_sec
        plot_values = df["pace_sec"]

        # format y-axis as mm:ss
        ax = plt.gca()
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_mmss))

    else:
        # km/h
        df['speed'] = df["distance_(km)"] / (df["duration_(min)"] / 60)
        plot_values = df["speed"]

    # --- plotting ---
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))

    plt.xlabel("Date (first was 2025-09-28)")
    plt.title(f"Swimming speed (having swimmed {tot_swim} times)")
    plt.ylabel(unit)

    plt.step(df['date'], plot_values, where='post', color="black", zorder=1)
    plt.scatter(df['date'], plot_values, c=df['heart_rate'], cmap='rainbow', s=45, zorder=2)

    plt.gcf().autofmt_xdate()
    plt.colorbar(label='Heart Rate')
    plt.show()

