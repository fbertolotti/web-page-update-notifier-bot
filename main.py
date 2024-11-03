#!/usr/bin/env python3

from bs4 import BeautifulSoup

import os

import requests

import sqlite3

def downloadHtml(url):
    res = requests.get(url)

    html = res.text

    return html

def analyseHtml(filename):
    with open(filename) as fp:

        soup = BeautifulSoup(fp, 'html.parser')

        r = soup.find_all("article", class_="card".split())

        r = soup.find_all("a", class_="presentation-card-link".split())

        r2 = []

        for item in r:
            r2.append((
                item["href"],
                item.find("h2").contents[0],
            ))

        return r2

def getDataFromDb(dbFile):
    con = sqlite3.connect(dbFile)

    cur = con.cursor()

    cur.execute("SELECT href FROM documents")

    data = cur.fetchall() # returns a list of tuples

    data = map(lambda item : item[0], data)

    cur.close()

    return data

def saveHtml(html, filename):
    with open(filename, 'w') as file:
        file.write(html)

def calculateDifference(all, dbData):
    result = []

    for item in all:
        if not item[0] in dbData:
            result.append(item)

    return result

def writeItemsToDatabase(dbFile, data):
    con = sqlite3.connect(dbFile)

    cur = con.cursor()

    cur.executemany("INSERT INTO documents (href, title) VALUES(?, ?)", data)

    con.commit() 

    con.close()

def printDiff(diff):
    for item in diff:
        print(item[0])
        print(item[1])
        print("\n")

def main():
    webPageUrl = os.environ['URL']

    folder = os.path.dirname(os.path.realpath(__file__))

    dbFile = folder + "/database.sqlite"

    filename = folder + "/temp.html"

    html = downloadHtml(webPageUrl)

    saveHtml(html, filename)

    all = analyseHtml(filename)

    os.remove(filename)

    dbData = getDataFromDb(dbFile)

    diff = calculateDifference(all, dbData)

    writeItemsToDatabase(dbFile, diff)

    printDiff(diff)

main()
