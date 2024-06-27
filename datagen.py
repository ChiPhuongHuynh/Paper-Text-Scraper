from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import csv
from tqdm import tqdm
import json
#slug = "/image-classification-on-stl-10"
#slug = "/image-classification-on-svhn"
#slug = "/object-detection-on-coco-minival"
#slug = "task/instance-segmentation"
#slug = "/language-modelling-on-wikitext-103"


def link_scrape(slug):
    body = "https://paperswithcode.com/"
    url = body + slug
    r = requests.get(url)
    s = BeautifulSoup(r.text, "html.parser")
    s = s.find("body")
    s = s.find(attrs={"class":"container content content-buffer"})
    s = s.find("main")
    s = s.find(attrs={"class":"row task-content"})

    t = s.find("div", attrs={"class":"artefact-header"})
    t = t.find("h1",attrs={"id":"task-home"})
    task = t.text

    s = s.find("div", attrs={"class":"col-lg-9"})
    s = s.find(attrs={"class":"task-benchmarks"})
    s = s.find("div",attrs={"id":"benchmarks"})
    s = s.find("div",attrs={"class":"sota-table-preview table-responsive"})
    s = s.find("table", attrs={"id": "benchmarksTable"})
    s = s.find("tbody")
    s = s.find_all("tr")

    output = []
    for r in s:
        cur = r.findAll("td")
        link = cur[1].find('a').get("href")
        data = cur[1].find('a').text.strip()
        loss_dt = is_loss(link)
        op = [link, data, task, loss_dt]
        if loss_dt != None: output.append(op)

    return output

def is_loss(slug):
    body = "https://paperswithcode.com"
    url = body + slug
    r = requests.get(url)
    s = BeautifulSoup(r.text, "html.parser")
    s = s.find("body")
    s = s.find(attrs={"class": "container content content-buffer"})

    s = s.find("script", {"id":"evaluation-table-metrics"})
    data = json.loads(s.text)
    if len(data) == 0: return None
    return data[0]['is_loss']

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
    link_body = "https://paperswithcode.com"
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

def process(df, dataset, task, is_loss = False):
    df["Dataset"] = dataset
    df["Task"] = task
    df = df.drop(df[df['accuracy'] == 'null'].index)

    df.loc[df["tags"] == "[']']", "tags"] = "[]"
    df.loc[df["tags"] == "[']}]</script']", "tags"] = "[]"
    df = df[df['accuracy'].notna()]
    df = df[df['id'].notna()]

    if df["accuracy"].dtypes != "std":
        df["accuracy"] = df["accuracy"].apply(str).str[0:5]
        df["accuracy"] = df["accuracy"].apply(str).str.replace("%", "")
        df["accuracy"] = df["accuracy"].apply(str).str.replace("}", "")
        df["accuracy"] = df["accuracy"].apply(str).str.replace("\\", "")
    df['accuracy'] = pd.to_numeric(df['accuracy'], errors='coerce')
    df.dropna(subset=['accuracy'], inplace=True)

    if is_loss:
        df["accuracy_norm"] = (df["accuracy"].max() - df["accuracy"]) / (df["accuracy"].max() - df["accuracy"].min())
        df["accuracy"] = 100 - df["accuracy"]
    else:
        df["accuracy_norm"] = (df["accuracy"] - df["accuracy"].min()) / (df["accuracy"].max() - df["accuracy"].min())

    cols = ['Task', 'Dataset', 'name', 'accuracy', 'accuracy_norm', 'params', 'tags', 'id']
    df = df[cols]
    if df.shape[0] == 1: df['accuracy_norm'] = 1.0
    return df

def normalization_data(df):
    df_cleaned = df.dropna(subset=['accuracy_norm'])
    sample_idx = df_cleaned.groupby(['Task', 'Dataset'])['accuracy_norm'].idxmax()

    sample = df_cleaned.loc[sample_idx]
    
    maxima = sample.groupby(['Task'])['accuracy'].max()
    sample['max'] = sample['Task'].map(maxima)
    minima = sample.groupby(['Task'])['accuracy'].min()
    sample['min'] = sample['Task'].map(minima)
    sample.loc[sample['accuracy'] == sample['max'], 'difficulty'] = 1
    sample.loc[sample['accuracy'] == sample['min'], 'difficulty'] = 0
    sample.loc[(sample['accuracy'] != sample['max']) & (sample['accuracy'] != sample['min']), 'difficulty'] = (sample['accuracy'] - sample['min']) / (sample['max'] -sample['min'])
    print(sample)

    return sample

def pipeline(slug):
    info = link_scrape(slug)
    fields = ["name", "accuracy", "params", "tags", "id"]
    rows = []
    for op in info:
        link = op[0]
        dataset = op[1]
        task = op[2]
        is_loss = op[3]

        t1, t2 = sota_dt_prep(link)
        r = eval_scrape(t2)
        cur = pd.DataFrame(r, columns=fields)
        cur = process(cur, dataset, task, is_loss)
        r = cur.values.tolist()
        rows.extend(r)
    return rows

def main1():
    fields = ["Task", 'Dataset', 'name', 'accuracy', 'accuracy_norm', 'params', 'tags', 'id']

    file = open('link.txt','r')
    links = file.readlines()
    links = [link.strip("\n") for link in links]
    #rows = []
    csvfile = open("task/many.csv", 'a')
    csvwriter = csv.writer(csvfile, delimiter=',')
    csvwriter.writerow(fields)
    for slug in links:
        print("\n" + slug + "\n")
        cur = pipeline(slug)
        csvwriter.writerows(cur)
        #rows.extend(cur)

    #rows = pipeline(slug)

    csvfile.close()

def main2():
    df0 = pd.read_csv("task/task-based.csv",index_col=False)
    cur = normalization_data(df0)
    cur.to_csv("task/normalized.csv", index=False)

main2()