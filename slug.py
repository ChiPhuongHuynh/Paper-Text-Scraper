from bs4 import BeautifulSoup
import requests
import re
import csv

body = "https://paperswithcode.com/paper/"
slug = "unireplknet-a-universal-perception-large"

url = body+slug

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html5lib')

f = open("./text/sample.txt", "w", encoding="utf-8")

cur = soup.find('body')
cur = cur.find(attrs={'class':'container content content-buffer'})
cur = cur.find('main')
cur = cur.find(attrs={'class':'paper-abstract'})
cur = cur.find(attrs={'class':'row'})
cur = cur.find(attrs={'class':'col-md-12'})
f.write(cur.prettify())

print(cur.find('a')['href'])