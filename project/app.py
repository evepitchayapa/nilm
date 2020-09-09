from flask import Flask , render_template,redirect, url_for,request
from pymongo import MongoClient
import pandas as pd  
import matplotlib.pyplot as plt
import numpy as np                     
from io import BytesIO
import base64
import seaborn as sns
import pygal
from flask_cors import CORS,cross_origin
from flask_jsonpify import jsonify
from bson.json_util import dumps


app = Flask(__name__)
CORS(app)
cross_origin()
#if __name__ == '__main__':

    #app.run(debug=True)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/", methods=["GET"])
def helloWorld():
    return jsonify('hello')


def dataframe ():
    con = MongoClient("localhost",27017)
    db = con.get_database("nilm")
    iron = db.iron
    iron = iron.find()
    listdf = list(iron)
    # df = pd.DataFrame(listdf)
    df = dumps(listdf)
    wash = db.wash
    wash = wash.find()
    wash = list(wash)
    wash = pd.DataFrame(wash)
    return df,wash

@app.route("/show", methods=["GET"])
def home():
    df,wash = dataframe()
    #df = df.head(3)

    # tables=[df.to_html(classes='data')]
    # titles=df.columns.values
    
    # return render_template('dataframe.html',  
    # tables = tables,titles=titles )
    print('type')
    print (type(df))
    return df
   

@app.route("/test")
def test():
    return("hello")

@app.route("/graphic")
def pygale ():
    df,wash = dataframe()
    timecats = ['12 AM', '', '', '', '', '5 AM', '', '', '', '', '', '12 AM', '', '', '', '', '8 PM', '', '', '', '8 PM', '', '', '']    
    tg_iron = df.groupby('hour').mean()
    tg_iron['hour'] = tg_iron.index
    
    w = wash.groupby('hour').mean()
   
    graph = pygal.Line(y_title='Active Power(W)',x_title='Time Of Day',)
    graph.title = ''
    graph.x_labels = tg_iron['hour']
    #graph.add('hour', tg_iron['hour'])
    
    graph.add('Cloths Iron',tg_iron['active'])
    graph.add('Washing Machine',w['active'])
    graph_data = graph.render_data_uri()

    return render_template('graphic.html',graph_data = graph_data)


# @app.route('/home')
# def plot():
#     figactive = activeperhour()
#     on_png , off_png = percen_on_off()
#     return render_template('result.html', result=figactive.decode('utf8'),percen_on=on_png.decode('utf8'),percen_off=off_png.decode('utf8'))

# def activeperhour ():
#     df,wash= dataframe()
#     timecats = ['12 AM', '', '', '', '', '5 AM', '', '', '', '', '', '12 AM', '', '', '', '', '8 PM', '', '', '', '8 PM', '', '', '']
#     tg_iron = df.groupby('hour').mean()
#     tg_iron['hour'] = tg_iron.index
#     tg_iron.plot(x = 'hour', y= 'active')
#     plt.xticks(range(len(timecats)), timecats)
#     plt.ylabel("Active Power(W)")
#     plt.xlabel('Time Of Day')
#     figfile = BytesIO()
#     plt.savefig(figfile, format='png')
#     figfile.seek(0)  # rewind to beginning of file
#     figdata_png = base64.b64encode(figfile.getvalue())
#     return figdata_png

    
# def percen_on_off ():
#     df,wash = dataframe()
#     df = on_off(df)
#     on = duration_on(df)
#     off = duration_off(df)

#     #plot percen on
#     plt.figure(figsize=(10,3))
#     axoncl = sns.barplot(x=on.index, y=on['percen_on'], edgecolor='black',color='red', linewidth=1,alpha=0.4)
#     plt.title('Clothes iron')
#     plt.xlabel('Duration')
#     plt.ylabel('% ON')
#     plt.ylim(0,100)
#     figfile = BytesIO()
#     plt.savefig(figfile, format='png')
#     figfile.seek(0)  # rewind to beginning of file
#     on_png = base64.b64encode(figfile.getvalue())

#     #plot percen off

#     plt.figure(figsize=(10,3))
#     axoffcl = sns.barplot(x=off.index, y=off['percen_off'], edgecolor='black',color='red', linewidth=1,alpha=0.4)
#     plt.title('Clothes iron')
#     plt.xlabel('Duration')
#     plt.ylabel('% OFF')
#     plt.ylim(0,100)

#     figfile = BytesIO()
#     plt.savefig(figfile, format='png')
#     figfile.seek(0)  # rewind to beginning of file
#     off_png = base64.b64encode(figfile.getvalue())

#     return(on_png,off_png)


