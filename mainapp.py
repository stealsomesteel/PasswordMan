from flask import Flask, render_template, request, redirect, url_for,flash
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "husshhhh"

conn = sqlite3.connect('passwords.db', check_same_thread=False)
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS passwords
             (id INTEGER PRIMARY KEY, title TEXT, username TEXT, password TEXT)''')
conn.commit()

@app.route("/")
def index():
    c.execute("SELECT * FROM passwords")
    passwords = c.fetchall()
    return render_template("index.html", passwords=passwords)
@app.route("/show")
def show():
    return redirect(url_for("index"))

@app.route("/add", methods=["GET", "POST"])
def add_password():
    if request.method == "POST":
        title = request.form["title"]
        username = request.form["username"]
        password = request.form["password"]
        c.execute("SELECT * FROM passwords WHERE title=LOWER(?) AND username = ? AND password <> ?", (title,username, password))
        exist=c.fetchone()
        if exist:
            flash("New Password detected for this service. Click on Show Table to update your password")
            
        else:
            c.execute("SELECT * FROM passwords WHERE title=LOWER(?) AND username = ? AND password = ?", (title,username, password))
            if c.fetchone():
                flash("This account is already in the database!!!")
                return redirect(url_for("add_password"))
            else:
                c.execute("INSERT INTO passwords (title, username, password) VALUES (LOWER(?),?, ?)", (title,username, password))
                conn.commit()
                return redirect(url_for("index"))
       
    return render_template("add.html")

@app.route("/delete/<int:id>",methods=["POST"])
def delete_password(id):
    c.execute("DELETE FROM passwords WHERE id=?", (id,))
    conn.commit()
    return redirect(url_for("index"))

@app.route("/update_password/<int:id>", methods=["GET","POST"])
def update_password(id):
    new_password = request.form["new_password"]
    c.execute("UPDATE passwords SET password =? WHERE id =?", (new_password, id))
    conn.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)