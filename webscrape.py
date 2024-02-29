from bs4 import BeautifulSoup
import requests
import re
import csv

url = "https://arxiv.org/abs/1512.03385"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html5lib')

dataset_keywords = ["ImageNet", "COCO", "CIFAR-10"]

f = open("./text/1512.03385.txt", "w", encoding="utf-8")

f.write(soup.prettify())

content = soup.find('div', id='content-inner')

year = content.find(attrs={'class':'dateline'}).text[-5:-1]

title = content.find(attrs={'class':'title mathjax'}).text[6:]
authors = (content.find(attrs={'class':'authors'}).text[8:]).split(", ")

abstract = (content.find(attrs={'class':'abstract mathjax'})).text

metadata = (content.find(attrs={'summary':'Additional metadata'}))
task = (metadata.find(attrs={'class':'primary-subject'})).text[-6:-1]

for s in abstract.split(". "):
    if ("error" in s):
        rr = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", s)
        print(100 - float(str(rr[0])))

row = [title, authors, year, task]
fields = ["Title", "Authors", "Year", "Task"]
with open("table0.csv",'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter='|')
    csvwriter.writerow(fields)
    csvwriter.writerow(row)
    csvfile.close()
