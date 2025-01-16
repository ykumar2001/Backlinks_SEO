from flask import Flask,render_template,request,redirect,url_for,session
from pymongo import MongoClient
from datetime import datetime
import requests
from bs4 import BeautifulSoup

client=MongoClient('mongodb://localhost:27017/')
db=client["backlinksDB"]
collection=db["Description"]
user_collection = db["users"]

app=Flask(__name__)
app.secret_key="login_page112"

# redirect to login page
@app.route('/')
def home_page():
    return render_template("template.html")

# open web for login 
@app.route('/login_',methods=["GET","POST"])
def login_page():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        print(f"username:{username}\n password: {password}")
        
        # find user in the database
        user=user_collection.find_one({"username":username})
        print("user",user)

        if user and user["password"]==password:
            session['username']=user['username']

            return redirect(url_for("submit_backlink_page"))
        else:
            return redirect(url_for("login_"))
    else:
        if 'username' in session is not None:
            return redirect(url_for("submit_backlink_page"))

    return render_template("template.html")

# logout portal on web page 
@app.route("/logout",methods=["GET"])
def logout_user():
    if 'username' in session:
        session.pop('username',None)
        return render_template("template.html")    

# Redirect you to description page
@app.route('/description_page',methods=["GET","POST"])
def submit_backlink_page():
    print(f"method called: {request.method}")
    
    today_date = (datetime.now().strftime('%Y-%m-%d'))
 
    print("today_date: ",today_date)
    if request.method == "POST":
        # description=request.form.get('description')
        
        keywords_name=request.form.get('keywords_name')
        backlink_url=request.form.get('backlink_url')
        domain_url=request.form.get('domain_url')
        submitted_url=request.form.get("submitted_url")
        domain_authority=request.form.get("domain_authority")
        # user_name=request.form.get('username')
        
        user_name = session['username']
        
        status= collect_all_links(submitted_url,keywords_name)
        print("STATUS: ",status)
        collection.insert_one({
            "date": str(today_date),
            "keywords_name":keywords_name,
            "backlink_url":backlink_url,
            "domain_url":domain_url,
            "submitted_url":submitted_url,
            # "domain_authority":domain_authority,
            "user_name":user_name,
            "lastcheck":today_date,
            "status":status
            })
        
       
        return redirect(url_for('backlink_page'))        
    return render_template('submit.html')

# check URL live or NOT
def collect_all_links(url, keywords):
    try:
        print("Keywords type: ", type(keywords))
      
        # Send GET request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()  # Raise an error for HTTP status codes >= 400

        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Check if any keyword is in the page content
        for key in keywords:
            if key.lower() in soup.get_text().lower():  # Case-insensitive check
                return "live"  # Return tuple with status and URL

        return "NA"
    

    except requests.exceptions.RequestException as e:
        # Return tuple with error status and message in case of an exception
        return "error", f"Error accessing {url}: {e}"

# Show Success Page after submssion of description page
@app.route('/backlink-page', methods=['GET'])
def backlink_page():
    username = session['username']
    # today_date = datetime.now().date()
    today_date = (datetime.now().strftime('%Y-%m-%d'))

    # Pagination parameters
    page = int(request.args.get('page', 1))  # Default to page 1 if not provided
    page_size = 10
    skip = (page - 1) * page_size

    # Query with pagination
    datas = collection.find({'user_name': username, 'date': str(today_date)}) \
        .skip(skip) \
        .limit(page_size)

    # Total record count for pagination
    total_count = collection.count_documents({'user_name': username, 'date': str(today_date)})
    total_pages = (total_count + page_size - 1) // page_size  # Round up

    return render_template(
        'backlink.html', 
        datas=datas, 
        page=page, 
        total_pages=total_pages
    )
if __name__ == '__main__':
    app.run(debug=True)