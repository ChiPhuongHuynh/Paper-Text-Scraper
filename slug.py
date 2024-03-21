from bs4 import BeautifulSoup
import requests
import re
import csv

url = "https://paperswithcode.com/sota/image-classification-on-imagenet"

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html5lib')

body = soup.find("body")

body = body.find(attrs={'class':'container content content-buffer'})
f = open("./text/sample.txt", "w", encoding="utf-8")

cur = body.find("script", id="evaluation-chart-data")
cur_string = str(cur)
cur_string = cur_string[(cur_string.find("\"dataPoints\"") + len("\"dataPoints\"")+3):]
t = cur_string.find("},") + 3
datapoints = cur_string.split("},")

eval = str(body.find("script", id="evaluation-table-data"))

f.write(eval)


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