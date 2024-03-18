# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FirstItem(scrapy.Item):
    """第一层网页的存储数据结构"""
    # 店铺名
    shopName = scrapy.Field()

    # 星级
    star = scrapy.Field()

    # 评价数量
    commentNumber = scrapy.Field()

    # 人均价格
    avgPrice = scrapy.Field()

    # 店铺类型 烤肉店/火锅店/自助餐店铺
    shopType = scrapy.Field()

    # 店铺地址
    shopAddress = scrapy.Field()

    # 此店铺是否有团购套餐
    isGroupBuy = scrapy.Field()

    # 团购内容, 如果没有团购套餐, 此项为空
    groupBuyContent = scrapy.Field()

    # 店铺 id
    dataShopId = scrapy.Field()

    # 搜索关键词
    searchKeyword = scrapy.Field()

    # 店铺图片链接
    picLink = scrapy.Field()