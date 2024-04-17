from flask import Flask
from flask import  Flask, render_template, request, redirect,flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os

app = Flask(__name__)

app.secret_key ="cchghhvhvhjhvvhvhvh"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myfirstdb.db"

db = SQLAlchemy(app)

mail= Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'nitesh26028@gmail.com'
app.config['MAIL_PASSWORD'] = 'etzm cfxs yeex lawp'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
2

class ContactUs(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(120))
    Message = db.Column(db.Text)
    MYimage = db.Column(db.String(255))
# db.create_all()
    
with app.app_context():
    db.create_all()


@app.route("/")
def homepage():
    return render_template("home.html")

@app.route("/about")
def aboutus():
    return render_template("about.html")

@app.route("/contact")
def contactus():
    return render_template("contact.html")

@app.route("/services")
def servicespage():
    
    data = ContactUs.query.all()

    return render_template("services.html", mydata = data)

@app.route("/savethisdata", methods = ["POST"])
def savethisdata(): 
    if request.method == "POST":
        mytitle = request.form.get("title")
        mymessage = request.form.get("msg")
        myimg=request.files.get("img")
        if myimg:
            myimg.save(os.path.join("static/images", myimg.filename))
            path = os.path.join("static/images", myimg.filename)

        data = ContactUs(Title = mytitle, Message = mymessage, MYimage = path)
        # data = ContactUs(Title = mytitle, Message = message)
        db.session.add(data)
        db.session.commit()
        flash("Data Sucessfully saved in database..")
        flash("Check data saved in database")
        flash("Done")

        # msg = Message('Hello', sender = 'nitesh26028@gmail.com', recipients = ['nitesh26028@gmail.com'])
        # msg.body = "Hello Flask message sent from Flask-Mail"
        # mail.send(msg)
        # return "Setnt"
        return redirect("/contact")

    # return "your data saved sucessfulyyy......!"


@app.route("/deletethisdata/<int:x>", methods = ["POST"])
def deletethisdata(x):
    
    data = ContactUs.query.filter_by(id = x).first()
    db.session.delete(data)
    db.session.commit()

    return redirect("/services")

@app.route("/update-data/<int:myid>", methods = ["POST"])
def updatedata(myid):
    data = ContactUs.query.filter_by(id = myid).first()
    return  render_template('contact-update.html', xyz = data)




@app.route("/update-this-data/<int:xy>", methods = ["POST"])
def updatethis(xy):
    data = ContactUs.query.filter_by(id = xy).first()
    if request.method == "POST":
        mytitle = request.form.get("title")
        message = request.form.get("msg")

        data.Title = mytitle
        data.Message = message
        db.session.commit()
    return redirect("/services")

# dkjfdkljgkjdij
if __name__ == "__main__":
    app.run(debug = True)

# oRM: sqlalchemy