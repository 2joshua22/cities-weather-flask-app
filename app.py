from flask import Flask,render_template,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests
import confidential

app=Flask(__name__)
app.config["SECRET_KEY"]=confidential.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"]=confidential.SQLALCHEMY_DATABASE_URI
db=SQLAlchemy(app)
migrate=Migrate(app,db)
app.app_context().push()

class Cities(db.Model):
    __tablename__="cities"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),nullable=False)
    img=db.Column(db.String(120),nullable=False)
    datetime=db.Column(db.String(30),nullable=False)
    temp=db.Column(db.String(30),nullable=False)
    temp_like=db.Column(db.String(30),nullable=False)
    desc=db.Column(db.String(30),nullable=False)
    humi=db.Column(db.String(30),nullable=False)
    wind=db.Column(db.String(30),nullable=False)


    def __repr__(self):
        return "<Name %r" %self.name

class CityForm(FlaskForm):
    city_name=StringField("City: ",validators=[DataRequired()])
    submit=SubmitField("Add")



@app.route('/',methods=['POST','GET'])
def home():
    form=CityForm()
    cities=Cities.query.all()
    if form.validate_on_submit():
        city_name=form.city_name.data
        api_key=confidential.key
        url="http://api.weatherapi.com/v1/current.json?key={}&q={}&aqi=no".format(api_key,city_name)
        response=requests.get(url)
        data=response.json()
        city=Cities(name=data["location"]["name"],img=data["current"]["condition"]["icon"],datetime=data["location"]["localtime"],temp=data["current"]["temp_c"],temp_like=data["current"]["feelslike_c"],desc=data["current"]["condition"]["text"],humi=data["current"]["humidity"],wind=data["current"]["wind_kph"])
        db.session.add(city)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('home.html',Form=form,Cities=cities)

@app.route('/delete/<int:id>')
def delete(id):
    city=Cities.query.get(id)
    db.session.delete(city)
    db.session.commit()
    return redirect(url_for('home'))
if __name__=="__main__":
    app.run(debug=True)