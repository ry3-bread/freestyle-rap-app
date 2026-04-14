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
        # handle edge case of empty word
        if not word_to_add:
            flash("Empty word! Try again.")
            return redirect(url_for("add_page"))
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
    # connect to database
    with db.get_connection() as conn:
        # get all the words
        word_rows = db.get_all_words(conn)
    return render_template('edit.html', words=word_rows)

@app.route("/edit/<int:word_id>")
def edit_specific_page(word_id):
    # get connection
    with db.get_connection() as conn:
    # get word
        word = db.get_word(conn, word_id)
    # get rhymes
        rhymes = db.get_rhymes(conn, word_id)
    return render_template('edit_word.html', word=word, rhymes=rhymes)

@app.route("/edit/<int:word_id>/rename", methods=['GET', 'POST'])
def edit_rename_page(word_id):
    # get connection
    if request.method == 'POST':
        rename_word = request.form["rename_word"]
        rename_word = rename_word.strip().lower()
        if not rename_word:
            flash("Empty word to rename to! Try again.")
            return redirect(url_for("edit_rename_page", word_id=word_id))
        with db.get_connection() as conn:
            if db.rename_word(conn, word_id, rename_word):
                flash("Successful!")
                return redirect(url_for("edit_rename_page", word_id=word_id))
            else:
                flash("Failed. Word already exists.")
                return redirect(url_for("edit_rename_page", word_id=word_id))
    else:
        with db.get_connection() as conn:
            word = db.get_word(conn, word_id)
        return render_template("edit_rename_page.html", word=word)

@app.route("/edit/<int:word_id>/add-rhymes", methods=['GET', 'POST'])
def edit_add_rhymes_page(word_id):
    # get connection
    if request.method == 'POST':
        more_rhymes = request.form["more_rhymes"]
        more_rhymes = [r.strip().lower() for r in more_rhymes.split(",") if r.strip()]
        if not more_rhymes:
            flash("No rhymes submitted! Try again.")
            return redirect(url_for("edit_add_rhymes_page", word_id=word_id))
        with db.get_connection() as conn:
            for rhyme in more_rhymes:
                db.add_rhyme(conn, rhyme, word_id)
        flash("Successful adding of rhymes!")
        return redirect(url_for("edit_add_rhymes_page", word_id=word_id))
    else:
        with db.get_connection() as conn:
            word = db.get_word(conn, word_id)
        return render_template("edit_add_rhymes_page.html", word=word)

@app.route("/edit/<int:word_id>/delete-word", methods=['GET', 'POST'])
def edit_delete_word_page(word_id):
    if request.method == 'POST':
        if request.form["action"] == "Yes":
            with db.get_connection() as conn:
                db.delete_word(conn, word_id)
            flash("Successful!")
            return redirect(url_for("edit_page"))
        else:
            return redirect(url_for("edit_specific_page", word_id=word_id))
    else:
        with db.get_connection() as conn:
            word = db.get_word(conn, word_id)
        return render_template("edit_delete_word_page.html", word=word)

if __name__ == "__main__":
    app.run(debug=True)
