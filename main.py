from flask import Flask, render_template, request, url_for
import requests
from bs4 import BeautifulSoup

from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

app = Flask(__name__)


app.config['SECRET_KEY'] = '9QeQ7QGz!}~K`/!#'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# db.create_all()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    personal_number = db.Column(db.String(11), nullable=False)

    # def __str__(self):
    #     return f'name:{self.name},lastname:{self.last_name},personalnumber:{self.personal_number},'


@app.route("/")
def home():
    # users = Users(name="nika", last_name="mgaloblishvili", personal_number="010110185947")
    # db.session.add(users)
    # db.session.commit()
    # Users.query.delete()
    # db.session.commit()
    return render_template("home.html")



@app.route("/registration", methods=['GET', 'POST'])
def reg():
    if request.method == "POST":
        msg = "success"
        # print(request.form['username'])
        users = Users(name=request.form['username'], last_name=request.form['lastname'], personal_number=request.form['personal_number'])
        db.session.add(users)
        db.session.commit()
        return render_template("registration.html", message=msg)
    return render_template("registration.html")


@app.route("/registered-users")
def getRegisteredUsers():
    # res = db.select([Users.id, Users.name]).where(Users.id.in_(['1', '2']))
    # print(res)
    res = Users.query.all()
    return render_template("users-list.html", users_data=res)


@app.route("/profile/<int:userId>")
def deatiledUserProfile(userId):
    res = Users.query.filter_by(id=userId).first()
    # print(res.name)
    return render_template("user-inner.html", user=res)


@app.route("/profile/delete/user/<int:userId>")
def deleteRequestedUser(userId):
    res = Users.query.filter_by(id=userId).one()
    db.session.delete(res)
    db.session.commit()
    return redirect(url_for('getRegisteredUsers'))


@app.route("/about-project")
def about():
    return render_template("about.html")


@app.route("/prices")
def prices():
    price_array = []
    data = requests.get("https://www.gulf.ge/")
    src = BeautifulSoup(data.text, "html.parser")
    fuel_prices = src.findAll("div", {"class": "price_entry"})
    for i in fuel_prices:
        combined_data = i.text.strip()
        price_array.append(combined_data)
    print(price_array)
    return render_template("prices.html", price_data=price_array)




@app.route("/currency-rates")
def currency():
    data = requests.get("https://tbconline.ge/ibs/delegate/rest/exchangerate/v1/exchangeRatesChanges")
    # for i in data.json():
    #     print(i['currencyName'])
    return render_template("currency.html", currency_data=data.json())





@app.route("/author")
def author():
    return render_template("author.html")


app.run()
