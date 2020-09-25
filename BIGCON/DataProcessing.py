import pandas as pd
import datetime

# DateTime 형변환
def date_change(datas, target_col = 'date', date_format = '%Y-%m-%d %H:%M'):
    datas[target_col] = datas[target_col].apply(lambda i : datetime.datetime.strptime(i, date_format))
    return datas

# 카테고리 피쳐화
def make_feature(datas, target_col = '상품군'):
    category = list(datas[target_col])

    for c in set(category):
        datas[c] = 0

    for i,c in enumerate(category):
        datas[c][i] = 1
    
    return datas

def normalize(datas, target_col, norm_df=''):
    if type(norm_df) == str:
        norm_df = datas.describe()

    data_mean, data_std = norm_df[target_col][['mean','std']]
    datas[target_col] = (datas[target_col] - data_mean) / data_std

    return datas