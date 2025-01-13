from flask import Flask,render_template,request,redirect,url_for,flash,session
from pymongo import MongoClient

client=MongoClient('mongodb://localhost:27017/')
db=client["backlinksDB"]
collection=db["Description"]
user_collection = db["users"]

app=Flask(__name__)
app.secret_key="login_page112"

@app.route('/')
def home_page():
    return render_template("template.html")

@app.route('/login_',methods=["GET","POST"])
def login_page():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        print(f"username:{username}\n password: {password}")
        
        user=user_collection.find_one({"username":username})
        print("user",user)
        if user and user["password"]==password:
            flash("Login successful!","success")
            session['username']=user['username']

            return redirect(url_for("submit_backlink_page"))
        else:
            flash("Invaild username or password,","danger")
            return redirect(url_for("login_page"))
    else:
        if 'username' in session is not None:
            return redirect(url_for("submit_backlink_page"))

    return render_template("template.html")

@app.route("/logout",methods=["GET"])
def logout_user():
    if 'username' in session:
        session.pop('username',None)
        return render_template("template.html")    

@app.route('/description_page',methods=["GET","POST"])
def submit_backlink_page():
    print(f"method called: {request.method}")
    if request.method == "POST":
        description=request.form.get('description')
        print(description)
        collection.insert_one({'description':description})
        return redirect(url_for('success_page', description=description))
    return render_template('description_page.html')

@app.route('/success')
def success_page():
    # Retrieve description from query parameters
    description = request.args.get('description', default="No description provided")
    print(f"description:{description}")
    return render_template('success.html', description=description)

if __name__ == '__main__':
    app.run(debug=True)