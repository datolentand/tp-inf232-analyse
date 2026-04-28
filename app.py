from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('sondage.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reponse
                 (id INTEGER PRIMARY KEY, age INTEGER, filiere TEXT, 
                  budget INTEGER, depense TEXT)''')
    conn.commit()
    conn.close()
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    age = request.form['age']
    filiere = request.form['filiere']
    budget = request.form['budget']
    depense = request.form['depense']
    conn = sqlite3.connect('sondage.db')
    c = conn.cursor()
    c.execute("INSERT INTO reponse (age, filiere, budget, depense) VALUES (?, ?, ?, ?)",
              (age, filiere, budget, depense))
    conn.commit()
    conn.close()
    return "Merci! <a href='/stats'>Voir les statistiques</a>"

@app.route('/stats')
def stats():
    conn = sqlite3.connect('sondage.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*), AVG(budget), MIN(budget), MAX(budget) FROM reponse")
    total, moyenne, mini, maxi = c.fetchone()
    c.execute("SELECT depense, COUNT(*), ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM reponse), 1) FROM reponse GROUP BY depense")
    depenses = c.fetchall()
    conn.close()
    return render_template('stats.html', total=total, moyenne=round(moyenne or 0), 
                           mini=mini or 0, maxi=maxi or 0, depenses=depenses)

if __name__ == '__main__':
    app.run(debug=True)
