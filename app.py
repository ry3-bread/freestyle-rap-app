from flask import Flask, render_template
import database as db

app = Flask(__name__)

with app.app_context():
    db.initialize_database()

@app.route("/")
def main_page():
    return render_template('main.html', hidden=True)

@app.route("/practice")
def practice_page():
    return "You're in practice!"

@app.route("/add")
def add_page():
    return "You're in add!"

@app.route("/edit")
def edit_page():
    return "You're in edit!"

if __name__ == "__main__":
    app.run(debug=True)
