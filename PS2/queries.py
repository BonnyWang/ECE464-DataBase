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
    return collection.find(myquery).count();

def total():
    return collection.count_documents({});

# TODO: Use Aggregate pipeline


if __name__ == "__main__":
    print("Total number of books in the database:");
    print(total());
    # print("Books have 4 star rating:");
    books4Star = findWithRating("Four");
    for b in books4Star:
        print(b['title']);

