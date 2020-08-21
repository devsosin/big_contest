import scrapy
import json
from bs4 import BeautifulSoup

# 11st Item Cralwer
class ExampleSpider(scrapy.Spider):
    
    name = "11ST"

    category_num = 1001295
    MAX_CATEGORY = 1003137
    page_num = 1
    PAGE_LIMIT = 5
    
    start_urls = [
        'http://www.11st.co.kr/category/DisplayCategory.tmall?method=getSearchFilterAjax&pageLoadType=ajax&version=1.2&method=getDisplayCategory2Depth&pageSize=40&viewType=I&lCtgrNo={0}&dispCtgrNo={0}&pageNo={1}&pageNum={1}'.format(category_num, page_num)
    ]

    def parse(self, response):
        sources = json.loads(response.text)
        sp = BeautifulSoup(sources['template'], 'html.parser')
        for item in sp.select('li'):
            yield{
                'category' : ExampleSpider.category_num,
                'item_name' : item.select_one('div.pname p').text
            }

        ExampleSpider.page_num += 1
        if ExampleSpider.page_num > ExampleSpider.PAGE_LIMIT:
            ExampleSpider.page_num = 1
            if ExampleSpider.category_num < ExampleSpider.MAX_CATEGORY:
                ExampleSpider.category_num += 1
            else:
                return

        yield scrapy.Request('http://www.11st.co.kr/category/DisplayCategory.tmall?method=getSearchFilterAjax&pageLoadType=ajax&version=1.2&method=getDisplayCategory2Depth&pageSize=40&viewType=I&lCtgrNo={0}&dispCtgrNo={0}&pageNo={1}&pageNum={1}'.format(ExampleSpider.category_num, ExampleSpider.page_num), callback=self.parse)
            
