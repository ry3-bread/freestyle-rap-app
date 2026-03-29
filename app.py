from flask import Flask, render_template, request
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

@app.route("/add", methods=['GET', 'POST'])
def add_page():
    if request.method == 'POST':
        pass # LEFT OFF HERE`
    else:
        return render_template('add.html')

@app.route("/edit")
def edit_page():
    return "You're in edit!"

if __name__ == "__main__":
    app.run(debug=True)
