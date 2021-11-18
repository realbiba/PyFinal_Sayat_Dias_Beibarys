from flask import *
from flask.helpers import make_response
from flask_sqlalchemy import SQLAlchemy
from selenium import webdriver
from bs4 import BeautifulSoup
from transformers import pipeline


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Bibasecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:9803@localhost:5432/pyFinal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


db.engine.execute('drop table if exists news')
db.engine.execute('create table  news (id int, name varchar(255), news varchar)')
db.session.commit()

class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column( db.VARCHAR(255))
    news = db.Column( db.VARCHAR(5000))

    def __init__(self,id,name, news):
        self.id = id
        self.name = name
        self.news = news


def GetFromDb(name, par):
    new_ex = News(1, name, str(par))
    db.session.add(new_ex)
    db.session.commit()

    return  db.engine.execute("select * from news where name = '" + name + "'")

@app.route('/coin',  methods = ['GET', 'POST'])
def coin():
    if request.method == 'POST':
        summarizer = pipeline("summarization")

        name = request.form['name']
        url = 'https://coinmarketcap.com/currencies/' + str(name) + "/news/"

        driver = webdriver.Chrome(executable_path=r'C:\Users\Beiba\OneDrive\Рабочий стол\chromedriver.exe')
        driver.get(url)
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')

        news = []
        news = soup.findAll('div', class_='sc-16r8icm-0 jKrmxw container')
        print('All news:')
        print(news)
        print("**************************")
        chunkNews = []

        for i in range(len(news)):


            if news[i].find('p', class_='sc-1eb5slv-0 svowul-3 ddtKCV') is not None:
                print("----------------------------")
                print("First part : ",chunkNews)
                print("----------------------------")
                chunkNews.append(news[i].text)
                print("----------------------------")
                print("Second part : ",chunkNews)
                print("----------------------------")
                ARTICLE = chunkNews
                chunkNews = summarizer(ARTICLE, max_length=50, min_length=40, do_sample=False)
                print("----------------------------")
                print("Third part : ",chunkNews)
                print("----------------------------")
                

        for i, news_item in enumerate(chunkNews):
            print(i, f"{news_item}\n")

        for chunkParagraphs in chunkNews:
            coins= GetFromDb(name, chunkParagraphs['summary_text'])

        return render_template("withNews.html", coins=coins, name=name )
    else:
        return "Retrieving Data!"

@app.route('/')
def index():
    auth = request.authorization
    if auth and auth.password == '9803':
        return render_template('index.html')
    return make_response('Something is wrong!', 401, {'WWW-Authenticate': 'Basic realm="Login required'})


if __name__ == '__main__':
    app.run(debug=True)
