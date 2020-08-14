import scrapy
import datetime

# TV Channel Cralwer
class ExampleSpider(scrapy.Spider):
    
    name = "HOMEANDSHOPPING"

    # HOME AND SHOPPING
    start_date = '2019/12/31'
    
    start_urls = [
        'http://www.hnsmall.com/display/tvtable.do?from_date={}'.format(start_date)
    ]
    
    now_date = datetime.date(2019,12,31)
    end_date = datetime.date(2020,1,1)

    def parse(self, response):

        for tv in response.css('tbody tr'):
            yield {
                'time' : str(ExampleSpider.now_date) + ' ' + str(tv.css('span.time::text').get()),
                'title' : tv.css('div.text a strong::text').get(),
                'content' :  tv.css('div.text a::text').getall()
            }

        ExampleSpider.now_date += datetime.timedelta(days=1)

        if ExampleSpider.now_date == ExampleSpider.end_date:
            return
        yield scrapy.Request('http://www.hnsmall.com/display/tvtable.do?from_date={}'.format(str(ExampleSpider.now_date).replace('-','/')), callback=self.parse)
