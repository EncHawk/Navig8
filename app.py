from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "beep"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

class users(db.Model):  
    id = db.Column(db.Integer, primary_key=True) 
    usr_name = db.Column(db.String, nullable=False, unique=True)  
    usr_email = db.Column(db.String, nullable=False, unique=True)
    role = db.Column(db.String, nullable=False)

    def __init__(self, usr_name, usr_email, role):
        self.usr_name = usr_name  
        self.usr_email = usr_email  
        self.role = role  

class events(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    evnt_title = db.Column(db.String, nullable=False)
    evnt_uni = db.Column(db.String, nullable=False)
    evnt_flair = db.Column(db.String, nullable=False)

    def __init__(self, evnt_title, evnt_uni, evnt_flair):
        self.evnt_title = evnt_title
        self.evnt_uni = evnt_uni
        self.evnt_flair = evnt_flair

@app.route("/")
def home():
    all_events = events.query.all()

    # Check if user is logged in and get username

    if "user_name" in session:
        user_name = session["user_name"]
    else:
        user_name = None
    return render_template("home_page.html", events=all_events, name=user_name)

@app.route("/view_data")
def view_data():
    return render_template("show_data.html", values=users.query.all())


@app.route("/admin", methods=["GET"])
def admin():
    if "role" in session and session["role"] == "admin":
        return render_template("admin-form.html")
    else:
        flash("Access denied. Admin privileges required.", "danger")
        return render_template("home_page.html")
    


@app.route("/add_event", methods=["POST", "GET"])
def add_event():
    # Check if user is admin
    if "role" not in session or session["role"] != "admin":
        flash("Access denied. Admin privileges required.", "danger")
        return render_template("home_page.html")
    
    if request.method == "POST":
        event_name = request.form["name"]
        event_uni = request.form["uni_name"]
        flair = request.form["flair"]
        
        # Create a new event
        new_event = events(event_name, event_uni, flair)
        db.session.add(new_event)
        db.session.commit()
        
        flash("Event added successfully!", "success")
        return render_template("home_page.html")
    else:
        # If someone tries to access this route with GET
        return redirect(url_for("admin"))
    




@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        usr_nm = request.form["user_name"]
        usr_email = request.form["user_email"]
        role = request.form["role"]

        found_user = users.query.filter_by(usr_name=usr_nm).first()
        if found_user:
            session["email"] = found_user.usr_email
            session["role"] = found_user.role
        else:
            usr = users(usr_nm, usr_email, role)
            db.session.add(usr)
            db.session.commit()
            session["email"] = usr_email
            session["role"] = role

        session["user_name"] = usr_nm
        session["user_email"] = usr_email

        flash(f"Welcome {usr_nm}!", "success")
        return redirect(url_for("home"))
    
    if "user_name" in session:
        flash(f"User already logged in.", "info")
        return redirect(url_for("home"))
    
    return render_template("form.html")

@app.route("/logout")
def logout():
    session.pop("user_name", None)
    session.pop("email", None)
    flash("User logged out of the session.", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
