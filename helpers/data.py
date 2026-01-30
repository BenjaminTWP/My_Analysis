import pandas as pd

def get_df_from_csv(year_column=True):

    df = pd.read_csv('data/exercise_data.csv')
    df['date'] = pd.to_datetime(df['date'])

    if year_column:
        df['year'] = df['date'].dt.year
    
    return df.copy()