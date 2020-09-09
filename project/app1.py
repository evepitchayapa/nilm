from flask import Flask , render_template,redirect, url_for,request
import pandas as pd  
from pymongo import MongoClient
import pandas as pd  

app = Flask(__name__)

def dataframe ():
    con = MongoClient("localhost",27017)
    db = con.get_database("nilm")
    iron = db.iron
    iron = iron.find()
    listdf = list(iron)
    df = pd.DataFrame(listdf)
    return df

@app.route("/", methods=["GET"])
def home():
    df = dataframe()
    df = df.head(3)
    tables=[df.to_html(classes='data')]
    titles=df.columns.values
    return render_template('dataframe.html',  
    tables = tables,titles=titles )