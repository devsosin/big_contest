import scrapy
import datetime

# TV Channel Cralwer
class ExampleSpider(scrapy.Spider):
    
    name = "JTBC"

    # JTBC
    start_date = '20190101'
    
    start_urls = [
        'http://jtbc.joins.com/schedule/{}'.format(start_date)
    ]
    
    now_date = datetime.date(2019,1,1)
    end_date = datetime.date(2020,1,1)

    def parse(self, response):

        for tv in response.css('ul.chart_time_list li'):
            yield {
                'time' : str(ExampleSpider.now_date) + ' ' + str(tv.css('div.time_v::text').get()),
                'title' :  tv.css('strong.title::text').get(),
                'content' : tv.css('span.add_exp::text').get()
            }
        ExampleSpider.now_date += datetime.timedelta(days=1)

        if ExampleSpider.now_date == ExampleSpider.end_date:
            return
        yield scrapy.Request('http://jtbc.joins.com/schedule/{}'.format(str(ExampleSpider.now_date).replace('-','')), callback=self.parse)
