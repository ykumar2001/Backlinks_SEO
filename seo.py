from flask import Flask,render_template,request,redirect,url_for
from pymongo import MongoClient

client=MongoClient('mongodb://localhost:27017/')
db=client["backlinksDB"]
collection=db["Description"]

app=Flask(__name__)

@app.route('/')
def home_page():
    return "welcome to the page!"

@app.route('/login_')
def login_page():
    return render_template("/template.html")

@app.route('/description_page',methods=["GET","POST"])
def submit_backlink_page():
    if request.method=="POST":
        description=request.form.get('description_page')
        collection.insert_one({'description':description})

        return redirect(url_for('success.html'),description_page=description)
    return render_template('/description_page.html')

@app.route('/success')
def success_page():
    description=request.args.get('/description_page')
    return render_template('/success.html',description=description)




if __name__=='__main__':
    app.run(debug=True)