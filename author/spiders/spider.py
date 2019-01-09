from scrapy.spiders import CrawlSpider
from scrapy import Selector,item
from scrapy import Request
from author.items import  AuthorItem
class A(CrawlSpider):
    name = "author"
    start_urls = ['https://www.jianshu.com/recommendations/users?utm_source=desktop&utm_medium=index-users']
    def parse(self,response):
        selector = Selector(response)
        authors = selector.xpath('//div[@class="row"]/div/div/a[@target="_blank"]')
        for auth in  authors :
            url = "https://www.jianshu.com"+auth.xpath('@href').extract()[0]
            yield Request(url,callback=self.parse_item)
    def parse_item(self,response):
        selector = Selector(response)
        Id = selector.xpath('//div[@class="main-top"]/a/@href').extract()[0].lstrip("/u/")
        src = "https://www.jianshu.com" +selector.xpath('//div[@class="main-top"]/a/@href').extract()[0]
        img = "http:"+selector.xpath('//div[@class="main-top"]/a/img/@src').extract()[0]
        username = selector.xpath('//div[@class="title"]/a[@class="name"]/text()').extract()[0]
        sex = selector.xpath('//div[@class="title"]/i/@class').extract()
        profiles = selector.xpath('//div[@class="js-intro"]/text()').extract()
        if profiles :
            profile =profiles[0]
        else :
            profile = ''
        if sex :
            if sex[0] == 'iconfont ic-man':
                sex = 1
            elif sex[0] == 'iconfont ic-woman':
                sex = 2
        else :
            sex = 0
        infos = selector.xpath('//div[@class="info"]/ul/li/div//p/text()')
        attention = infos.extract()[0]
        fans = infos.extract()[1]
        article = infos.extract()[2]
        words_num = infos.extract()[3]
        like_num = infos.extract()[4]
        item =  AuthorItem()
        item['Id'] = Id
        item['Profile'] = profile
        item['Username'] = username
        item['Src'] = src
        item['Img'] = img
        item['Sex'] = sex
        item['Attention'] = attention
        item['Fans'] = fans
        item['Article'] = article
        item['WordNum'] = words_num
        item['LikeNum'] = like_num
        yield item