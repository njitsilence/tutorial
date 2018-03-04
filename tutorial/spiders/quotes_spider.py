import scrapy
from scrapy import Request,FormRequest
from scrapy.selector import Selector
import logging
import os,json
from tutorial.items import PeopleItem,MyImageItem

class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    start_url = "https://www.zhihu.com/people/wang-qiang-34-34"
    # start_url = "https://www.zhihu.com/org/teng-xun-ke-ji"
    base_url =  "https://www.zhihu.com/"
    counter = 0

    def __init__(self):
        self.xrsf = ""
        self.current_zhihuid = ""

    def start_requests(self):
        return [Request("https://www.zhihu.com/#signin",
                        meta={"cookiejar":1},
                        callback=self.post_login)]

    def post_login(self,response):
        # self.xsrf = Selector(response).xpath("//input[@name='_xsrf']/@value").extract()[0]
        return [FormRequest(
            "https://www.zhihu.com/login/email",
            method="POST",
            meta={"cookiejar":response.meta["cookiejar"]},
            formdata={
                # "_xsrf":self.xsrf,
                "phoneNo":"15680098186",
                "password":"jj891030",
                "remeber_me":"true"
            },
            callback=self.after_login
        )]

    def after_login(self,response):
        return [Request(
            self.start_url,
            meta={"cookiejar": response.meta["cookiejar"]},
            callback=self.parse_people,
            errback=self.parse_err
        )]

    def parse_people(self,response):
        self.counter+=1
        logging.info("hom many times come to parse_people %i times" % self.counter )
        selector = Selector(response)

        nickname = selector.xpath("//h1[@class='ProfileHeader-title']/span[@class='ProfileHeader-name']/text()").extract_first()
        zhihuid = os.path.split(response.url)[-1]
        self.current_zhihuid = zhihuid
        # logging.info(self.current_zhihuid)
        busniess = selector.xpath("//div[@class='ProfileHeader-infoItem']/text()").extract_first()
        img_url = selector.xpath("//div[@class='UserAvatar ProfileHeader-avatar']/img/@src").extract_first()
        gender = ""
        gender_male_icon = selector.response.xpath("//svg[@class='Icon Icon--male']").extract_first()
        gender_female_icon = selector.response.xpath("//svg[@class='Icon Icon--female']").extract_first()
        if gender_male_icon is not None:
            gender = "male"
        if gender_female_icon is not None:
            gender = "female"

        try:
            following_count,follower_count = selector.xpath("//div[@class='NumberBoard FollowshipCard-counts NumberBoard--divider']/a/div/strong/text()").extract()
            following_count, follower_count = int(following_count.replace(",","")),int(follower_count.replace(",",""))
        except ValueError:
            pass

        following_url = self.start_url + '/following'
        # following_url = self.start_url + '/followers'

        # response_for_following = Request(following_url,
        #                     meta={"cookiejar": response.meta["cookiejar"]},
        # )

        # yield Request(following_url,
        #               meta={"cookiejar":response.meta["cookiejar"]},
        #               callback=self.parse_following,
        #               errback=self.parse_err,
        #               dont_filter=True,
        # )

        # item = PeopleItem(
        #     nickname = nickname,
        #     zhihuid = zhihuid,
        #     busniess = busniess,
        #     img_url = img_url,
        #     gender = gender,
        #     following_count = following_count,
        #     follower_count = follower_count,
        #     # following_url =  following_url,
        # )
        # yield item

        item = MyImageItem(
            image_urls=[img_url],
            # image_paths=["full/wangqiang.jpg"]
        )
        yield item

    def parse_following(self, response):
        selector = Selector(response)
        # following_details = selector.xpath("//div[@class='ContentItem-image']/span/div/div/a/@href").extract()
        # data_state = selector.xpath("//div[@id='data']/@data-state").extract()
        # ids = json.loads(data_state[0])["people"]["followingByUser"][self.current_zhihuid]["ids"]
        pagination = selector.xpath("//div[@class='Pagination']/button/text()").extract()
        totoal_page = int(pagination[-2])
        # logging.info("type",type(totoal_page))
        for i in range(totoal_page):
            page = str(i+1)
            following_url = self.base_url + "people/" + self.current_zhihuid + "/following?page=" + page
            # following_url = self.base_url + "people/" + self.current_zhihuid + "/followers?page=" + page
            # logging.info(following_url)
            yield Request(following_url,
                          meta={"cookiejar": response.meta["cookiejar"]},
                          callback=self.get_following_url,
                          errback=self.parse_err,
                          # dont_filter=True,
                          )

    def get_following_url(self,response):
        selector = Selector(response)
        data_state = selector.xpath("//div[@id='data']/@data-state").extract()
        ids = []
        try:
            ids = json.loads(data_state[0])["people"]["followingByUser"][self.current_zhihuid]["ids"]
        except KeyError:
                pass
        # ids = json.loads(data_state[0])["people"]["followersByUser"][self.current_zhihuid]["ids"]

        for user_id in ids:
            if user_id:
                following_url_home = self.base_url + "people/" + user_id
                logging.info(following_url_home)
                yield Request(following_url_home,
                              meta={"cookiejar": response.meta["cookiejar"]},
                              callback=self.parse_people,
                              # errback=self.parse_err,
                              # dont_filter=True,
                              )


    def parse_err(self,response):
        logging.info(response.body)
        # logging.ERROR('crawl {} failed'.format(response.url))
