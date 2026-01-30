from helpers.data import get_df_from_csv
from helpers.mapping import name_dict
import matplotlib.pyplot as plt
import numpy as np

def plot_workout_per_year(colormap="Set1"):
    df = get_df_from_csv()

    # Define workout types and fixed colormap
    workout_types = df['workout'].dropna().unique()
    workout_types = workout_types[workout_types != "missing_workout_type"]
    cmap = plt.get_cmap(colormap)
    colors = cmap(np.linspace(0, 1, len(workout_types)))
    color_map = dict(zip(workout_types, colors))

    # Create pie charts
    years = sorted(df['year'].unique())
    _, axes = plt.subplots(3, 3, figsize=(14, 8))
    axes = axes.flatten()

    for i, year in enumerate(years):
        ax = axes[i]
        year_data = df[df['year'] == year]
        workouts = year_data['workout'].value_counts()

        # Keep only >0 entries and map to color order
        workouts = workouts[workouts > 0]
        workouts = workouts.reindex([w for w in workout_types if w in workouts.index])
        total = workouts.sum()
        labels = [name_dict.get(w, w) for w in workouts.index]

        wedges, texts, autotexts = ax.pie(
            workouts,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            colors=[color_map[w] for w in workouts.index]
        )

        for text in autotexts:
            text.set_fontsize(10)
            text.set_color('white')

        ax.set_title(f'{year} ({total} träningspass)')
        ax.set_ylabel('')


    for j in range(i + 1, len(axes)):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()

