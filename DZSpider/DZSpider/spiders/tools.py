import os
from urllib.parse import quote
import pymongo
from typing import Union, Optional

from scrapy.utils.project import get_project_settings

# 获取 settings 文件的对象
settings = get_project_settings()



class MyMongoDB():
    def __init__(self):
        # 链接数据库
        client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        self.db = client[settings['MONGO_DB']]  # 获得数据库的句柄
        self.table = self.db[settings['MONGO_COLL']]  # 获得collection的句柄

    def findData(self, id: str=None)->Optional[bool]:
        assert id is not None
        result = self.table.find_one({"dataShopId": id})
        if result:
            return True
        return False
    @property
    def size(self):
        result = self.table.find()
        return len(list(result))


def create_urls():
    """生成 urls"""
    urls = {}
    path = os.getcwd() + "\keywords.txt"
    keywords = open(path, encoding="utf-8").readlines()
    keywords = [i.replace("\n", "") for i in keywords]

    for keyword in keywords:
        urls[keyword] = []
        for page in range(1, 50):
            url = f"https://www.dianping.com/search/keyword/6/0_{quote(keyword)}/p{page}"
            urls[keyword].append(url)
    return urls

def create_cookies(cookie: str) -> dict:
    cookies = cookie.split(";")
    cookies = [i.split("=") for i in cookies]
    cookies = {i[0].strip():i[1].strip() for i in cookies}
    return cookies


def main():
    # urls = create_urls()
    import config
    create_cookies(config.cookie)

# main()

