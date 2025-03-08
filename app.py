from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import os


PEOPLE_FOLDER = os.path.join('static', 'images')


app = Flask(__name__ , static_folder='static')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
app.secret_key = "beep"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class users(db.Model):  
    id = db.Column(db.Integer, primary_key=True) 
    usr_name = db.Column(db.String, nullable=False, unique=True)  
    usr_email = db.Column(db.String, nullable=False)
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

class announcements(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    ann_info = db.Column(db.String,  nullable=False)
    uni_name = db.Column(db.String,  nullable=False)

    def __init__ (self, ann_info, uni_name):
        self.ann_info=ann_info
        self.uni_name=uni_name

@app.route("/")
@app.route("/home")
def home():
    all_events = events.query.all()

    # Check if user is logged in and get username

    if "user_name" in session:
        user_name = session["user_name"]
    else:
        user_name = None
    berserk_img= os.path.join(app.config['UPLOAD_FOLDER'], 'L.png')
    hustle_img= os.path.join(app.config['UPLOAD_FOLDER'], 'B.png')
    aspire_img= os.path.join(app.config['UPLOAD_FOLDER'], 'S.png')
    dilip_img= os.path.join(app.config['UPLOAD_FOLDER'], 'dilip.png')
    eric_img =os.path.join(app.config['UPLOAD_FOLDER'], 'eric.png')
    return render_template("home_page.html", events=all_events, name=user_name, berserk_img= berserk_img, hustle_img=hustle_img, aspire_img=aspire_img, dilip_img=dilip_img, eric_img =eric_img  )

@app.route("/view_data")
def view_data():
    return render_template("show_data.html", values=users.query.all())


@app.route("/admin", methods=["GET"])
def admin():
    if "role" in session and session["role"] == "admin":
        return render_template("admin.html")
    #instead of going directly to the admin form or smtn we can make a intermediary page that admins can access and that can hold links to all these forms
    else:
        flash("Access denied. Admin privileges required.", "danger")
        return redirect(url_for("home"))
    

@app.route("/clear_events")
def clear_events():
    # if user not admin gtfo :)
    if "role" not in session or session["role"] != "admin":
        flash("Access denied. Admin privileges required.", "danger")
        return redirect(url_for("home"))
    
    #else remove all events
    db.session.query(events).delete()
    db.session.commit()
    
    flash("All events have been cleared!", "success")
    return redirect(url_for("home"))


@app.route("/add_event", methods=["POST"])
def add_event():
    if "role" not in session or session["role"] != "admin":
        flash("Access denied. Admin privileges required.", "danger")
        return redirect(url_for("home"))

    # Get form data
    event_name = request.form["name"]
    event_uni = request.form["uni_name"]
    flair = request.form["flair"]

    # Store event in database
    new_event = events(event_name, event_uni, flair)
    db.session.add(new_event)
    db.session.commit()

    flash("Event added successfully!", "success")
    return redirect(url_for("admin"))  # Redirect back to admin page


@app.route("/add_announcement", methods=["POST","GET"])
def announcement():
    if request.method == "POST":
        ann= request.form["ann_name"]
        uni_ann=request.form["uni_name"]
        
        # new announcement
        new_announcement = announcements(ann, uni_ann)
        db.session.add(new_announcement)
        db.session.commit()
        

        flash("Announcement added successfully!", "success")
        return render_template("home_page.html")
    #else:
        # user is admin and still somehow tries to add events or take admin actions:
        #return redirect(url_for("admin"))
        
@app.route("/berserk")
def  berserk():
    berserk0_img=os.path.join(app.config['UPLOAD_FOLDER'], 'L0.jpg')
    berserk1_img=os.path.join(app.config['UPLOAD_FOLDER'], 'L1.png')
    berserk2_img=os.path.join(app.config['UPLOAD_FOLDER'], 'L2.png')
    berserki_img=os.path.join(app.config['UPLOAD_FOLDER'], 'Linfo.png')
    return render_template("berserk.html", berserk0_img=berserk0_img, berserk1_img=berserk1_img, berserk2_img=berserk2_img, berserki_img=berserki_img) 

@app.route("/hustler")
def hustler ():
    hustle0_img=os.path.join(app.config['UPLOAD_FOLDER'], 'B0.png')
    hustle1_img=os.path.join(app.config['UPLOAD_FOLDER'], 'B1.png')
    hustle2_img=os.path.join(app.config['UPLOAD_FOLDER'], 'B2.png')
    hustlei_img=os.path.join(app.config['UPLOAD_FOLDER'], 'Linfo.png')
    return render_template("hustle.html",hustlei_img=hustlei_img, hustle0_img=hustle0_img, hustle1_img=hustle1_img, hustle2_img=hustle2_img) #dabba will hold the actual variable, container = variable

@app.route("/aspire")
def aspire():
    aspire0_img=os.path.join(app.config['UPLOAD_FOLDER'], 'S0.png')
    aspire1_img=os.path.join(app.config['UPLOAD_FOLDER'], 'S1.png')
    aspire2_img=os.path.join(app.config['UPLOAD_FOLDER'], 'S2.png')
    aspirei_img=os.path.join(app.config['UPLOAD_FOLDER'], 'Linfo.png')
    return render_template("aspire.html",aspirei_img=aspirei_img, aspire0_img=aspire0_img, aspire1_img=aspire1_img, aspire2_img=aspire2_img)

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        usr_nm = request.form["user_name"]
        usr_email = request.form["user_email"]
        role = request.form["role"]

        found_user = users.query.filter_by(usr_email=usr_email).first()

        if found_user:
            session["user_name"] = found_user.usr_name
            session["user_email"] = found_user.usr_email
            session["role"] = found_user.role
            flash(f"Welcome back,{found_user.usr_name}!", "success")
        else:
            new_user = users(usr_nm, usr_email, role)
            db.session.add(new_user)
            db.session.commit()
            session["user_name"] = usr_nm
            session["user_email"] = usr_email
            session["role"] = role
            flash(f"Welcome, {usr_nm}!", "success")

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
