from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import csv

class Scrape_Stats_NBA(object):
    def __init__(self, season="2019-20", season_type="Regular%20Season"):
        self.season = season
        self.season_type = season_type
        self.titles = []
        self.item = []
        self.driver = webdriver.Firefox()
        
    def format_season_type(self, season_t):
        if season_t == "regular_season":
            self.season_type = "Regular%20Season"
        elif season_t == "preseason":
            self.season_type = "Pre%20Season"
        elif season_t == "playoffs":
            self.season_type = "Playoffs"
        elif season_t == "all_star":
            self.season_type = "All%20Star"
        else:
            self.season_type = "Regular%20Season"
        

    def scrape_data(self):
        url = "https://stats.nba.com/teams/traditional/?sort=W_PCT&dir=-1&Season={}&SeasonType={}".format(self.season, self.season_type)
        self.driver.get(url)
        s = BeautifulSoup(self.driver.page_source, 'html.parser')
        tableAll = s.find('table')

        titlesSoup = tableAll.find_all('th')
        for title in titlesSoup:
            self.titles.append(title.get_text())

        rows = s.find("table").find("tbody").find_all("tr")
        self.driver.close()
        for row in rows:
            for i in range(0,28):
                self.item.append(row.find_all("td")[i].get_text())
        


    def format_data(self):
        self.item = [i.replace(" ", "") for i in self.item]
        self.item = [i.replace("\n", "") for i in self.item]
        self.item = [self.item[i:i+28] for i in range(0,len(self.item),28)]
        self.titles = [self.titles[0:28]]

    def write_to_file(self):
        with open('nba_stats.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(self.titles)
            writer.writerows(self.item)

    def run(self):
        self.format_season_type(self.season_type)
        self.scrape_data()
        self.format_data()
        self.write_to_file()

#format season ex: 2019-20
#season_type: preseason regular_season playoffs all_star
scrape = Scrape_Stats_NBA("2019-20", "regular_season")
scrape.run()
print("file .csv saved")
