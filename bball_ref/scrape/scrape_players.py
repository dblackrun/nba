import mechanize
from BeautifulSoup import BeautifulSoup
import re

BASE_URL = 'http://www.basketball-reference.com'

class Scrape:

    def __init__(self):
        self.browser = mechanize.Browser(factory=mechanize.RobustFactory())
        self.browser.set_handle_robots(False)
        self.browser.set_handle_refresh(False)
        self.browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0')]

    def scrape(self, headers, player_link, table_name, row_indices):
        rows = []
        url = BASE_URL + player_link["link"]
        response = self.browser.open(url)
        soup = BeautifulSoup(response.read())

        advanced_table = soup.find("table", {"id":table_name})
        for tr in advanced_table.findAll('tr'):
            if tr['class'] == "full_table" or tr['class'] == "light_text partial_table":
                full_row = {}
                row = tr.findAll('td')
                season = str(row[0].contents).split(">")[1].replace("</a", "")
                full_row["season"] = season
                team = str(row[2].contents).replace("[u'", "").replace("']", "")
                if team != "TOT":
                    team = team.split(">")[1].replace("</a", "")
                full_row["team"] = team
                for i in range(len(row_indices)):
                    value = str(row[row_indices[i]].contents).replace("[u'", "").replace("']", "")
                    full_row[headers[i]] = value
                full_row["player"] = player_link["player"]
                rows.append(full_row)
        return rows