# def on_off(df):
#     on = df['active'] >10
#     on = on.to_frame()
#     on.columns = ['active']
#     onlist = []
#     offlist = []
#     count_true = 0
#     count_false = 0
#     for i in range(len(on['active'])):
#         if on['active'][i] == True:
#             count_true += 1
#             if count_false > 0:
#                 offlist.append(count_false)
#             count_false = 0
#         else:
#             if count_true > 0:
#                 onlist.append(count_true)
#             count_true = 0
#             count_false += 1
#     if count_true != 0:
#         onlist.append(count_true)
#     if count_false != 0:
#         offlist.append(count_false)
#     dfonoff = pd.DataFrame(onlist, columns=['on'])
#     dfonoff['off'] = pd.DataFrame(offlist)
    
#     return dfonoff

# def duration_on(df):
#     on_list=[]
#     for i in df['on']:
#         if i <= 1:
#             on_list.append('1s')
#         elif i <= 10:
#             on_list.append('10s')
#         elif i <= 30:
#             on_list.append('30s')
#         elif i <= 60:
#             on_list.append('1M')
#         elif i <= 300:
#             on_list.append('5M')
#         elif i <= 900:
#             on_list.append('15M')
#         elif i <= 1800:
#             on_list.append('30M')
#         elif i <= 3600:
#             on_list.append('1H')
#         elif i <= 7200:
#             on_list.append('2H')
#         elif i <= 14400:
#             on_list.append('4H')
#         elif i > 14400:
#             on_list.append('>4H')
#         else:
#             on_list.append('1s')
            
#     df['duration_on'] = on_list
#     total_on = df['on'].sum()
#     total_on
#     on_list =[]
#     for i in range(len(df['on'])):
#         calpercent = ((df['on'][i]) * 100) / total_on
#         on_list.append(calpercent)

#     df['percen_on'] = on_list
#     on = df.groupby(['duration_on']).sum()
#     corindex =['1s','10s','30s','1M','5M','15M','30M','1H','2H','4H','>4H']
#     on = on.reindex(corindex)
#     return on

# def duration_off(df):
#     off_list=[]
#     for i in df['off']:
#         if i <= 1:
#             off_list.append('1s')
#         elif i <= 10:
#             off_list.append('10s')
#         elif i <= 30:
#             off_list.append('30s')
#         elif i <= 60:
#             off_list.append('1M')
#         elif i <= 300:
#             off_list.append('5M')
#         elif i <= 900:
#             off_list.append('15M')
#         elif i <= 1800:
#             off_list.append('30M')
#         elif i <= 3600:
#             off_list.append('1H')
#         elif i <= 7200:
#             off_list.append('2H')
#         elif i <= 14400:
#             off_list.append('4H')
#         elif i > 14400:
#             off_list.append('>4H')
#         else:
#             off_list.append('1s')
            
#     df['duration_off'] = off_list
#     total_off = df['off'].sum()
#     total_off
#     off_list =[]
#     for i in range(len(df['off'])):
#         calpercent = ((df['off'][i]) * 100) / total_off
#         off_list.append(calpercent)

#     df['percen_off'] = off_list
#     off = df.groupby(['duration_off']).sum()
#     corindex =['1s','10s','30s','1M','5M','15M','30M','1H','2H','4H','>4H']
#     off = off.reindex(corindex)
#     return off


























#route
# @app.route("/")
# def student():
#     return render_template('student.html')
# @app.route('/blog/<int:postid>')
# def shw_blog(postid):
#     return 'blog num %d' %postid
# @app.route('/revno/<float:rev>')
# def rev (rev):
#     return 'rev num %f' %rev

# @app.route('/admin')
# def admin():
#     name = 'admin'
#     return render_template('hello.html',name = name)

# @app.route('/guest/<guest>')
# def guest (guest):
#     return 'hello %s ja' %guest

# @app.route('/user/<name>')
# def user (name):
#     if name == 'admin':
#         return redirect(url_for('admin'))
#     else:
#         return redirect(url_for('guest',guest = name))
    
# @app.route('/success/<name>')
# def success(name):
#    return 'welcome %s' % name

# @app.route('/login',methods = ['POST', 'GET'])
# def login():
#    if request.method == 'POST':
#       user = request.form['nm']
#       return redirect(url_for('success',name = user))
#    else:
#       user = request.args.get('nm')
#       return redirect(url_for('success',name = user))

# @app.route('/result',methods = ['GET','POST'])
# def result():
#     #dict = {'phy':50,'math':100,'eng':1}
#     if request.method == 'POST':
#         result = request.form
#     return render_template('result.html',result = result)

# @app.route('/index')
# def index():
#     return render_template('index.html')











