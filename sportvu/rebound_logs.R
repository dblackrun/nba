# install.packages("RCurl")
# install.packages("RJSONIO")

# load packages
library(RCurl)
library(RJSONIO)

# base url for player shot logs
BASE_URL <- "http://stats.nba.com/stats/playerdashptreboundlogs?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&Period=0&PlayerID=<player_id>&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision="
# url for player totals page
league_stats_url <- "http://stats.nba.com/stats/leaguedashplayerstats?DateFrom=&DateTo=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&StarterBench=&VsConference=&VsDivision="

# get all players who have gotten a rebound this season
league_data_json <- getURL( league_stats_url )
league_data_list <- fromJSON( league_data_json, nullValue=NA )
number_of_rows <- length( league_data_list$resultSets[[1]]$rowSet )
league_data_table <- data.frame( matrix( unlist( league_data_list$resultSets[[1]]$rowSet ), nrow=number_of_rows, byrow=T ) )
colnames( league_data_table ) <- league_data_list$resultSets[[1]]$headers
league_data_table$REB <- as.numeric(as.character(league_data_table$REB))
league_data_table <- league_data_table[which(league_data_table$REB > 0),]

getPlayerReboundLogs <- function( player_id ){
  # function to get rebound logs for a single player
  url <- gsub("<player_id>", player_id, BASE_URL)
  data_json <- getURL( url )
  data_list <- fromJSON( data_json, nullValue=NA )
  number_of_rows <- length( data_list$resultSets[[1]]$rowSet )
  if(number_of_rows > 0){
    data_table <- data.frame( matrix( unlist( data_list$resultSets[[1]]$rowSet ), nrow=number_of_rows, byrow=T ) )
    colnames( data_table ) <- data_list$resultSets[[1]]$headers
    # player id and name don't come with rebound logs so add them to the taable
    data_table$PLAYER_ID <- player_id
    data_table$PLAYER_NAME <- league_data_table$PLAYER_NAME[which(league_data_table$PLAYER_ID == player_id)]
    data_table
  }
}
# get rebound logs for all players
rebound_logs <- do.call(rbind, lapply(league_data_table$PLAYER_ID, getPlayerReboundLogs))

# save table as a csv file
write.csv(rebound_logs, file="rebound_logs_2014_2015.csv", row.names=F)