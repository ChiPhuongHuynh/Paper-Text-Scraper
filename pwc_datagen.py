from bs4 import BeautifulSoup
import requests
import re
import csv
from tqdm import tqdm

#prepare the state of the art leaderboard website data for specific task
def sota_dt_prep(slug):
    link_body = "https://paperswithcode.com/sota"
    url = link_body + slug
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')

    body = soup.find("body")
    body = body.find(attrs={'class': 'container content content-buffer'})
    cur = body.find("script", id="evaluation-chart-data")
    cur_string = str(cur)
    cur_string = cur_string[(cur_string.find("\"dataPoints\"") + len("\"dataPoints\"") + 3):]
    table1 = cur_string.split("},")
    table2 = str(body.find("script", id="evaluation-table-data"))

    return table1, table2

def scrapeurl_slug(slug):
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
    out = cur.find('a')['href'].split("https://arxiv.org/pdf/")
    out = out[1].split(".pdf")
    return out[0]

#get the arxiv reference number from the review number for the data
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

#scrape the first table from this site
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
            try: paper = scrapeurl_slug(slug)
            except: paper = None
            rows.append([name, year, accuracy, paper])
            #print([name, year, accuracy, paper])
        except: pass
    return rows

#scrape the second table from this site
def eval_scrape(datatable):
    eval = datatable[(datatable.find("{")) + 1:]
    sample = eval.split("{\"table_id\"")
    rows = []
    for s in tqdm(sample):
        s = s.split("\"tags\"")
        data = s[0].split(", \"")
        tag = s[1].split("}, {")
        name = data[3].split(": ")[1][1:-1]
        params = data[17].split(": ")[1]
        accuracy = (data[16].split(": ")[2])
        hardware_req = (data[19].split(": ")[1])
        url = data[28].split(": ")[1][1:-2]
        try: arxiv = scrapeurl_2(url)
        except: arxiv = None
        tags = []
        for i in tag:
            tags.append(i.split(", ")[1].split(": ")[1][1:-1])
        rows.append([name, accuracy, params, hardware_req, tags, arxiv])
    return rows

def sota_pipeline(slug):
    table1, table2 = sota_dt_prep(slug)
    e_fields = ["name", "accuracy", "params", "hardware_req","tags", "id"]
    a_fields = ["name", "year", "accuracy", "paper", "id"]
    e_row = eval_scrape(table2)
    a_row = accuracy_scrape(table1)
    with open("table1.csv", 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='|')
        csvwriter.writerow(e_fields)
        csvwriter.writerows(e_row)
        csvfile.close()

    with open("table2.csv", 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='|')
        csvwriter.writerow(a_fields)
        csvwriter.writerows(a_row)
        csvfile.close()