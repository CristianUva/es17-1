from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import os 
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///astronomia.db'
db = SQLAlchemy(app)

class Telescopio(db.Model):
    __tablename__ = 'telescopio'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    posizione = db.Column(db.String(255), nullable=False)
    apertura = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    osservazioni = db.relationship('Osservazione', backref='telescopio', lazy=True)

class Corpo(db.Model):
    __tablename__ = 'corpo'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    categoria = db.Column(db.String(50), nullable=False)
    magnitudine = db.Column(db.Float, nullable=False)
    distanza_parsec = db.Column(db.Float, nullable=False)
    osservazioni = db.relationship('Osservazione', backref='corpo', lazy=True)

class Ricercatore(db.Model):
    __tablename__ = 'ricercatore'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    cognome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    istituzione = db.Column(db.String(150), nullable=False)

class Osservazione(db.Model):
    __tablename__ = 'osservazione'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    durata_minuti = db.Column(db.Float, nullable=False)
    condizioni_meteo = db.Column(db.String(50), nullable=False)
    note = db.Column(db.Text)
    telescopio_id = db.Column(db.Integer, db.ForeignKey('telescopio.id'), nullable=False)
    corpo_id = db.Column(db.Integer, db.ForeignKey('corpo.id'), nullable=False)
    ricercatori = db.relationship('Ricercatore', secondary='ricercatore_osservazione', 
                                  backref=db.backref('osservazioni', lazy='dynamic'))

ricercatore_osservazione = db.Table('ricercatore_osservazione',
    db.Column('ricercatore_id', db.Integer, db.ForeignKey('ricercatore.id'), primary_key=True),
    db.Column('osservazione_id', db.Integer, db.ForeignKey('osservazione.id'), primary_key=True)
)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/telescopi')
def lista_telescopi():
    telescopi = Telescopio.query.order_by(Telescopio.apertura.desc()).all()
    return render_template('telescopi.html', telescopi=telescopi)

@app.route('/corpi')
def lista_corpi():
    corpi = Corpo.query.order_by(Corpo.distanza_parsec).all()
    return render_template('corpi.html', corpi=corpi)

@app.route('/ricercatore/<int:id>')
def dettaglio_ricercatore(id):
    ricercatore = Ricercatore.query.get_or_404(id)
    osservazioni = Osservazione.query.join(ricercatore_osservazione).filter_by(ricercatore_id=id).all()
    return render_template('ricercatore.html', ricercatore=ricercatore, osservazioni=osservazioni)

@app.route('/statistiche')
def statistiche():
    # Media osservazioni per telescopio
    num_osservazioni = db.session.query(db.func.count(Osservazione.id) / db.func.count(db.distinct(Telescopio.id))).scalar()
    
    # Corpo più osservato
    corpo_piu_osservato = db.session.query(Corpo.nome, db.func.count(Osservazione.id)).\
        join(Osservazione, Osservazione.corpo_id == Corpo.id).\
        group_by(Corpo.id).\
        order_by(db.func.count(Osservazione.id).desc()).\
        first()
        
    corpo_nome = corpo_piu_osservato[0] if corpo_piu_osservato else "Nessuno"
    
    return render_template('statistiche.html', num_osservazioni=num_osservazioni, corpo_piu_osservato=corpo_nome)


