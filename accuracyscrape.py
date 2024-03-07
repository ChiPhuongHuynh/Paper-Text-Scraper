from bs4 import BeautifulSoup
import requests
import re
import json
import csv
from tqdm import tqdm

url = "https://paperswithcode.com/sota/image-classification-on-imagenet"

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html5lib')

body = soup.find("body")

body = body.find(attrs={'class':'container content content-buffer'})
f = open("./text/paperswithcode.txt", "w", encoding="utf-8")

f.write(soup.prettify())

def scrapeurl(slug):
    body = "https://paperswithcode.com/paper/"
    url = body + slug

    r = requests.get(url)
    s = BeautifulSoup(r.content, 'html5lib')

    cur = s.find('body')
    cur = cur.find(attrs={'class': 'container content content-buffer'})
    cur = cur.find('main')
    cur = cur.find(attrs={'class': 'paper-abstract'})
    cur = cur.find(attrs={'class': 'row'})
    cur = cur.find(attrs={'class': 'col-md-12'})
    out = cur.find('a')['href']
    return out

cur = body.find("script", id="evaluation-chart-data")
cur_string = str(cur)
cur_string = cur_string[(cur_string.find("\"dataPoints\"") + len("\"dataPoints\"")+3):]
t = cur_string.find("},") + 3
datapoints = cur_string.split("},")
slug = (datapoints[0].split(", ")[5].split(": ")[1])[1:-1]
print(scrapeurl(slug))

afields = ["name", "year", "accuracy", "paper"]

def accuracy_scrape(datatable):
    rows = []
    for dt in tqdm(datatable):
        dt0 = dt.split(", ")
        try:
            year = (dt0[0].split(": ")[1])[1:5]
            accuracy = (dt0[1].split(": ")[1])
            name = (dt0[2].split(": ")[1])[1:-1]
            #paper = (dt0[5].split(": ")[1])[1:-1]
            slug = (dt0[5].split(": ")[1])[1:-1]
            paper = scrapeurl(slug)
            rows.append([name, year, accuracy, paper])
            #print([name, year, accuracy, paper])
        except: pass
    return rows
arows = accuracy_scrape(datapoints)
with open("table1.csv",'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter='|')
    csvwriter.writerow(afields)
    csvwriter.writerows(arows)
    csvfile.close()

eval = str(body.find("script", id="evaluation-table-data"))
"""
eval = eval[(eval.find("{"))+1:]
sample = eval.split("{\"table_id\"")
s = sample[1].split("\"tags\"")
data = s[0].split(", \"")
tag = s[1].split("}, {")

print(s[0][0:100])
for i in range(len(data)):
    #print(data[i])
    print(str(i) + " " + data[i].split(": ")[1])
print(data[17].split(": ")[2])
for i in tag:
   print(i.split(", ")[1].split(": ")[1])
"""

efields = ["name", "accuracy", "params", "hardware_req","tags"]
def eval_scrape(datatable):
    eval = datatable[(datatable.find("{")) + 1:]
    sample = eval.split("{\"table_id\"")
    rows = []
    for s in sample:
        s = s.split("\"tags\"")
        data = s[0].split(", \"")
        tag = s[1].split("}, {")
        name = data[3].split(": ")[1][1:-1]
        params = data[18].split(": ")[1]
        accuracy = (data[17].split(": ")[2])
        hardware_req = (data[19].split(": ")[1])
        tags = []
        for i in tag:
            tags.append(i.split(", ")[1].split(": ")[1][1:-1])
        rows.append([name, accuracy, params, hardware_req, tags])
    return rows

erows = eval_scrape(eval)



with open("table2.csv",'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter='|')
    csvwriter.writerow(efields)
    csvwriter.writerows(erows)
    csvfile.close()
