from bs4 import BeautifulSoup
import requests
import re
import csv
from tqdm import tqdm

#slug = "/image-classification-on-stl-10"
#slug = "/image-classification-on-svhn"
#slug = "/object-detection-on-coco-minival"
slug = "/3d-part-segmentation-on-shapenet-part"
#slug = "/language-modelling-on-wikitext-103"

def scrapeurl_slug(slug):
    if len(slug) < 5: return "null"
    body = "https://paperswithcode.com"
    url = body + slug
    r = requests.get(url)
    s = BeautifulSoup(r.content, 'html5lib')

    cur = s.find('body')
    cur = cur.find(attrs={'class': 'container content content-buffer'})
    #print(cur)

    cur = cur.find('main')
    cur = cur.find(attrs={'class': 'paper-abstract'})
    cur = cur.find(attrs={'class': 'row'})
    cur = cur.find(attrs={'class': 'col-md-12'})
    out = cur.find('a')['href'].split("https://arxiv.org/pdf/")
    out = out[1].split(".pdf")
    return out[0]
def sota_dt_prep(slug):
    link_body = "https://paperswithcode.com/sota"
    url = link_body + slug
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    f = open("./text/paperswithcode.txt", "w", encoding="utf-8")

    f.write(soup.prettify())
    body = soup.find("body")
    body = body.find(attrs={'class': 'container content content-buffer'})
    cur = body.find("script", id="evaluation-chart-data")
    cur_string = str(cur)
    cur_string = cur_string[(cur_string.find("\"dataPoints\"") + len("\"dataPoints\"") + 3):]
    table1 = cur_string.split("},")
    table2 = str(body.find("script", id="evaluation-table-data"))

    return table1, table2

def eval_scrape(datatable):
    eval = datatable[(datatable.find("{")) + 1:]
    sample = eval.split("{\"table_id\"")
    f = open("./text/sample.txt", "w", encoding="utf-8")

    for i in sample:
        f.write(i)
        f.write("\n")
    rows = []
    s = sample[0]
    #print(s)
    for s in tqdm(sample):
        s = s.split("\"tags\"")
        #print(s[1])
        data = s[0].split(", \"")
        tag = s[1].split("}, {")

        name = "null"
        accuracy = "null"
        params = "null"
        url = "null"
        arxiv = "null"
        for i in range(len(data)):
            if ("method\"" in data[i] and name == "null"):
                name = data[i].split(": ")[1][1:-1]
                #print(name)
            if ("metrics\"" in data[i] and accuracy == "null"):
                accuracy = (data[i].split(": ")[2]).replace("\"","")
                #error = error.replace("%","")
                #try: accuracy = 100.0 - float(error)
                #except: accuracy = "null"
                #print(accuracy)

            if ("url\"" in data[i] and url == "null"):
                url = data[i].split(": ")[1][1:-1]
                try: arxiv = scrapeurl_slug(url)
                except: arxiv = "null"
                #print(id)
                #print(url)d

            if (("params\"" in data[i] or "PARAMS\"" in data[i]) and params == "null"):
                params = data[i].split(": ")[1].replace("\"","")
                params = params.replace("}","")
                #print(params)
        tags = []
        for i in tag:
            tags.append(i.split(", ")[1].split(": ")[1][1:-1])
        rows.append([name, accuracy, params, tags, arxiv])
    return rows

t1, t2 = sota_dt_prep(slug)
fields = ["name", "accuracy", "params","tags", "id"]
rows = eval_scrape(t2)


with open("datatables-unprocessed/3d-part-estimation.csv", 'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter='|')
    csvwriter.writerow(fields)
    csvwriter.writerows(rows)
    csvfile.close()