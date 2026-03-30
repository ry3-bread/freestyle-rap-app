from flask import Flask, render_template, request, redirect, url_for, flash
import database as db


app = Flask(__name__)
app.secret_key = "atemporarysecretkey" # will change this later since this is a personal app

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
        # get word from form
        word_to_add = request.form["word"]
        # sanitize word
        word_to_add = word_to_add.strip().lower()
        # get rhymes string from form
        rhymes_to_add = request.form["rhymes"]
        # split, sanitize, filter rhymes
        rhymes_sanitized = [r.strip().lower() for r in rhymes_to_add.split(",") if r.strip()]
        # open database connection
        with db.get_connection() as conn:
            # add word
            w = db.add_word(conn, word_to_add)
            # loop through rhymes, call add_rhyme()
            for r in rhymes_sanitized:
                db.add_rhyme(conn, r, w) 
            # flash success message
        flash("Word added successfully!")
        # redirect to /add
        return redirect(url_for("add_page"))
    else:
        return render_template('add.html')

@app.route("/edit")
def edit_page():
    return "You're in edit!"

if __name__ == "__main__":
    app.run(debug=True)
