import mechanize
from BeautifulSoup import BeautifulSoup
import csv

# date format yyyy-mm-dd
start_date = "2014-01-01"
end_date = "2015-04-01"

output_path = 'injuries.csv'

def csvDictWiter(path, fieldnames, data):
    with open(path, "a") as out_file:
        writer = csv.DictWriter(out_file, delimiter=',', fieldnames=fieldnames)
        writer.writerow(data)

fieldnames = ["Date", "Team", "Acquired", "Relinquished", "Notes"]

with open(output_path, "w") as out_file:
    writer = csv.DictWriter(out_file, delimiter=',', fieldnames=fieldnames)
    writer.writeheader()

url = 'http://www.prosportstransactions.com/basketball/Search/SearchResults.php?Player=&Team=&BeginDate='+start_date+'&EndDate='+end_date+'&ILChkBx=yes&InjuriesChkBx=yes&PersonalChkBx=yes&submit=Search&start=&start='
i = 0
while True:
    br = mechanize.Browser(factory=mechanize.RobustFactory())
    br.set_handle_robots(False)
    br.set_handle_refresh(False)
    br.addheaders = [('User-agent', 'Firefox')]

    response = br.open(url + str(i*25))
    soup = BeautifulSoup(response.read())

    table = soup.find('table', {'class':'datatable center'})
    if len(table.findAll('tr')) > 1:
        for tr in table.findAll('tr'):
            td = tr.findAll('td')
            if td[0].contents[0] != "&nbsp;Date":
                row = {}
                row['Date'] = str(td[0].contents[0])
                row['Team'] = str(td[1].contents[0])
                row['Acquired'] = str(td[2].contents[0])
                row['Relinquished'] = str(td[3].contents[0])
                row['Notes'] = str(td[4].contents[0])
                csvDictWiter(output_path, fieldnames, row)
        i += 1
    else:
        break