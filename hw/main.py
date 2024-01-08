import json
import datetime
from random import random
from datetime import timedelta
from wine import Wine
from beer import Beer
from market import Market


def print_drinks_list(date1, date2):
    lst = market.get_drinks_by_production_date(date1, date2)
    if len(lst) != 0:
        for dr in lst:
            print(dr.title, dr.production_date)
    else:
        print("упс, такого напитка нема")


with open("wines.json") as json_rsr:
    wines_json = json.load(json_rsr)
wines = list()
for w_json in wines_json:
    try:
        date_created = datetime.date(int(w_json["vintage"]), int(random()*12 + 1), int(random()*28 + 1))
    except ValueError:
        date_created = datetime.date.today()
    wines.append(Wine(w_json["wine_full"], date_created))

with open("beers.json") as json_rsr:
    beers_json = json.load(json_rsr)
beers = list()
for b_json in beers_json:
    end_date = datetime.date.today()
    start_date = end_date - timedelta(days=740)
    random_date = start_date + (end_date - start_date) * random()
    beers.append(Beer(b_json["name"], random_date))

print("Market instance init")
market = Market(wines, beers)
print("есть ли в магазине вино 'Chianti Classico Riserva'")
print(market.has_drink_with_title("Chianti Classico Riserva"))
print()

print("распечатаем все напитки по наименованию")
for i in market.get_drinks_sorted_by_title():
    print(i.title + " --- " + str(i.production_date))

print_drinks_list(datetime.date(2021, 1, 1), datetime.date(2021, 1, 1))
print_drinks_list(datetime.date(2021, 1, 1), datetime.date(2022, 1, 1))
print_drinks_list(datetime.date(2025, 1, 1), datetime.date(2025, 1, 1))
print_drinks_list(datetime.date(1111, 1, 1), datetime.date(1111, 1, 1))
print_drinks_list(datetime.date(1, 1, 1), datetime.date(2025, 1, 1))
