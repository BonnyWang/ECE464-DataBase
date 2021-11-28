import grequests;
from pymongo import database;
import pymongo;
from pymongo import MongoClient;
from bs4 import BeautifulSoup;

BATCH_LENGTH = 5;
urls = [];
results = [];

# Setup MongoDB
client = pymongo.MongoClient("mongodb+srv://Bonny:database@mdatabase.1icis.mongodb.net/mDatabase?retryWrites=true&w=majority")
db = client.test;

db.books.create_index( "title", unique=True);

def generateURLs():
    for i in range(1,51):
        urls.append('https://books.toscrape.com/catalogue/page-%(i)s.html' % locals());
        

def scrape():
    global urls;
    while urls:
        batch = urls[:BATCH_LENGTH];
        rs = (grequests.get(url) for url in batch);
        batch_results = grequests.map(rs);

        for result in batch_results:
            processResult(result.content);

        urls = urls[BATCH_LENGTH:]

def processResult(batchResult):
    soup = BeautifulSoup(batchResult,'html.parser');
    links = soup.findAll('article', class_='product_pod');

    for link in links:
        data = {
            'title':link.find_all('h3')[0].a['title'],
            'image-Address':link.find_all('img')[0]['src'],
            'price':link.find_all('div')[1].find_all('p')[0].string.replace("Â£", "£"),
            'rating':link.p['class'][1],
            'instock availability': link.find_all('div')[1].find_all('p')[1].text.strip() 
        }
        # print(data)
        
        # Use upsert to prevent multiple insertion when runing program multiple times 
        db.books.update_one({'title':data['title']}, {"$set" : data}, upsert=True);



if __name__ == "__main__":
    generateURLs();
    scrape();