import sqlite3
import json
from flask import Flask, jsonify, request, g

app = Flask(__name__)

DATABASE= 'test.db'

def get_db():
  conn = sqlite3.connect('test.db', detect_types=sqlite3.PARSE_DECLTYPES)
  #conn.row_factory = sqlite3.Row
  return conn


connection = sqlite3.connect('test.db', detect_types=sqlite3.PARSE_DECLTYPES)
#connection.row_factory = sqlite3.Row
with open('schema.sql') as f:
  connection.executescript(f.read())

cur = connection.cursor()
data = [{'titel': 'Risotto', 'zutaten':'Reis, Bouillon, Zwiebeln', 'beschreibung': 'Reis anduensten, abloeschen mit Bouillon, koecheln lassen'}, {'titel': 'Pancakes', 'zutaten':'Eier, Milch, Mehl', 'beschreibung': 'Alles zusammenmischen, kurz stehen lassen und dann in die Pfanne geben'}, {'titel': 'Pancakes', 'zutaten':'Eier, Milch, Mehl', 'beschreibung': 'Alles, kurz stehen lassen und dann in die Pfanne geben'}]
sql = "INSERT INTO rezepte(titel, zutaten, beschreibung) VALUES (?, ?,?);"

for rezept in data:
  cur.execute(sql, (rezept['titel'], rezept['zutaten'], rezept['beschreibung']))

connection.commit()
connection.close()

def get_post():
  db = get_db()
  cursor = db.cursor()
  cursor.execute('SELECT * FROM rezepte')
  #print(cursor.fetchall())
  return cursor.fetchall()

def get_id(id):
 db = get_db()
 cursor = db.cursor()
 cursor.execute('SELECT * FROM rezepte WHERE id = ?', [id])
 return cursor.fetchone()

def insert_post(titel, zutaten, beschreibung):
  try:
    db = get_db()
    cursor = db.cursor()
    #cursor.execute('INSERT INTO rezepte (titel, zutaten, beschreibung) VALUES (?,?,?)', [rezept['titel'], rezept['zutaten'], rezept['beschreibung'], json.dumps(rezept)]) #Fehlercode: Expecting value: line 1 column 1 (char 0)
    cursor.execute('INSERT INTO rezepte (titel, zutaten, beschreibung) VALUES (?,?,?)', [titel, zutaten, beschreibung])
    db.commit()
    return True
  except Exception:
    raise


def update_post(titel, zutaten, beschreibung, id):
  db = get_db()
  cursor = db.cursor()
  cursor.execute('UPDATE rezepte SET titel = ?, zutaten = ?, beschreibung = ?' 'WHERE id = ?', [titel, zutaten, beschreibung, id])
  db.commit()
  return True

def delete_post(id):
  db = get_db()
  cursor = db.cursor()
  cursor.execute('DELETE FROM rezepte WHERE id= ?', [id])
  db.commit()
  return True
 


@app.route('/', methods=["GET"])
def get_rezepte():
  return jsonify(get_post())

@app.route('/<int:id>', methods=["GET"])
def get_rezept_id(id):
  return jsonify(get_id(id))

@app.route('/test')
def index():
  return jsonify({'name': 'Alex'})

@app.route('/add', methods=["POST"])
def insert_rezepte():
  import pdb
  pdb.set_trace()
  if request.method == 'POST':
    #rezept_details = request.get_json()
    
    try:
      titel = request.form['titel']
      zutaten = request.form['zutaten']
      beschreibung = request.form['beschreibung']
      result = insert_post(titel, zutaten, beschreibung)
      return f"Rezept wurde erstellt"
    except Exception as e:
      return jsonify(f"Fehler bei Hinzufuegen des Rezepts" + str(e))


@app.route('/<int:id>/update', methods=['PUT'])
def update_rezepte():
  rezept_details = request.get_json()
  id = rezept_details['id']
  titel = rezept_details['titel']
  zutaten = rezept_details['zutaten']
  beschreibung = rezept_details['beschreibung']
  return jsonify(insert_post(titel, zutaten, beschreibung, id))

@app.route('/<int:id>/delete', methods=['DELETE'])
def delete(id):
  return jsonify(delete_post(id))


if __name__=="__main__":
  app.run(debug=True)






