# Load File 사용 가능한 상태로 전처리

import pandas as pd
from datetime import datetime

def load():
    perform_df = pd.read_json('datas/raw_data/raw_perform.json')
    rating_df = pd.read_json('datas/raw_data/raw_rating.json')
    test_df = pd.read_json('datas/test_data/forecast.json')

    # Datetime 으로 변경
    perform_df['방송일시'] = list(map(lambda i : datetime.fromtimestamp(i/1000), perform_df['방송일시']))
    test_df['방송일시'] = list(map(lambda i : datetime.fromtimestamp(i/1000), test_df['방송일시']))

    # int형으로 변경
    perform_df['판매단가'] = list(map(lambda i : None if i == ' - ' else i, perform_df['판매단가']))
    perform_df['판매단가'] = list(map(lambda i : int(i.replace(',','')) if i != None else None, perform_df['판매단가']))
    perform_df[' 취급액 '] = list(map(lambda i : int(i.replace(',','')) if i != None else None, perform_df[' 취급액 ']))

    test_df['판매단가'] = list(map(lambda i : None if i == ' - ' else i, test_df['판매단가']))
    test_df['판매단가'] = list(map(lambda i : int(i.replace(',','')) if i != None else None, test_df['판매단가']))


    return perform_df, rating_df, test_df
