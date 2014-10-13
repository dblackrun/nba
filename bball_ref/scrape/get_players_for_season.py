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

    def getPlayers(self, year):
        players = {}
        url = BASE_URL + "/leagues/NBA_" + str(year) + "_totals.html"
        response = self.browser.open(url)
        soup = BeautifulSoup(response.read())

        year_table = soup.find("table", {"id":"totals"})
        for a in year_table.findAll('a'):
            if "players" in str(a):
                players[a['href']] = str(a.contents).replace("[u'", "").replace("']", "")
        return players