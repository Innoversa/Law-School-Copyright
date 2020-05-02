import scrapy
# from amazonscrap.items import AmazonscrapItem
from scrapy import signals
from scrapy.crawler import CrawlerProcess
import pandas as pd
# to run : scrapy crawl book-scraper


class BooksSpider(scrapy.Spider):
    name = "book-scraper"
    # def pass_in_df(self,df):
    #     self.df=df
    #     if 'title' in df.columns:
    #         self.book_names=df['title'].tolist()
    #     elif 'Title' in df.columns:
    #         self.book_names=df['Title'].tolist()

    def start_requests(self):
        search_base = 'https://www.amazon.com/s?k='
        book_names = []
        df=current_df[0]
        if 'title' in df.columns:
            book_names=df['title'].str.replace('\xa0','').tolist()
        elif 'Title' in df.columns:
            book_names=df['Title'].str.replace('\xa0','').tolist()
        print(book_names)

        #TODO for Aditya:
        #Scraper does not work on customized input, such as the list below. No result will be retrieved by this script
        #Also, running this code multiple times have a chance of getting inconsistent result for items

        book_names=['Pride and Prejudice', 'Jane Eyre', 'The Picture of Dorian Gray', 'Wuthering Heights', 'Crime and Punishment',
         'Frankenstein', 'The Count of Monte Cristo', "Alice's Adventures in Wonderland & Through the Looking-Glass",
         'Dracula', 'Les Misérables']

        #legacy code
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
        scrape_result[title]=all_prices
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


current_df=[]
scrape_result={}

def start_crawler(df_dict, output_path,progress_callback):
    tmp_r=[k for k in scrape_result]
    for key in tmp_r: del scrape_result[key]

    while len(current_df)>0:
        current_df.pop()
    print(df_dict)
    for k in df_dict:
        current_df.append(df_dict[k])
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })

        process.crawl(BooksSpider)
        process.start() # the script will block here until the crawling is finished
        print('##########################')
        current_df.pop()

    dfo = pd.DataFrame(columns=['Title','Paperback','Audiobook','Hardcover','Kindle'])
    i=0
    for title in scrape_result:
        print(title)
        dfo.loc[i,'Title']=title.strip()
        for book_price_type in scrape_result[title]:
            dfo.loc[i,book_price_type]=scrape_result[title][book_price_type].strip().replace('$','')
        i+=1
    dfo.to_csv(output_path+'/amzout.csv')
