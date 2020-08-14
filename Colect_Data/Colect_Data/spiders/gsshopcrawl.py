import scrapy
import datetime

# TV Channel Cralwer
class ExampleSpider(scrapy.Spider):
    
    name = "GSSHOP"

    # GSSHOP
    start_date = '20190101'
    
    start_urls = [
        'https://www.gsshop.com/shop/tv/tvScheduleMain.gs?lseq=415680-1&gsid=ECmain-AU415680-AU415680-1#{}_LIVE'.format(start_date)
    ]
    
    now_date = datetime.date(2019,1,1)
    end_date = datetime.date(2020,1,1)

    def parse(self, response):

        for tv in response.css('article.items'):
            yield {
                'time' : str(ExampleSpider.now_date) + ' ' + str(tv.css('span.times::text').get()),
                'title' :  tv.css('dt.prd-name::text').get(),
                # 'content' : tv.css('span.add_exp::text').get()
            }
        ExampleSpider.now_date += datetime.timedelta(days=1)

        if ExampleSpider.now_date == ExampleSpider.end_date:
            return
        yield scrapy.Request('https://www.gsshop.com/shop/tv/tvScheduleMain.gs?lseq=415680-1&gsid=ECmain-AU415680-AU415680-1#{}_LIVE'.format(str(ExampleSpider.now_date).replace('-','')), callback=self.parse)
