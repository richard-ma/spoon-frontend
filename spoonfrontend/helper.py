def get_one_column(column, s):
    return [item[column] for item in s]


if __name__ == "__main__":
    from datetime import date
    from settings import *
    from spoonfrontend.database import *
    collection_name = 'top_summary'
    client = Database.get_database_from_factory('mongodb')
    client.connect(MONGO_URI, MONGO_DATABASE).set_collection(collection_name)

    column = 'last_update'
    items = get_one_column('summary', client.get_date(column, date(2021, 3, 23)))
    print(items)
