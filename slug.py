from bs4 import BeautifulSoup
import requests
import re
import csv

body = "https://paperswithcode.com/paper/"
slug = "going-deeper-with-image-transformers/review/?hl=29203"

url = body+slug

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html5lib')

f = open("./text/table2.txt", "w", encoding="utf-8")


cur = soup.find('body')

cur = cur.find(attrs={'class':'container content content-buffer'})
cur = cur.find('form')
cur = cur.find(attrs={'class':'container-fluid content review-content'})
cur = cur.find(attrs={'class':'extracted-table'})
cur = cur.find(attrs={'class':'row'})
cur = cur.find(attrs={'class':'col-md-6 from-paper'})
cur = cur.find(attrs={'class':'container paper-extracts'})

cur = cur.find(attrs={'class':'paper-pdf-link'})
link = cur.find('a')['href'].split("https://arxiv.org/pdf/")
link = link[1].split(".pdf")
print(link[0])

f.write(cur.prettify())

#print(cur.find('a')['href'])