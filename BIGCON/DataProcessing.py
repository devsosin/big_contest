import pandas as pd
import datetime

def date_change(datas, target_col = 1, date_format = '%Y-%m-%d %H:%M'):
    datas[datas.columns[target_col]] = datas[datas.columns[target_col]].apply(lambda i : datetime.datetime.strptime(i, date_format))
    return datas
