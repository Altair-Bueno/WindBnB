from pymongo import MongoClient
from json import load
from bson.objectid import ObjectId

__MONGO_URL__ = 'mongodb://root:example@localhost:27017'
__MONGO_DATABASE__ = 'iweb'
__MONGO_COLLECTION__ = 'houses'

__DATABASE_JSON__ = "houses.json"

def transform(v):
    v["_id"] = ObjectId(v["_id"])
    
    return v

def main():
    client = MongoClient(__MONGO_URL__)
    db = client[__MONGO_DATABASE__]
    collection = db[__MONGO_COLLECTION__]

    with open(__DATABASE_JSON__) as contents:
        iweb_dict = load(contents)

    iweb_dict = [
        transform(v)
        for v in iweb_dict
    ]

    result = collection.insert_many(iweb_dict)
    
    print(f'{result.inserted_ids=}')

if __name__ == '__main__':
    main()
