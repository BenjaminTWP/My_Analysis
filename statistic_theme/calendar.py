from helpers.data import get_df_from_csv
import pandas as pd
import numpy as np
import calplot

def calendar_activity(filter):
    df = filter(get_df_from_csv())
    events = pd.Series(np.ones(len(df)), index=df['date'])
    calplot.calplot(events, cmap="Pastel2", yearlabel_kws={'fontname':'sans-serif'})