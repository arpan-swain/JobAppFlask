from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail,Message

app = Flask(__name__)

app.config["SECRET_KEY"] = "myapp123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
#db is an instance of SQLAlchemy class
db = SQLAlchemy(app)

#FOR SENDING MAIL
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] =True
app.config["MAIL_USERNAME"] = "arpanswain754@gmail.com"
app.config["MAIL_PASSWORD"] = "qvvf acqz vaxb boet"

mail = Mail(app)


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

        message_body = f"Thank You for Submission, {first_name}. "\
        f"Here are your details :\n {first_name}\n{last_name}\n{date}\n"\
        f" Thank You !"

        message = Message(subject="New Form Submission",
                          sender = app.config["MAIL_USERNAME"],
                          recipients=[email],
                          body=message_body)

        mail.send(message)

        flash(f"{first_name}, Your form was submitted successfully !", "success")

    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)