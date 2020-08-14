import scrapy
import datetime

# TV Channel Cralwer
class ExampleSpider(scrapy.Spider):
    
    name = "HYUNDAI"

    # HYUNDAI
    start_date = '20190101'
    
    start_urls = [
        'http://www.hyundaihmall.com/front/bmc/brodPordPbdv.do?date={}'.format(start_date)
    ]
    
    now_date = datetime.date(2019,1,1)
    end_date = datetime.date(2020,1,1)

    def parse(self, response):

        for tv in response.css('ul#brodListTop li'):
            if tv.css('p.time::text').get() == None:
                break
            yield {
                'time' : str(ExampleSpider.now_date) + ' ' + str(tv.css('p.time::text').get()),
                'category' : tv.css('span.host b::text').get(),
                'title' :  tv.css('p.prod_tit a::text').getall()
            }

        ExampleSpider.now_date += datetime.timedelta(days=1)

        if ExampleSpider.now_date == ExampleSpider.end_date:
            return
        yield scrapy.Request('http://www.hyundaihmall.com/front/bmc/brodPordPbdv.do?date={}'.format(str(ExampleSpider.now_date).replace('-','')), callback=self.parse)
