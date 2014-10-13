from scrape import scrape_players
import csv

# choose path for data to be saved to
output_path = 'players.csv'
# choose column headers - don't need to include player, season and team
headers=["FTM", "FTA", "3PM", "3PA"]
# column number on bball-ref (0 indexed) corresponding to above headers
indices = [17,18,11,12]
players = []

with open('links.csv', 'rb') as csvfile:
    rows = csv.DictReader(csvfile,  delimiter=',')
    for row in rows:
        players.append(row)

def csvDictWiter(path, fieldnames, data):
    with open(path, "a") as out_file:
        writer = csv.DictWriter(out_file, delimiter=',', fieldnames=fieldnames)
        for row in player_stats:
            writer.writerow(row)

fieldnames = ["player", "season", "team"]
for column in headers:
    fieldnames.append(column)

with open(output_path, "w") as out_file:
    writer = csv.DictWriter(out_file, delimiter=',', fieldnames=fieldnames)
    writer.writeheader()

scrape_obj = scrape_players.Scrape()
for x in range(len(players)):
    player_stats = scrape_obj.scrape(headers, players[x], "totals", indices)
    csvDictWiter(output_path, fieldnames, player_stats)
