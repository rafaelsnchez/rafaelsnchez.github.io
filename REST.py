#!/usr/bin/python
import json
from bson import json_util
from bson.json_util import dumps
import bottle
from bottle import route, run, get, request, abort

from pymongo import MongoClient

connection = MongoClient('localhost', 27017)

# database and collection
db = connection['market']
collection = db['stocks']
collectionComp = db['company']


# setup URI paths for REST service
@route('/createStock/<ticker>', method='POST')
def createStock(ticker):
    createData = request.json
    createData.update({'Ticker': ticker})  # Ticker key and value
    print(createData)

    for item in createData:
        print(createData[item])

    createdRecord = collection.insert(createData)  # insert data to collection
    newDoc = collection.find_one({"_id": createdRecord})  # new ticker symbol

    return "Created Document " + dumps(newDoc)
    # return json.loads(json.dumps(string, indent=4, default=json_util.default))


@route('/getStock/<ticker>', method='GET')
def get_data(ticker):
    readDoc = collection.find({"Ticker": ticker})

    return "Document Found " + dumps(readDoc)


@route('/updateStock/<ticker>', method='PUT')
def createStock(ticker):
    updateData = request.json
    print(updateData)
    query = {'Ticker': ticker}  # Ticker query
    for item in updateData:
        print(updateData[item])
        updateRecord = {"$set": {item: updateData[item]}}
        collection.update(query, updateRecord)

    updatedDoc = collection.find({"Ticker": ticker})  # finds all updates
    result = dumps(updatedDoc)
    return "Updated Document " + str(result)
    # return json.loads(json.dumps(string, indent=4, default=json_util.default))


@route('/deleteStock/<ticker>', method='GET')
def get_update(ticker):
    query = {"Ticker": ticker}
    print(query)

    result = collection.delete_many(query)
    return "Document Deleted " + ticker


def createDocumentsReport(tickerName):
    pass


@route('/stockReport/', method='POST')
def run_create():
    data = request.json
    reports = []

    for item in data:
        tickerList = data[item]
        tickerArray = tickerList.split(",")

        for tickerName in tickerArray:
            pulledReport = createDocumentsReport(tickerName)
            reports.append("Stock Report " + tickerName + " \n" + pulledReport)
            return reports


class CreatePortfolio(object):
    pass


@route('/portfolio/', method='POST')
def run_create():
    data = request.json
    for item in data:
        industry = data[item]

    result = CreatePortfolio(industry)
    return "Industries " + industry + " \n " + result


if __name__ == '__main__':
    # app.run(debug=True)
    run(host='localhost', port=8080)


