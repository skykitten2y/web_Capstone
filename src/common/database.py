import os

import pymongo

class Database(object):  #get general Database class as well as object you defined below
    #uri = os.environ.get("MONGODB_URI")
    uri = "mongodb://127.0.0.1:27017"
    DATABASE = None
    # with out initialize method, since all database need to access the same uri and database

    @staticmethod  #tell python we are not using self in this method
    def initialize():
        db = pymongo.MongoClient(Database.uri) #access uri through Database class, that's why we called static
        #Database.DATABASE = db.get_default_database()
        Database.DATABASE = db['fullstack']
    @staticmethod
    def insert(collection,data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query) ##not return a cursor, cursor start at begin of the collection and output one by one

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query) #return jason object

    @staticmethod
    def replace_data(collection,search,replacement):
        Database.DATABASE[collection].replace_one(search,replacement)
        #clients = [a for client in collection.find({})] # put client in collection.find({}) to a as a list
        # #we can use if statment: if client['Risklevel'] >100  or access things like a['age']
        #print(a)

    @classmethod
    def extract_prices(cls):
        priceNames = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'BERK', 'JPM', 'JNJ', 'WMT', 'V', 'PG',
                      'XOM', 'BAC', 'MA', 'T', 'HD', 'INTC', 'VZ', 'DIS', 'UNH', 'KO',
                      'CVX', 'WFC', 'MRK', 'CMCSA', 'PFE', 'CSCO', 'BA', 'PEP', 'ORCL', 'C',
                      'MCD', 'ABT', 'NKE', 'MDT', 'ADBE', 'COST', 'PM', 'NVDA', 'UTX', 'HON',
                      'AMGN', 'NFLX', 'IBM', 'UNP', 'TMO', 'CRM', 'ACN', 'NEE', 'AVGO', 'TXN',
                      'LLY', 'RTN', 'LMT', 'SPG', 'SBUX', 'UPS', 'DHR', 'QCOM', 'AXP', 'AMT',
                      'MMM', 'BMY', 'USB', 'MO', 'BKNG', 'LOW', 'CVS', 'GILD', 'FIS', 'SYK',
                      'CAT', 'GE', 'GS', 'MDLZ', 'MS', 'CELG', 'CME', 'TJX', 'BLK', 'ADP',
                      'TMUS', 'DUK', 'EL', 'CB', 'D', 'INTU', 'ANTM', 'BDX', 'CI', 'PNC',
                      'SO', 'ISRG', 'COP', 'SPGI', 'CL', 'CCI', 'PLD', 'AGN', 'BSX', 'CSX']
        prices = []
        for i in range(0, 100):
            get_price = Database.find_one("prices", {"ticker": priceNames[i]})
            prices.append(get_price)
            del prices[i]['_id']

        price_raw_data = {}
        ticker_list = []
        price_list = []
        for k in range(100):
            ticker_list.append(prices[k]['ticker'])
        for k in range(100):
            price_list.append(prices[k]['Prices'])
        for i in range(100):
            price_raw_data[ticker_list[i]] = price_list[i]

        return price_raw_data



    @classmethod
    def extract_factors(cls):
        factorNames = ['MKT','HML','SMB','CMA','RMW']
        factors = []
        for j in range(0, 5):
            get_factor = Database.find_one("factors", {"Factor_Name": factorNames[j]})
            factors.append(get_factor)

        factor_raw_data = {}
        factor_list = []
        value_list = []

        for k in range(100):
            factor_list.append(factors[k]['Factor_Name'])
        for k in range(100):
            value_list.append(factors[k]['Values'])
        for i in range(100):
            factor_raw_data[factor_list[i]] = value_list[i]
        return factor_raw_data