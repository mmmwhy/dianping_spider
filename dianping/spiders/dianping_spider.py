# coding=utf-8
import scrapy
from ..items import DianpingItem

class DianpingSpider(scrapy.spiders.Spider):
    name = "dianping"
    allowed_domains = ["dianping.com"]

    # 大概思路
    # 1、1000家上海餐厅
    # 2、获取餐厅ID
    # 3、dianping/shop/id 获取经纬度
    # 4、dianping/shop/id/review_all 抓取用户ID以及用户评分
    # 5、信任度由皮尔逊系数计算获得

    def start_requests(self):

        location = ['r5', 'r2', 'r6', 'r1', 'r3', 'r4', 'r12', 'r10', 'r7', 'r9', 'r13', 'r8', 'r5937', 'r5938',
                    'r5939', 'r8846', 'r8847', 'c3580', 'r801', 'r802', 'r804', 'r865', 'r860', 'r803', 'r835', 'r812',
                    'r842', 'r846', 'r849', 'r806', 'r808', 'r811', 'r839', 'r854']
        foodtype = ['g101', 'g113', 'g132', 'g112', 'g117', 'g110', 'g116', 'g111', 'g103', 'g114', 'g508', 'g102',
                    'g115', 'g109', 'g106', 'g104', 'g248', 'g3243', 'g251', 'g26481', 'g203', 'g107', 'g105', 'g108',
                    'g215', 'g247', 'g1338', 'g1783', 'g118']
        for lbs in location:
            for ft in foodtype:
                for i in range(1, 50):
                    url = 'http://www.dianping.com/shanghai/ch10/%s%sp%s' % (lbs, ft, i)
                    yield scrapy.Request(url=url, callback=self.parse_list_first)

    def parse_list_first(self, response):
        # 此时获得的是所有的shop链接
        shop_all = response.xpath('//*[@class="txt"]/div[@class="tit"]//a[contains(@href,"shop") and \
                                 not(contains(@href,"#"))]/@href').extract()
        for url in shop_all:
            yield scrapy.Request(url=url, callback=self.shop_loc)

    def shop_loc(self, response):
        try:
            postion = response.xpath('//script').extract()
            postion = str(postion).split('shopGlat')[1].split(('cityGlat'))[0].split(('\"'))
            postion = postion[1]+' '+postion[3]
            shopid = response.url.split("/")[-1]
            with open('shopdata', "a") as f:
                f.write(shopid+" "+postion + '\n')

        except IndexError:
            print('IndexError')
        print(response)
        url = response.url+'/review_all'
        yield scrapy.Request(url=url, callback=self.shop_review_all)

    def shop_review_all(self, response): # 获取页面整体数据
        try:
            shop_review_num = int(response.xpath("//a[@class='PageLink'][9]/@title").extract()[0])
        except IndexError:
            shop_review_num = 5
            print('shop_review_num_IndexError')

        for i in range(1, shop_review_num):
            url = response.url + ('/p%s' %i)
            yield scrapy.Request(url=url, callback=self.shop_review_data)

    def shop_review_data(self,response):
        for user in (response.xpath("//*[@class=\"review-rank\" or @class=\"name\"]")):
            rating = user.xpath("//span[contains(@class,\"star\") and not(contains(@class,\"user\"))]").extract()
            #评分在第倒数16位
            rating = [i[-16] for i in rating]
            userid = user.xpath("//*[contains(@href,\"member\") and \
                                not(contains(@href,\"photos\"))]//@href").extract()[1:]
            userid = [i.split("/")[-1] for i in userid][::2]
            shopid = response.url.split("/")[-3]

            for i in range(len(userid)):
                with open('ratingdata', "a") as f:
                    f.write(userid[i]+" "+shopid +" "+ rating[i]+'\n')





