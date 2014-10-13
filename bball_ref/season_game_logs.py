from scrape import get_players_for_season
from scrape import scrape_players
import csv

season = 2014
headers =["MP", "TS", "EFG", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "USG", "ORtg", "DRtg"]
indices = [9,10,11,12,13,14,15,16,17,18,19,20,21]

output_path = 'logs_' + str(season) + '.csv'

def csvDictWiter(path, fieldnames, data):
    with open(path, "a") as out_file:
        writer = csv.DictWriter(out_file, delimiter=',', fieldnames=fieldnames)
        for row in player_stats:
            writer.writerow(row)

fieldnames = ["player", "G", "Date"]
for column in headers:
    fieldnames.append(column)

with open(output_path, "w") as out_file:
    writer = csv.DictWriter(out_file, delimiter=',', fieldnames=fieldnames)
    writer.writeheader()

print "Getting players for " + str(season) + " ..."
season_scrape_obj = get_players_for_season.Scrape()
players = season_scrape_obj.getPlayers(season)
print "Retrieved players"

scrape_obj = scrape_players.Scrape()

for key in players.keys():
    link = 'http://www.basketball-reference.com' + key
    link =  link.replace( ".html", "/gamelog/2014/" )
    try:
        print "Getting logs for " + players[key] + " ..."
        player_stats = scrape_obj.scrapeLogs(headers, link, players[key], "pgl_advanced", indices)
        print "Writing to file..."
        csvDictWiter(output_path, fieldnames, player_stats)
    except:
        print "FAIL"
