from pymongo import database;
import pymongo;
from pymongo import MongoClient;

client = pymongo.MongoClient("mongodb+srv://Bonny:database@mdatabase.1icis.mongodb.net/mDatabase?retryWrites=true&w=majority")
db = client.test;

collection = db.books;

def findWithRating(rate):
    myquery = { "rating": rate};
    return collection.find(myquery);

def findNumberWithRating(rate):
    myquery = { "rating": rate};
    return collection.count_documents(myquery);

def total():
    return collection.count_documents({});

def checkInstock(name):
    return collection.find({'title':name},{"instock availability":1, "_id":0})

# Use aggregate pipe line to obtain the book with lowest price with 5 stars
def lowestPrice5Star():
    pipeline = [
        {
            "$match": {
                "rating": "Five"
            }
        },
        {
            "$sort": {
                "price": pymongo.ASCENDING
            }
        },
        {
            "$limit": 1
        },
        {
            "$project":{
                'title': 1,
                'price': 1,
                '_id': 0
            }
        }
    ]

    return collection.aggregate(pipeline);


if __name__ == "__main__":
    print("Query Results:");
    
    print("\nTotal number of books in the database:");
    print(total());
    
    print("\n\nBooks have 4 star rating:");
    books4Star = findWithRating("Four");
    for b in books4Star:
        print(b['title']);

    print("\n\nNumber of books with 4-star rating:");
    print(findNumberWithRating("Four"));

    print("\n\nLowest price book with five stars:");
    print(list(lowestPrice5Star()));

    checkName = input("\n\nEnter the book name to check if it is available:");
    print(list(checkInstock(checkName))[0]['instock availability']);

