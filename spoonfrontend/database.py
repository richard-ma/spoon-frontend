import pymongo
from datetime import *


class Database():
    @staticmethod
    def get_database_from_factory(database_type):
        if database_type == 'mongodb':
            return DatabaseMongodb()

    def __init__(self):
        pass

    def connect(self):
        pass

    def close(self):
        pass


class DatabaseMongodb(Database):
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None

    def connect(self, uri, db_name, collection_name=None):
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[db_name]

        if collection_name is not None:
            self.collection = self.db[collection_name]

        return self

    def close(self):
        self.client.close()

    def get_db(self):
        if self.db is not None:
            return self.db
        else:
            raise Exception("Database is None")

    def set_db(self, db_name):
        self.db = self.client[db_name]

        return self

    def get_collection(self):
        if self.collection is not None:
            return self.collection
        else:
            raise Exception("Collection is None")

    def set_collection(self, collection_name):
        self.collection = self.db[collection_name]

        return self

    # db.top_summary.find({$and: [
    #     {last_update: {$gte: ISODate("2021-03-19T00:00:00.000Z")}},
    #     {last_update: {$lt: ISODate("2021-03-20T23:59:59.999Z")}}
    # ]}).pretty()
    def get_duration(self, column, start, duration):
        return list(self.collection.find({'$and': [
            {column: {'$gte': start}},
            {column: {'$lt': start + duration}},
        ]}))

    def get_date(self, column, date):
        start = datetime.combine(date, time(0, 0, 0, 0))
        duration = timedelta(days=1)
        return self.get_duration(column, start, duration)

    def get_yestoday(self, column):
        yestoday = date.today() - timedelta(days=1)
        return self.get_date(column, yestoday)

    def get_latest(self, column, days=0, hours=0):
        start = datetime.now() - timedelta(days=days, hours=hours)
        return self.get_duration(column, start, timedelta(days=days, hours=hours))

    def get_latest_24_hours(self, column):
        return self.get_latest(column, hours=24)


if __name__ == '__main__':
    from settings import *
    collection_name = 'top_summary'
    client = Database.get_database_from_factory('mongodb')
    client.connect(MONGO_URI, MONGO_DATABASE).set_collection(collection_name)

    # items = db['top_summary'].find({'last_update': {'$gt': datetime.datetime(2021, 3, 19)}})
    column = 'last_update'
    items = client.get_yestoday(column)
    print(len(items))
