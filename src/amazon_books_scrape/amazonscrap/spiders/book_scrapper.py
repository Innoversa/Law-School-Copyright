import scrapy
# from amazonscrap.items import AmazonscrapItem
from scrapy import signals
from scrapy.crawler import CrawlerProcess
import pandas as pd
# to run : scrapy crawl book-scraper


class BooksSpider(scrapy.Spider):
    name = "book-scraper"

    def start_requests(self):
        search_base_p1 = 'https://www.amazon.com/s?k='
        search_base_p2 = '&i=stripbooks&ref=nb_sb_noss_2'
        self.search_base_p1=search_base_p1
        self.search_base_p2=search_base_p2
        book_names = []
        df=current_df[0]
        if 'title' in df.columns:
            book_names=df['title'].str.replace('\xa0','').tolist()
        elif 'Title' in df.columns:
            book_names=df['Title'].str.replace('\xa0','').tolist()
        print(book_names)
        # book_names=['Pride and Prejudice', 'Jane Eyre', 'The Picture of Dorian Gray', 'Wuthering Heights', 'Crime and Punishment',
        #  'Frankenstein', 'The Count of Monte Cristo', "Alice's Adventures in Wonderland & Through the Looking-Glass",
        #  'Dracula', 'Les Misérables']

        # #legacy code
        # book_names = ['What Every BODY Is Saying: An Ex-FBI Agent’s Guide to Speed-Reading People',
        #              'Louder Than Words: Take Your Career from Average to Exceptional with the Hidden Power of Nonverbal Intelligence']
        for names in book_names:
            if len(names)==0:
                continue
            print(search_base_p1 + names + search_base_p2)
            yield scrapy.Request(url=search_base_p1 + names.replace(' ','%20') + search_base_p2, callback=self.parse,cb_kwargs={'current_book':names})
                
    def parse(self, response, current_book):
        i=0
        #print('##'+current_book)
        while True:
            if i>20:
                print('============================================\nPlease check book name and search again\n',i)
                return 0
            
            print('___________searching','data-index="'+str(i))
            search_label = 'data-index="'+str(i)+'"'
            book_link = response.css('div['+search_label+']')
            sponsored_book = book_link.css('div[class="a-row a-spacing-micro"]').get()

            book_link = book_link.css('a[class="a-link-normal a-text-normal"]')
            if book_link.get() is not None and sponsored_book is None:
                
                found_book_name =  book_link.css('span[class="a-size-medium a-color-base a-text-normal"]').get()            
                if found_book_name:
                    found_book_name_s = found_book_name.find('>')
                    found_book_name_e = found_book_name.find('<', found_book_name_s+1)
                    found_book_name = found_book_name[found_book_name_s+1:found_book_name_e]
                    print('found book_________________________',i,found_book_name)
                    break  
            i+=1
            sponsored_book = None
        
        i=0
                   
        book_link = book_link.get()
        link_pos = book_link.find('href')
        
        link_start = book_link.find('"',link_pos+1)
        link_end = book_link.find('"',link_start+1)
        
        
        book_page = book_link[link_start+1:link_end]
        base_link = "https://www.amazon.com/"
        book_page = base_link + book_page
        yield scrapy.Request(book_page, callback=self.parse_book, cb_kwargs={'current_book':current_book})
        
    def parse_book(self, response, current_book):
        print('@@@'+response.url)
        book = {}
        title = response.css('span[class="a-size-extra-large"]::text').get()

        if title == None:
            title = response.css('title::text')[0].get()
            
        title = title.lstrip()
        title = title.rstrip()
            
        # prices = response.css('[class="a-unordered-list a-nostyle a-button-list a-horizontal"]')
        prices = response.css('a[class="a-button-text"]')
        
        all_prices = {}
        for p in prices:
            if '$' in p.get():
                book_type = p.css('span::text').get()
                bt = ''
                for c in book_type:
                    if c not in [' ','\n']:
                        bt += c
                book_type = bt
                html_data = p.get()
                price_idx = html_data.find('$')
                price = html_data[price_idx:html_data.find('<',price_idx)]
                price = price[:price.find('\n')]
                all_prices[book_type] = price
        
        if len(all_prices)==0:
            new_url = response.url
            new_url_change_pos = new_url.find('com')
            new_url = new_url[0:new_url_change_pos]+'in'+new_url[new_url_change_pos+3:]
            yield scrapy.Request(new_url, callback=self.parse_book, cb_kwargs={'current_book':current_book})
        
        else:    
            print('====================================\n',title,'\n',all_prices)
            print('====================================')
            all_prices['book_found']=title
            scrape_result[current_book] = all_prices
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

    writer = pd.ExcelWriter(output_path+'/amazonoutput.xlsx', engine='xlsxwriter')
    for sheet_name in df_dict:
        if df_dict[sheet_name].shape[0]==0:
            continue
        current_df.append(df_dict[sheet_name])
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })

        process.crawl(BooksSpider)
        process.start() # the script will block here until the crawling is finished
        print('##########################')
        print(current_df[0].columns)
        print(scrape_result)
        dfo = pd.DataFrame(index=range(current_df[0].shape[0]),columns=['Title','BookNameFound','Paperback','Audiobook','Hardcover','Kindle'])
        i=0
        for current_book_name in scrape_result:
            dfo.loc[i,'Title']=current_book_name
            for book_price_type in scrape_result[current_book_name]:
                if book_price_type not in dfo.columns:
                    continue
                if book_price_type=='book_found':
                    dfo.loc[i,'BookNameFound']=scrape_result[current_book_name][book_price_type].strip()
                else:
                    dfo.loc[i,book_price_type]=scrape_result[current_book_name][book_price_type].strip().replace('$','')
            i+=1
        #dfo.to_csv(output_path+'/amzout.csv')
        dfo.to_excel(writer, sheet_name=sheet_name)
        #clear up
        tmp_r=[k for k in scrape_result]
        for key in tmp_r: del scrape_result[key]
        current_df.pop()
    writer.save()