import scrapy

# TV Channel Cralwer
class ExampleSpider(scrapy.Spider):
    
    name = "11ST"

    category_num = 1001295
    MAX_CATEGORY = 1003137
    page_num = 10
    PAGE_LIMIT = 10
    
    start_urls = [
        'http://www.11st.co.kr/category/DisplayCategory.tmall?method=getDisplayCategory2Depth&dispCtgrNo={}#pageNum%%{}'.format(category_num, page_num)
    ]

    def parse(self, response):
        items = response.css('div.product_listing').get()
        yield {'category':items}
        return
        
        if items != [] :
            for item in items:
                yield {
                    'title' :  item.css('div.pname p::text').get()
                }

        ExampleSpider.page_num += 1
        if ExampleSpider.page_num < ExampleSpider.PAGE_LIMIT:
            yield scrapy.Request('http://www.11st.co.kr/category/DisplayCategory.tmall?method=getDisplayCategory2Depth&dispCtgrNo={}#pageNum%%{}'.format(ExampleSpider.category_num, ExampleSpider.page_num), callback=self.parse)
        else:
            ExampleSpider.page_num = 1
            if ExampleSpider.category_num < ExampleSpider.MAX_CATEGORY:
                ExampleSpider.category_num += 1
                yield scrapy.Request('http://www.11st.co.kr/category/DisplayCategory.tmall?method=getDisplayCategory2Depth&dispCtgrNo={}#pageNum%%{}'.format(ExampleSpider.category_num, ExampleSpider.page_num), callback=self.parse)
            
