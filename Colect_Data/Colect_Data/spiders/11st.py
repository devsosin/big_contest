import scrapy
import json
from bs4 import BeautifulSoup
import pandas as pd
import FileMaker

# 11st Item Cralwer
class ExampleSpider(scrapy.Spider):
    
    name = "11ST"

    category_num = pd.read_json(r'C:\Users\student\big_contest\datas\out_data\category_table.json')['mid_cate_id'].unique()
    now_category = 0
    # MAX_CATEGORY = 1003137
    page_num = 1
    PAGE_LIMIT = 5
    
    def start_requests(self):
        url = 'http://www.11st.co.kr/category/DisplayCategory.tmall?method=getSearchFilterAjax&pageLoadType=ajax&version=1.2&method=getDisplayCategory2Depth&pageSize=40&viewType=I&lCtgrNo={0}&dispCtgrNo={0}&pageNo={1}&pageNum={1}'.format(ExampleSpider.category_num[ExampleSpider.now_category], ExampleSpider.page_num)
        ExampleSpider.fm = FileMaker.JsonMaker()
        ExampleSpider.fm.create_folder()
        ExampleSpider.fm.write_file()

        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        sources = json.loads(response.text)
        sp = BeautifulSoup(sources['template'], 'html.parser')
        for item in sp.select('li'):
            yield ExampleSpider.fm.add_data({
                'category' : str(ExampleSpider.category_num[ExampleSpider.now_category]),
                'item_name' : str(item.select_one('div.pname p').text)
            })

        ExampleSpider.page_num += 1
        if ExampleSpider.page_num > ExampleSpider.PAGE_LIMIT:
            ExampleSpider.page_num = 1
            if ExampleSpider.now_category < len(ExampleSpider.category_num):
                ExampleSpider.now_category += 1
            else:
                return

        yield scrapy.Request('http://www.11st.co.kr/category/DisplayCategory.tmall?method=getSearchFilterAjax&pageLoadType=ajax&version=1.2&method=getDisplayCategory2Depth&pageSize=40&viewType=I&lCtgrNo={0}&dispCtgrNo={0}&pageNo={1}&pageNum={1}'.format(ExampleSpider.category_num[ExampleSpider.now_category], ExampleSpider.page_num), callback=self.parse)
            
