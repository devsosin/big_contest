# 패키지 Import
import pandas as pd
import numpy as np
import datetime
import re
import copy
import math
import matplotlib.pyplot as plt
import seaborn as sns

from soynlp.vectorizer import BaseVectorizer

import lightgbm as lgb
import xgboost as xgb

import pickle
from sklearn.externals import joblib

# 전처리 클래스

class DataProcessing:
    # DateTime 형변환
    def date_change(self, datas, target_col = 'date', date_format = '%Y-%m-%d %H:%M'):
        datas[target_col] = datas[target_col].apply(lambda i : datetime.datetime.strptime(i, date_format))
        return datas

    # 카테고리 피쳐화
    def make_feature(self, datas, target_col = '상품군'):
        category = list(datas[target_col])

        for c in set(category):
            datas[c] = 0

        for i,c in enumerate(category):
            datas[c][i] = 1
        
        return datas

    def normalize(self, datas, target_col, norm_df=''):
        if type(norm_df) == str:
            norm_df = datas.describe()

        data_mean, data_std = norm_df[target_col][['mean','std']]
        datas[target_col] = (datas[target_col] - data_mean) / data_std

        return datas

# 단어 벡터 생성 클래스
class WordPre:
    def embedding_datas(self, datas, max_length = 16):
        datas = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]',' ', datas)
        datas = re.sub(r' ?(\d+) ?', r' \1', datas)
        with open(r'helper_data\vect.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
        temp = pd.DataFrame(vectorizer.encode_a_doc_to_list(datas)).T.fillna(0).astype(int)
        now_columns = len(temp.columns)
        if now_columns < max_length:
            for i in range(now_columns, max_length):
                temp[i] = 0
        co = temp.columns[:max_length]
        return temp[co]



def forecasting(present):
    dp = DataProcessing()
    wp = WordPre()
    product_df = pd.DataFrame.from_dict(present, orient='index').T
    wv = np.asarray(wp.embedding_datas(product_df['상품명'][0]))

    dp.date_change(product_df, '방송일시')
    # 주말 1 평일 0
    product_df['요일'] = product_df['방송일시'].apply(lambda i : 1 if i.weekday() % 7 in[5,6] else 0)

    # 월, 시간, 상품군 피쳐 생성
    for i in range(1,13):
        product_df['%s월'%i] = 0
    for i in range(24):
        product_df['%s시'%i] = 0
    for i in ['잡화', '농수축', '주방', '건강기능', '이미용', '의류', '가전', '생활용품', '가구', '침구', '속옷']:
        product_df[i] = 0

    product_df['방송일시'].apply(lambda i : '%s월'%i.month)
    product_df['%s월'%product_df['방송일시'][0].month]=1
    product_df['%s시'%product_df['방송일시'][0].hour]=1
    product_df[product_df['상품군'][0]] = 1

    # 시청률 분석
    watch_rating_df = pd.read_csv(r'helper_data\view_rating.csv')
    # 평균 로우, 칼럼 제거
    watch_rating_df.drop(len(watch_rating_df)-1, axis=0, inplace=True)
    watch_rating_df.drop(watch_rating_df.columns[-1], axis=1, inplace=True)

    # 시간대 Index화
    watch_rating_df.set_index('시간대', inplace=True)
    watch_rating_df.sort_index(inplace=True)

    # 평균 값으로 채우기
    temp = watch_rating_df.mean(axis=1)
    for c in watch_rating_df.columns:
        watch_rating_df[c] = temp
    watch_rating_df['2020-01-01'] = temp

    # 예측 기간까지 채우기
    for i in range(1, 31):
        watch_rating_df['2020-06-{:02d}'.format(i)] = temp
    watch_rating_df['2020-07-01'] = temp

    # 1열로 활용가능하게 만들기
    total_date = watch_rating_df.columns
    total_time = watch_rating_df.index
    temp = []
    for this_date in total_date:
        for this_time in total_time:
            temp.append(('%s %s'%(this_date, this_time), watch_rating_df[this_date][this_time]))

    view_df = dp.date_change(pd.DataFrame(temp, columns = ['date', 'rate']), 'date')
    view_df.set_index('date', inplace=True)

    # 편성 프로그램 별 시청률 계산
    temp = list(map(lambda i : sum(view_df['rate'][i['방송일시'] : i['방송일시'] + datetime.timedelta(minutes=int(i['노출(분)']))]), product_df.iloc))
    product_df['view'] = temp

    # 기상 분석
    # 3일 예보
    cloud_df = pd.read_csv(r'helper_data\cloud_forecast_기상청.csv', index_col=0)
    tem_df = pd.read_csv(r'helper_data\tem_forecast_기상청.csv', index_col=0)
    weather_cate = {'맑음' :0, '구름조금' : 1, '구름많음' :2, '흐림' :3, '구름많고 눈' :4, '흐리고 눈' :7, '구름많고 비': 5, '흐리고 비' :8, '구름많고 비/눈' :6, '흐리고 비/눈' :9}
    cloud_df['wc'] = cloud_df['예보'].apply(lambda i : weather_cate[i])

    # 인구수에 따라 날씨 상태 수치화
    temp = cloud_df['popul'].unique().sum()
    cloud_df['p*wc'] = cloud_df['popul'] / temp  * cloud_df['wc']
    cloud_df = cloud_df.groupby('forecast').sum()

    product_df['pwc'] = cloud_df.loc[str(product_df['방송일시'][0].date())]['p*wc']

    temp = tem_df['popul'].unique().sum()
    tem_df['p*lowtem'] = tem_df['popul'] / temp * tem_df['최저기온']
    tem_df['p*hightem'] = tem_df['popul'] / temp * tem_df['최고기온']

    # 예측 일자 별 최저 기온, 최고 기온 추가
    tem_df = tem_df.groupby('예보시각').sum()
    product_df['plowtem'] = tem_df.loc[str(product_df['방송일시'][0].date())]['p*lowtem']
    product_df['phightem'] = tem_df.loc[str(product_df['방송일시'][0].date())]['p*hightem']

    norm_df = pd.read_csv(r'helper_data\norm_df.csv', index_col=0)

    # 정규화 필요 Column List
    norm_column = ['노출(분)', '판매단가', 'view', 'pwc', 'plowtem', 'phightem']

    for c in norm_column:
        dp.normalize(product_df, c, norm_df)

    # 학습에 필요한 Column
    train_column = ['노출(분)',  '판매단가', 'view', '요일',
                    # 월
                    '1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월', 
                    # 시간대
                    '6시', '7시', '8시', '9시', '10시', '11시', '12시', '13시', '14시', '15시', '16시', '17시', '18시', '19시', '20시', '21시', '22시', '23시', '0시', '1시', '2시',
                    # 상품군
                    '잡화', '농수축', '주방', '건강기능', '이미용', '의류', '가전', '생활용품', '가구', '침구', '속옷',
                    # 기상
                    'pwc', 'plowtem', 'phightem']

    product_X = np.asarray(product_df[train_column]).reshape(-1, len(train_column))
    product_X = np.concatenate((wv, product_X), axis=1)

    print(product_X.shape)
    xgb_model_load = joblib.load(r'helper_data\xgb_best.pkl')
    return '예상 매출액 : %s원'%int(xgb_model_load.predict(product_X)[0])