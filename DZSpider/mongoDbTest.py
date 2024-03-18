from pymongo import MongoClient
from typing import Union

class Test():
    def __init__(self, dbName: str, tableName:Union[str, None]=None):
        HOST = "localhost"
        PORT = 27017
        self.client = MongoClient(host=HOST, port=PORT)
        self.db = self.client[dbName]
        # self.tableName = tableName
        # if self.tableName:
        #     self.datas = self.db[self.tableName]

    def getDBs(self)->list:
        """获取数据库名称, 也就是 collections 的名称"""
        dbNames = self.client.list_database_names()
        return dbNames

    def getCollections(self)->list:
        """获取当前数据库下所有的表名"""
        tableNames = self.db.list_collection_names()
        return tableNames

    def addData(self, data: Union[dict, list]=None, tableName: str=None):
        table = self.db[tableName]

        if isinstance(data, dict):
            table.insert_one(data)

        if isinstance(data, list):
            table.insert_many(data)

    def findData(self, tableName: str=None):
        """
        查找数据
        :param tableName: 表名
        :return:
        """
        datas = self.db[tableName]

        # 查找 name 值为 李四的值.
        result = datas.find_one({"name": "张三"})
        print("----------------------------------")
        print("result:")
        print(result)
        print(type(result))
        print("----------------------------------")

        for data in datas.find():
            print(data)

    def updateData(self):
        """改 数据 (更新数据)"""
        table = self.db["Test"]
        table.update_one({"name": "张三"}, {"$set": {"age": 30}})

    def deleteData(self):
        table = self.db["Test"]
        # result = table.delete_one({"name": "张三"})
        # print(result)
        # print(result.deleted_count)  # 输出删除的元素条数


        # 删除所有年龄为 18 的人
        # _list = {"age": 18}
        # table.delete_many(_list)

        # 删除 Test 表
        self.db.drop_collection("Test")


    def createData(self):
        """创建假数据用来测试"""
        """如果没有数据库, 就创建数据库"""
        if "MongoTest" not in self.getDBs():
            mongoTest = self.client["MongoTest"]  # 创建数据库

        """如果数据库中没有对应的测试表, 就创建测试表"""
        if "Test" not in self.getCollections():
            mongoTest.create_collection("Test")     # 建表

def main():
    test = Test(dbName="MongoTest")
    test.createData()
    datas = [
        {"name": "麻生希", "age": 18},
        {"name": "北岛玲", "age": 18},
        {"name": "椎名空", "age": 25},
        {"name": "张三", "age": 25},
    ]
    test.addData(tableName="Test", data={"name": "赵二", "age": 23})
    test.addData(tableName="Test", data=datas)
    # test.addData(tableName="Test",)
    test.findData(tableName="Test")
    test.updateData()

    print("---------------------------------------------")
    test.findData(tableName="Test")
    test.deleteData()


if __name__ == '__main__':
    main()
