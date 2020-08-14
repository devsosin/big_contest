import scrapy
import datetime

# TV Channel Cralwer
class ExampleSpider(scrapy.Spider):
    
    name = "EBS"

    # EBS
    start_date = '20190101'
    
    start_urls = [
        'https://www.ebs.co.kr/schedule?channelCd=tv&date={}&onor=tv'.format(start_date)
    ]
    
    now_date = datetime.date(2019,1,1)
    end_date = datetime.date(2020,1,1)
    def parse(self, response):

        for tv in response.css('ul.main_timeline li'):
            if tv.css('div.time > span::text').get() == None:
                break
            yield {
                'time' : str(ExampleSpider.now_date) + ' ' + str(tv.css('div.time > span::text').get()),
                'title' :  tv.css('div.tit p > strong::text').get(),
                'content' : tv.css('div.tit p > span::text').get()
            }
        ExampleSpider.now_date += datetime.timedelta(days=1)

        if ExampleSpider.now_date >= ExampleSpider.end_date:
            return
        yield scrapy.Request('https://www.ebs.co.kr/schedule?channelCd=tv&date={}&onor=tv'.format(str(ExampleSpider.now_date).replace('-','')), callback=self.parse)
