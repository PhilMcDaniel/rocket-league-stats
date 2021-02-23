from flask import Flask, render_template      
import pandas as pd

app = Flask(__name__)

#get dataframe with data
player_summary = pd.read_csv(".\\stat_files\\summary\\CLMNPlayerSummary.csv", sep=';')
overall_records = pd.read_csv(".\\stat_files\\summary\\CLMNSeriesRecord.csv", sep=';')
team_summary = pd.read_csv(".\\stat_files\\summary\\CLMNTeamSummary.csv", sep=';')
player_games_played = pd.read_csv(".\\stat_files\\summary\\CLMNRegularSeasonPlayerGamesPlayed.csv", sep=';')

@app.route("/")
def home():
    return render_template("home.html")
    
@app.route("/overallrecords")
def overallrecord():
    return render_template("home.html",tables=[overall_records.to_html(classes='data')],titles=overall_records.columns.values)

@app.route("/teamsummary")
def teamsummary():
    return render_template("home.html",tables=[team_summary.to_html(classes='data')],titles=team_summary.columns.values)

@app.route("/playersummary")
def playersummary():
    return render_template("home.html",tables=[player_summary.to_html(classes='data')],titles=player_summary.columns.values)

@app.route("/playergamesplayed")
def playergamesplayed():
    return render_template("home.html",tables=[player_games_played.to_html(classes='data')],titles=player_games_played.columns.values)


if __name__ == "__main__":
    app.run(debug=True)