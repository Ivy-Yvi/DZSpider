import scrapy
import tools, config
from ..items import FirstItem

db = tools.MyMongoDB()


class DianpingSpider(scrapy.Spider):
    name = "dianping"
    allowed_domains = ["dianping.com"]
    start_urls = ["https://dianping.com"]

    def start_requests(self):
        allUrls = tools.create_urls()

        for keyword, urls in allUrls.items():
            for url in urls:
                # print(url)
                yield scrapy.Request(
                    url=url,
                    method="get",
                    headers={
                        "Host": "www.dianping.com",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                    },
                    cookies=tools.create_cookies(config.cookie),
                    dont_filter=True,
                    callback=self.parse,
                    meta={"searchKeyword": keyword},
                )
                # break
            # break

    def parse(self, response):
        """div@id: shop-all-list"""
        # searchKeyword
        searchKeyword = response.meta.get("searchKeyword")

        # 提取 li 标签
        lis = response.xpath("//div[@id='shop-all-list']/ul/li")

        for li in lis:  # 遍历 li 标签列表
            # 提取店铺 id
            dataShopId = li.xpath("//div[@id='shop-all-list']/ul/li/div[@class='pic']/a/@data-shopid").get()

            """增量式逻辑: 判断店铺的id 是否在数据库中, 如果在就跳过本次解析"""
            isExist = db.findData(id=dataShopId)
            if isExist:
                continue

            # 提取店铺名
            shopName = li.xpath("div[@class='txt']/div[@class='tit']/a/@title").get()

            # 提取店铺星级
            star = li.xpath("div[@class='txt']/div[@class='comment']/div[@class='nebula_star']/div[@class='star_icon']/span/@class").get()
            star = star.split(" ")[1].split("_")[-1]
            star = int(star) // 10

            # 提取店铺评论数量
            commentNumber = li.xpath("div[@class='txt']/div[@class='comment']/a[@class='review-num']/b//text()").get()

            # 提取人均价格
            avgPrice = li.xpath("div[@class='txt']/div[@class='comment']/a[@class='mean-price']/b//text()").get()
            if (isinstance(avgPrice, str)):
                avgPrice = avgPrice.replace("￥", "")

            # 提取店铺类型
            shop = li.xpath("div[@class='txt']/div[@class='tag-addr']/a/span//text()").extract()
            shopType = shop[0]

            # 提取店铺地址
            shopAddress = shop[1]

            # 提取团购信息
            groupBuyContent = li.xpath("div[@class='svr-info']/div/a//text()").extract()

            isGroupBuy = "否"
            if groupBuyContent:
                isGroupBuy = "是"
                groupBuyContent = "".join(groupBuyContent)
                groupBuyContent = groupBuyContent.replace("\n", "").replace(" ", "")

            else:
                groupBuyContent = ""

            # 提取店铺图片链接
            picLink = li.xpath("div[@class='pic']/a/img/@src").get()

            item = FirstItem()
            item["shopName"] = shopName
            item["star"] = star
            item["commentNumber"] = commentNumber
            item["avgPrice"] = avgPrice
            item["shopType"] = shopType
            item["shopAddress"] = shopAddress
            item["isGroupBuy"] = isGroupBuy
            item["groupBuyContent"] = groupBuyContent
            item["dataShopId"] = dataShopId
            item["searchKeyword"] = searchKeyword
            item["picLink"] = picLink
            yield item
