from flask import Flask, redirect , url_for , render_template , request, session, flash


app = Flask(__name__)
app.secret_key = "beep"

@app.route("/")
def home():
  return render_template("home_page.html")


@app.route("/login" , methods = ["POST", "GET"])
def login():
  if request.method == "POST":
    usr_nm = request.form["user_name"]
    usr_email= request.form["user_email"]
    session["user_name"] = usr_nm
    session["user_email"] = usr_email
    if usr_nm in session:
      flash(f"user already exists under the name: {usr_nm} and email: {usr_email}")
      return render_template("home_page.html", name=usr_nm , email=usr_email)
    
    return render_template("display.html", name=usr_nm , email=usr_email)
  
  else:
    return render_template("form.html")
    
@app.route("/logout")
def logout():
  flash("User logged out .")
  session.pop("user", None)
  session.pop("email", None)
  return redirect(url_for("login"))


if __name__ == "__main__":
  app.run(debug=True)