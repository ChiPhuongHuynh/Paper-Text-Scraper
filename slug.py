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