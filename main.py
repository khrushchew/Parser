from functions import check_hrefs
import requests
from bs4 import BeautifulSoup
import json
import csv

url = 'https://calorizator.ru/product'

headers = {"Accept": "text/css,*/*;q=0.1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                                                         "Chrome/121.0.0.0 Safari/537.36"}

req = requests.get(url, headers=headers)

src = req.text

with open("index.html", "w", encoding="utf-8-sig") as file:
    file.write(src)

with open("index.html", "r", encoding="utf-8-sig") as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")

all_products_hrefs = soup.find_all("li")

all_categories_dict = {}

for item in all_products_hrefs:
    if len(item.get("class")) == 1 and set(item.get("class")[0]) & set("prod") == set("prod"):
        for a in item:
            item_text = a.text
            if check_hrefs(a.get("href")):
                item_href = "https://calorizator.ru/" + a.get("href")
                all_categories_dict[a.text] = item_href

with open("all_categories_dict.json", "w") as file:
    json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

with open("all_categories_dict.json", "r") as file:
    all_categories = json.load(file)

result = []
count = 0

for category_name, category_href in all_categories.items():

    del_list = ["'", '"', ".", ",", " "]
    for i in del_list:
        if i in category_name:
            category_name = category_name.replace(i, "_")
    req = requests.get(url=category_href, headers=headers)
    src = req.text
    with open(f"data/{count}_{category_name}.html", "w", encoding="utf-8-sig") as file:
        file.write(src)
    with open(f"data/{count}_{category_name}.html", "r", encoding="utf-8-sig") as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    table_head = soup.find("tr").find_all("a")
    title = ";".join([i.text for i in table_head])
    with open(f"data/{count}_{category_name}.csv", "w", encoding="utf-8-sig") as file:
        file.write(title + '\n')
    product_data = soup.find("tbody").find_all("tr")
    for i in product_data:
        products_tds = i.find_all("td")
        title = products_tds[1].find("a").text.strip()
        proteins = products_tds[2].text.strip()
        fats = products_tds[3].text.strip()
        carbohydrates = products_tds[4].text.strip()
        calories = products_tds[5].text.strip()
        result.append(
            {
                "Title": title,
                "Proteins": proteins,
                "Fats": fats,
                "Carbohydrates": carbohydrates,
                "Calories": calories
            }
        )
        with open(f"data/{count}_{category_name}.csv", "a", encoding="utf-8-sig") as file:
            writer = csv.writer(file, delimiter=';', lineterminator='\n')
            writer.writerow(
                (
                    title,
                    proteins,
                    fats,
                    carbohydrates,
                    calories
                )
            )
        with open(f"data/{count}_{category_name}.json", "w", encoding="utf-8-sig") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)

    count += 1
