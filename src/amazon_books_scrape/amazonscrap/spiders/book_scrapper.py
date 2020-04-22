import scrapy
# from amazonscrap.items import AmazonscrapItem
from scrapy import signals

# to run : scrapy crawl book-scraper
class BooksSpider(scrapy.Spider):
    name = "book-scraper"
    start_urls = [
        'https://www.amazon.com/15-Invaluable-Laws-Growth-Potential/dp/B009KF1JXI/ref=pd_vtpd_14_2/146-8950855-9827903?_encoding=UTF8&pd_rd_i=B009KF1JXI&pd_rd_r=7686f2a6-6f92-4657-9bdb-cf960ff286d4&pd_rd_w=XD2CI&pd_rd_wg=dOfwP&pf_rd_p=be9253e2-366d-447b-83fa-e044efea8928&pf_rd_r=P551JA4BJQ11BEXH4B68&psc=1&refRID=P551JA4BJQ11BEXH4B68'
        ,'https://www.amazon.com/Python-Crash-Course-Hands-Project-Based-ebook/dp/B018UXJ9RI/ref=sr_1_4?dchild=1&keywords=python+crash&qid=1587273440&sr=8-4'
        ,'https://www.amazon.com/Success-Principles-TM-Anniversary-Where/dp/0062364286/ref=sr_1_3?crid=8LPPMYAIAM2Y&dchild=1&keywords=success+principles+canfield&qid=1587279182&sprefix=success+pri%2Caps%2C186&sr=8-3'
        # ,'https://www.amazon.com/Python-Crash-Course-Hands-Project-Based-ebook/dp/B018UXJ9RI/ref=sr_1_4?dchild=1&keywords=python+crash&qid=1587273440&sr=8-4'
    ]

    books_already_scrapped = list()

    def parse(self, response):
        book = {}
        
        title = response.css('span[class="a-size-extra-large"]::text').get()

        if title == None:
            title = response.css('title::text')[0].get()

        # prices = response.css('[class="a-unordered-list a-nostyle a-button-list a-horizontal"]')
        prices = response.css('a[class="a-button-text"]')
        
        all_prices = {}
        for p in prices:
            if '$' in p.get():
                book_type = p.css('span::text').get()
                html_data = p.get()
                price_idx = html_data.find('$')
                price = html_data[price_idx:html_data.find('<',price_idx)]
                price = price[:price.find('\n')]
                all_prices[book_type] = price
        print('====================================\n',title,'\n',all_prices)
        print('====================================')
        
        return book

    @staticmethod
    def get_book_id(response):
        url = response.request.url
        url = url.split("/")
        return url[-2]

    def spider_opened(self):
        print("\n\n\nSpider Opened")
        print(self.start_urls)



    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(BooksSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        return spider

    @staticmethod
    def escape(text):
        text = text.replace("'","''")
        return text
