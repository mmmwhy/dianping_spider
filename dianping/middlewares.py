# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class DianpingSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

from fake_useragent import UserAgent


class RandomUserAgentMiddleware(object):
    """
    随机更换User-Agent
    """

    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)

        request.headers.setdefault('User-Agent', get_ua())


from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.chrome.options import Options


class JSPageMiddleware(object):

    def __init__(self):
        # 不过每次都要看着浏览器执行这些操作, 有时候有点不方便
        # 我们可以让 selenium 不弹出浏览器窗口, 让它”安静”地执行操作.
        # 在创建 driver 之前定义几个参数就能摆脱浏览器的身体了.
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # define headless
        prefs = {
            'profile.default_content_setting_values': {
                'images': 2
            }
        }
        chrome_options.add_experimental_option('prefs', prefs)

        self.browser = webdriver.Chrome(
                executable_path='E:/Python/chromedriver.exe', chrome_options=chrome_options)

        super(JSPageMiddleware, self).__init__()

    # 通过chrome请求动态网页，代替scrapy的downloader
    def process_request(self, request, spider):
        self.browser.get(request.url)
        import time
        # 别太快
        time.sleep(1)
        # 直接返回给spider，而非再传给downloader
        return HtmlResponse(url=self.browser.current_url, body=self.browser.page_source, encoding="utf-8",
                            request=request)
