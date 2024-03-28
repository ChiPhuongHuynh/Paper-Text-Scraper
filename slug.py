from bs4 import BeautifulSoup
import requests
import re
import csv
from tqdm import tqdm

url = "https://paperswithcode.com/sota/image-classification-on-imagenet"

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html5lib')

body = soup.find("body")

body = body.find(attrs={'class':'container content content-buffer'})
#f = open("./text/sample.txt", "w", encoding="utf-8")

"""
cur = body.find("script", id="evaluation-chart-data")
cur_string = str(cur)
cur_string = cur_string[(cur_string.find("\"dataPoints\"") + len("\"dataPoints\"")+3):]
t = cur_string.find("},") + 3
datapoints = cur_string.split("},")
"""
def scrapeurl_2(link):
    if link == "ul": return "Null"
    body = "https://paperswithcode.com"
    url = body+link
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')

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
    return link[0]


eval = str(body.find("script", id="evaluation-table-data"))

def eval_scrape(datatable):
    eval = datatable[(datatable.find("{")) + 1:]
    sample = eval.split("{\"table_id\"")
    rows = []
    for s in tqdm(sample):
        #s = sample[1]
        s = s.split("\"tags\"")
        data = s[0].split(", \"")
        #for i in range(len(data)): print(str(i) + " " + data[i] + "\n")
        tag = s[1].split("}, {")
        name = data[3].split(": ")[1][1:-1]
        params = data[17].split(": ")[1]
        accuracy = (data[16].split(": ")[2])
        hardware_req = (data[19].split(": ")[1])
        url = data[28].split(": ")[1][1:-2]
        #print(url)
        #arxiv = None
        try: arxiv = scrapeurl_2(url)
        except: arxiv = None
        tags = []
        for i in tag:
            tags.append(i.split(", ")[1].split(": ")[1][1:-1])
        rows.append([name, accuracy, params, hardware_req, tags, arxiv])
    return rows
#url = "/paper/omnivec-learning-robust-representations-with/review/?hl=112988"
efields = ["name", "accuracy", "params", "hardware_req","tags", "id"]
erows = eval_scrape(eval)
with open("table2_url.csv",'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter='|')
    csvwriter.writerow(efields)
    csvwriter.writerows(erows)
    csvfile.close()
