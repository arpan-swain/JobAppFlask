from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SECRET_KEY"] = "myapp123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
#db is an instance of SQLAlchemy class
db = SQLAlchemy(app)

#create a datbase model...db.model is also a class
class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))

@app.route("/", methods = ["GET","POST"])
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        not_date_obj = request.form["date"]
        date = datetime.strptime(not_date_obj, "%Y-%m-%d")
        occupation = request.form["occupation"]

        form = Form(first_name =first_name, last_name = last_name, email= email,date=date, occupation =occupation)

        db.session.add(form)
        db.session.commit()

        flash(f"{first_name}, Your form was submitted successfully !", "success")

    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)