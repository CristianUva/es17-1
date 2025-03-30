from flask import Flask, render_template, g
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DATABASE = 'astronomia.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_db():
    # Elimina il database esistente
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
    print("Database eliminato")
    
    # Crea il database e carica lo schema
    conn = sqlite3.connect(DATABASE)
    
    # Leggi lo schema SQL dal file
    with open('schema.sql', 'r') as f:
        schema_sql = f.read()
    
    # Esegui lo schema SQL per creare le tabelle e inserire i dati
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()
    
    print("Database inizializzato con successo")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/telescopi')
def lista_telescopi():
    telescopi = query_db('SELECT * FROM TELESCOPIO ORDER BY apertura DESC')
    return render_template('telescopi.html', telescopi=telescopi)

@app.route('/corpi')
def lista_corpi():
    corpi = query_db('SELECT * FROM CORPO_CELESTE ORDER BY distanza_parsec')
    return render_template('corpi.html', corpi=corpi)

@app.route('/ricercatore/<int:id>')
def dettaglio_ricercatore(id):
    ricercatore = query_db('SELECT * FROM RICERCATORE WHERE id = ?', [id], one=True)
    
    osservazioni = query_db('''
        SELECT o.* FROM OSSERVAZIONE o
        JOIN RICERCATORE_OSSERVAZIONE ro ON o.id = ro.osservazione_id
        WHERE ro.ricercatore_id = ?
    ''', [id])
    
    return render_template('ricercatore.html', ricercatore=ricercatore, osservazioni=osservazioni)

@app.route('/statistiche')
def statistiche():
    # Media osservazioni per telescopio
    num_osservazioni = query_db('''
        SELECT CAST(COUNT(o.id) AS REAL) / COUNT(DISTINCT t.id) 
        FROM OSSERVAZIONE o, TELESCOPIO t
    ''', one=True)[0]
    
    # Corpo più osservato
    corpo_query = query_db('''
        SELECT c.nome, COUNT(o.id) as conteggio
        FROM CORPO_CELESTE c
        JOIN OSSERVAZIONE o ON c.id = o.corpo_celeste_id
        GROUP BY c.id
        ORDER BY conteggio DESC
        LIMIT 1
    ''', one=True)
    
    corpo_nome = corpo_query[0] if corpo_query else "Nessuno"
    
    return render_template('statistiche.html', num_osservazioni=num_osservazioni, corpo_piu_osservato=corpo_nome)

if __name__ == '__main__':
    # Forza la ricreazione del database
    init_db()
    
    # Avvia l'app
    app.run(host='0.0.0.0', debug=True,port=58000)