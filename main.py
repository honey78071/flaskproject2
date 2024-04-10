from flask import  Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myfirstdb.db"

db = SQLAlchemy(app)


class ContactUs(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(120))
    Message = db.Column(db.Text)

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

@app.route("/savethisdata", methods = ["post"])
def savethisdata(): 
    if request.method == "POST":
        mytitle = request.form.get("title")
        message = request.form.get("msg")

        data = ContactUs(Title = mytitle, Message = message)
        db.session.add(data)
        db.session.commit()

        return redirect("/contact")

    return "your data saved sucessfulyyy......!"


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