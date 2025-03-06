from flask import Flask, redirect , url_for , render_template , request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "beep"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime= timedelta(minutes=5)


db= SQLAlchemy(app)


class users(db.Model):  
    id = db.Column(db.Integer, primary_key=True) 
    usr_name = db.Column(db.String, nullable=False, unique=True)  
    usr_email = db.Column(db.String, nullable=False, unique=True)
    role = db.Column(db.String, nullable=False)

    def __init__(self, usr_name, usr_email, role):
        self.usr_name = usr_name  
        self.usr_email = usr_email  
        self.role = role  



@app.route("/home")
def home():
  return render_template("home_page.html")

@app.route("/view_data")
def view_data():
    return render_template("show_data.html", values= users.query.all())


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        usr_nm = request.form["user_name"]
        usr_email = request.form["user_email"]
        role = request.form["role"]

        # Check if user exists in the database
        found_user = users.query.filter_by(usr_name=usr_nm).first()

        if found_user:
            session["email"] = found_user.usr_email
            session["role"] = found_user.role  # Store role in session
        else:
            # Create new user (default role: "user")
            usr = users(usr_nm, usr_email, role)
            db.session.add(usr)
            db.session.commit()
            session["email"] = usr_email
            session["role"] = role

        # store user info in session
        session["user_name"] = usr_nm
        session["user_email"] = usr_email

        if session["role"] == "admin":
            flash(f"Welcome Admin {usr_nm}!", "success")
        else:
            flash(f"Welcome, {usr_nm}!", "success")
        return render_template("home_page.html", name=usr_nm, email=usr_email)

    else:  # GET method
        if "user_name" in session:
            usr_nm = session["user_name"]
            flash(f"Welcome back, {usr_nm}!", "info")
            return render_template("home_page.html", name=usr_nm)

        return render_template("form.html")




    
@app.route("/logout")
def logout():
  flash("User logged out of the session.")
  session.pop("user_name", None)
  session.pop("email_name", None)
  return redirect(url_for("login"))


if __name__ == "__main__":
  app.run(debug=True)

with app.app_context():
    db.create_all()