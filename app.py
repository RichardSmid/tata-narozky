from Flask import Flask, redirect, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from bs4 import BeautifulSoup
import requests

def getAuthorName(url):
    html = requests.get("https://www.youtube.com/watch?v=" + url).text
    soup = BeautifulSoup(html, "lxml")

    links = soup.find_all("link")
    author = "NO AUTHOR"

    for link in links:
        if '"name"' in str(link):
            author = str(link)[15:]
            author = author[:author.find('"')]

    name = soup.find_all("title")[0].text
    name = name[:len(name)-10]
    if len(name) > 27:
        name = name[:28] + "..."

    return author, name 


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True);
    content = db.Column(db.String(20), nullable = False)
    author = db.Column(db.String(20), nullable = False)
    name = db.Column(db.String(100), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return  "<Video %r>" % self.content

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        print("POST <----------")
    else:
        videoGet = Video.query.order_by(Video.date_created).all()
        
        return render_template('index.html', videoGet = videoGet)

@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Video.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that video'

@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    video = Video.query.get_or_404(id)

    if request.method == 'POST':
        url = request.form["url"].split("v=")[len(request.form["url"].split("?"))-1]
        
        author, name = getAuthorName(url)
        videoPost = Video(content=url, name=name, author=author)

        video.content = url
        video.author = author
        video.name = name

        try:            
            db.session.commit()
            return redirect('/')
        except:
            return "Something fucked up and the program doesn't work"
    else:
        return render_template('update.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)