def init_db():
    with app.app_context():
        # Elimina tutte le tabelle esistenti
        db.drop_all()
        print("Tabelle eliminate")
        
        # Crea nuove tabelle
        db.create_all()
        print("Tabelle create")
        
        # Aggiungi i telescopi
        telescopi = [
            Telescopio(nome='Very Large Telescope', posizione='Cerro Paranal, Cile', apertura=8.2, tipo='Riflettore'),
            Telescopio(nome='Hubble Space Telescope', posizione='Orbita terrestre', apertura=2.4, tipo='Riflettore spaziale'),
            Telescopio(nome='Arecibo', posizione='Puerto Rico', apertura=305, tipo='Radiotelescopo'),
            Telescopio(nome='Atacama Large Millimeter Array', posizione='Deserto di Atacama, Cile', apertura=12, tipo='Interferometro'),
            Telescopio(nome='Subaru Telescope', posizione='Mauna Kea, Hawaii', apertura=8.2, tipo='Riflettore')
        ]
        db.session.add_all(telescopi)
        
        # Aggiungi i corpi celesti
        corpi_celesti = [
            Corpo(nome='M87', categoria='Galassia', magnitudine=8.6, distanza_parsec=16800000),
            Corpo(nome='Proxima Centauri', categoria='Stella', magnitudine=11.05, distanza_parsec=1.3),
            Corpo(nome='Nebulosa di Orione', categoria='Nebulosa', magnitudine=4.0, distanza_parsec=412),
            Corpo(nome='Sagittarius A*', categoria='Buco nero', magnitudine=0, distanza_parsec=8178),
            Corpo(nome='Europa', categoria='Satellite', magnitudine=5.29, distanza_parsec=0.00425),
            Corpo(nome='Pulsar del Granchio', categoria='Pulsar', magnitudine=16.0, distanza_parsec=2000)
        ]
        db.session.add_all(corpi_celesti)
        
        # Aggiungi i ricercatori
        ricercatori = [
            Ricercatore(nome='Elena', cognome='Rossi', email='elena.rossi@astro.it', istituzione='INAF'),
            Ricercatore(nome='John', cognome='Smith', email='jsmith@nasa.gov', istituzione='NASA'),
            Ricercatore(nome='Maria', cognome='González', email='mgonzalez@eso.org', istituzione='ESO'),
            Ricercatore(nome='Hiroshi', cognome='Nakamura', email='hnakamura@jaxa.jp', istituzione='JAXA'),
            Ricercatore(nome='Sophie', cognome='Dubois', email='sdubois@esa.int', istituzione='ESA')
        ]
        db.session.add_all(ricercatori)
        
        db.session.commit()  # Commit iniziale per avere gli ID
        
        # Recupera gli oggetti appena creati per usare i loro ID
        t1 = Telescopio.query.filter_by(nome='Very Large Telescope').first()
        t2 = Telescopio.query.filter_by(nome='Hubble Space Telescope').first()
        t3 = Telescopio.query.filter_by(nome='Arecibo').first()
        t4 = Telescopio.query.filter_by(nome='Atacama Large Millimeter Array').first()
        t5 = Telescopio.query.filter_by(nome='Subaru Telescope').first()
        
        c1 = Corpo.query.filter_by(nome='M87').first()
        c2 = Corpo.query.filter_by(nome='Proxima Centauri').first()
        c3 = Corpo.query.filter_by(nome='Nebulosa di Orione').first()
        c4 = Corpo.query.filter_by(nome='Sagittarius A*').first()
        c5 = Corpo.query.filter_by(nome='Europa').first()
        c6 = Corpo.query.filter_by(nome='Pulsar del Granchio').first()
        
        r1 = Ricercatore.query.filter_by(nome='Elena').first()
        r2 = Ricercatore.query.filter_by(nome='John').first()
        r3 = Ricercatore.query.filter_by(nome='Maria').first()
        r4 = Ricercatore.query.filter_by(nome='Hiroshi').first()
        r5 = Ricercatore.query.filter_by(nome='Sophie').first()
        
        # Aggiungi le osservazioni
        osservazioni = [
            Osservazione(timestamp=datetime.strptime('2023-07-15 22:30:00', '%Y-%m-%d %H:%M:%S'), durata_minuti=120, condizioni_meteo='Sereno', note='Ottima visibilità', telescopio_id=t1.id, corpo_id=c1.id),
            Osservazione(timestamp=datetime.strptime('2023-08-02 20:15:00', '%Y-%m-%d %H:%M:%S'), durata_minuti=90, condizioni_meteo='Poco nuvoloso', note='Interferenze minime', telescopio_id=t2.id, corpo_id=c3.id),
            Osservazione(timestamp=datetime.strptime('2023-08-10 23:00:00', '%Y-%m-%d %H:%M:%S'), durata_minuti=180, condizioni_meteo='Sereno', note='Immagini ad alta risoluzione ottenute', telescopio_id=t5.id, corpo_id=c4.id),
            Osservazione(timestamp=datetime.strptime('2023-09-05 21:45:00', '%Y-%m-%d %H:%M:%S'), durata_minuti=150, condizioni_meteo='Sereno', note='Osservazione di routine', telescopio_id=t2.id, corpo_id=c2.id),
            Osservazione(timestamp=datetime.strptime('2023-09-20 04:30:00', '%Y-%m-%d %H:%M:%S'), durata_minuti=240, condizioni_meteo='Sereno', note='Attività insolita rilevata', telescopio_id=t3.id, corpo_id=c6.id),
            Osservazione(timestamp=datetime.strptime('2023-10-12 19:20:00', '%Y-%m-%d %H:%M:%S'), durata_minuti=100, condizioni_meteo='Nuvoloso', note='Qualità osservazione compromessa', telescopio_id=t4.id, corpo_id=c1.id),
            Osservazione(timestamp=datetime.strptime('2023-11-08 22:10:00', '%Y-%m-%d %H:%M:%S'), durata_minuti=135, condizioni_meteo='Sereno', note='Nuovi dati sulla rotazione', telescopio_id=t1.id, corpo_id=c5.id),
            Osservazione(timestamp=datetime.strptime('2023-12-01 23:50:00', '%Y-%m-%d %H:%M:%S'), durata_minuti=200, condizioni_meteo='Sereno', note='Spettroscopia dettagliata completata', telescopio_id=t5.id, corpo_id=c3.id)
        ]
        db.session.add_all(osservazioni)
        db.session.commit()
        
        # Recupera le osservazioni per ID
        o1 = Osservazione.query.filter_by(note='Ottima visibilità').first()
        o2 = Osservazione.query.filter_by(note='Interferenze minime').first()
        o3 = Osservazione.query.filter_by(note='Immagini ad alta risoluzione ottenute').first()
        o4 = Osservazione.query.filter_by(note='Osservazione di routine').first()
        o5 = Osservazione.query.filter_by(note='Attività insolita rilevata').first()
        o6 = Osservazione.query.filter_by(note='Qualità osservazione compromessa').first()
        o7 = Osservazione.query.filter_by(note='Nuovi dati sulla rotazione').first()
        o8 = Osservazione.query.filter_by(note='Spettroscopia dettagliata completata').first()
        
        # Aggiungi le relazioni ricercatore-osservazione
        # Utilizziamo gli oggetti invece di creare manualmente le associazioni
        o1.ricercatori.extend([r1, r2])
        o2.ricercatori.append(r3)
        o3.ricercatori.append(r4)
        o4.ricercatori.extend([r1, r5])
        o5.ricercatori.append(r2)
        o6.ricercatori.extend([r3, r5])
        o7.ricercatori.extend([r4, r1])
        o8.ricercatori.extend([r3, r5])
        
        db.session.commit()

if __name__ == '__main__':
    # Forza la ricreazione del database
    init_db()
    
    # Avvia l'app
    app.run(host='0.0.0.0', debug=True)