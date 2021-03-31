import jieba

def count_words(s):
    ret = dict()
    for item in s:
        words = jieba.cut(item)
        for word in words:
            if word in ret.keys():
                ret[word] += 1
            else:
                ret[word] = 1

    return ret


def sorted_words(d):
    return dict(sorted(
        d.items(),
        key=lambda item: item[1],
        reverse=True
    ))


if __name__ == "__main__":
    from datetime import date
    from settings import *
    from spoonfrontend.database import *
    from spoonfrontend.helper import *

    collection_name = 'top_summary'
    client = Database.get_database_from_factory('mongodb')
    client.connect(MONGO_URI, MONGO_DATABASE).set_collection(collection_name)

    column = 'last_update'
    items = get_one_column('summary', client.get_date(column, date(2021, 3, 23)))
    ret = sorted_words(count_words(items))
    print(ret)