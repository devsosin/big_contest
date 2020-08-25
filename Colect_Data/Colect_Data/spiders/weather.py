import scrapy
import datetime
import json
import pandas as pd

# Weather Crawling
class ExampleSpider(scrapy.Spider):
    
    name = "weather"

    # Weather
    s_day = '20190101'
    e_day = '20190101'
    num = 24
    loc_list = list(pd.read_csv(r'C:\Users\student\big_contest\datas\out_data\loc.csv', header=None)[1:][0])
    loc_count = 73
    
    
    URL = 'http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList?serviceKey=JBatS%2BMfY2VXN5uzPh4y5aEwr9i6n0dfH%2BDAwWyw8BuUwcljukH7VgytQ%2BCLnUfzIi148AUH2IGFeLAFaxN3iQ%3D%3D&pageNo=1&dataCd=ASOS&dateCd=HR&stnIds={}&startHh=00&endHh=23&dataType=JSON'.format(loc_list[loc_count])
    params = '&numOfRows={}&startDt={}&endDt={}'.format(num, s_day, e_day)


    start_urls = [
        URL + params
    ]
    
    now_date = datetime.date(2019,1,1)
    end_date = datetime.date(2020,1,1)

    def parse(self, response):
        for item in json.loads(response.text)['response']['body']['items']['item']:
            yield {
                'time' : item['tm'], # 시간
                'loc' : item['stnNm'], # 지역
                'tem' : item['ta'], # 기온
                'hum' : item['hm'], # 습도
                'rain' : item['rn'], # 강수량
                'snow' : item['dsnw'] # 적설량
            }
        ExampleSpider.now_date += datetime.timedelta(days=1)

        if ExampleSpider.now_date >= ExampleSpider.end_date:
            ExampleSpider.loc_count += 1
            if ExampleSpider.loc_count == len(ExampleSpider.loc_list):
                return
            ExampleSpider.now_date = datetime.date(2019,1,1)
            ExampleSpider.URL = 'http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList?serviceKey=JBatS%2BMfY2VXN5uzPh4y5aEwr9i6n0dfH%2BDAwWyw8BuUwcljukH7VgytQ%2BCLnUfzIi148AUH2IGFeLAFaxN3iQ%3D%3D&pageNo=1&dataCd=ASOS&dateCd=HR&stnIds={}&startHh=00&endHh=23&dataType=JSON'.format(ExampleSpider.loc_list[ExampleSpider.loc_count])
            

        yield scrapy.Request(ExampleSpider.URL + '&numOfRows={}&startDt={}&endDt={}'.format(ExampleSpider.num, 
                            str(ExampleSpider.now_date).replace('-',''),
                            str(ExampleSpider.now_date).replace('-','')), callback=self.parse)
