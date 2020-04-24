import scrapy
# from amazonscrap.items import AmazonscrapItem
from scrapy import signals

# to run : scrapy crawl book-scraper
class BooksSpider(scrapy.Spider):
    name = "book-scraper"
    
    def start_requests(self):
        search_base = 'https://www.amazon.com/s?k='
        book_names = ['What Every BODY Is Saying: An Ex-FBI Agent’s Guide to Speed-Reading People',
                      'Louder Than Words: Take Your Career from Average to Exceptional with the Hidden Power of Nonverbal Intelligence']

        for names in book_names:
            yield scrapy.Request(url=search_base + names, callback=self.parse)
    
    def parse(self, response):
        

        book_link = response.css('div[data-index="1"]')
        # book_link = book_link.css('div[class="sg-row"]')
        book_link = book_link.css('a[class="a-link-normal"]').get()
        
        link_pos = book_link.find('href')
        
        link_start = book_link.find('"',link_pos+1)
        link_end = book_link.find('"',link_start+1)
        
        
        book_page = book_link[link_start+1:link_end]
        base_link = "https://www.amazon.com/"
        book_page = base_link + book_page
        
        yield scrapy.Request(book_page, callback=self.parse_book)
        
    def parse_book(self, response):
        
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
