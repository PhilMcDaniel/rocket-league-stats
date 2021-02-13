from flask import Flask, render_template      
import pandas as pd

app = Flask(__name__)

#get dataframe with data
df = pd.read_csv(".\\stat_files\\PLAYER_0ac4f9ee-9bd6-432c-8386-e2359834c365.csv", sep=';')

@app.route("/")
def home():
    return render_template("home.html",tables=[df.to_html(classes='data')], titles=df.columns.values)
    
@app.route("/salvador")
def salvador():
    return "Hello, Salvador"
    
if __name__ == "__main__":
    app.run(debug=True)