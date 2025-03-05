from flask import Flask, redirect , url_for , render_template , request, session, flash


app = Flask(__name__)

@app.route("/")
def home():
  return render_template("home_page.html")


@app.route("/login" , methods = ["POST", "GET"])
def login():
  if request.method == "POST":
    usr_nm = request.form["user_name"]
    usr_email= request.form["user_email"]
    return render_template("display.html", name=usr_nm , email=usr_email)
  
  else:
    return render_template("form.html")
    

@app.route("/welcome <name>")
def welcome( name):
  return f"{name}"


if __name__ == "__main__":
  app.run(debug=True)