

def cycling_filter(df, from_year=2020, to_year=3000):
    df = df[(df['year'] >= from_year) & (df['year'] <= to_year)]
    df = df[(df['workout'] == "motionscykel")]
    return df.copy()