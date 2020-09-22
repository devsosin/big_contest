import pandas as pd
import datetime

def date_change(datas, target_col = 'date', date_format = '%Y-%m-%d %H:%M'):
    datas[target_col] = datas[target_col].apply(lambda i : datetime.datetime.strptime(i, date_format))
    return datas
