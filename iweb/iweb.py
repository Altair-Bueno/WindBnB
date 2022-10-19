from pymongo import MongoClient
from json import load

__MONGO_URL__ = 'mongodb://root:example@localhost:27017'
__MONGO_DATABASE__ = 'iweb'
__MONGO_COLLECTION__ = 'houses'

__DATABASE_JSON__ = "houses.json"

def main():
    client = MongoClient(__MONGO_URL__)
    db = client[__MONGO_DATABASE__]
    collection = db[__MONGO_COLLECTION__]

    with open(__DATABASE_JSON__) as contents:
        iweb_dict = load(contents)

    result = collection.insert_many(iweb_dict)
    
    print(f'{result.inserted_ids=}')

if __name__ == '__main__':
    main()
