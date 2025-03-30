# Sistema di Network Astronomico

## Descrizione del Progetto
Questo progetto è un'applicazione web basata su Flask che consente di visualizzare informazioni su telescopi, corpi celesti, ricercatori e osservazioni astronomiche. Include pagine per visualizzare liste, dettagli e statistiche basate sui dati forniti.

### Funzionalità Principali
1. **Home Page (`/`)**:
   - Contiene pulsanti per navigare verso le altre pagine.

2. **Lista dei Telescopi (`/telescopi`)**:
   - Mostra una tabella con i telescopi ordinati per apertura.

3. **Lista dei Corpi Celesti (`/corpi`)**:
   - Mostra una tabella con i corpi celesti ordinati per distanza.

4. **Dettaglio Ricercatore (`/ricercatore/<int:id>`)**:
   - Mostra le osservazioni condotte da un ricercatore specifico, con i relativi corpi celesti.

5. **Statistiche (`/statistiche`)**:
   - Mostra:
     - Numero medio di osservazioni per telescopio.
     - Corpo celeste più frequentemente osservato.

---

## Come Funziona il Progetto

### Struttura del Progetto
- **`server.py`**: Contiene il codice principale dell'applicazione Flask.
- **`schema.sql`**: Script SQL per creare e popolare il database SQLite.
- **`templates/`**: Contiene i file HTML per il rendering delle pagine.
- **`static/`**: Contiene file statici come CSS.
- **`requirements.txt`**: Elenco delle dipendenze Python necessarie.

### Flusso di Lavoro
1. **Database**:
   - Il database SQLite viene creato utilizzando lo script `schema.sql`.
   - I dati iniziali vengono inseriti automaticamente.

2. **Applicazione Flask**:
   - Flask gestisce le richieste HTTP e restituisce le pagine HTML.
   - Le query al database vengono eseguite utilizzando il modulo `sqlite3`.

3. **Template HTML**:
   - I dati vengono passati ai template HTML per il rendering dinamico.

---

## Come Apportare Modifiche

### Modificare il Database
1. Aggiorna il file `schema.sql` per aggiungere o modificare tabelle.
2. Elimina il file `astronomia.db` esistente:
   ```bash
   rm astronomia.db
   ```
3. Riavvia il server per ricreare il database:
   ```bash
   python3 server.py
   ```

### Aggiungere Nuove Rotte
1. Aggiungi una nuova funzione in `server.py` con il decoratore `@app.route`.
2. Scrivi la logica per recuperare i dati dal database.
3. Crea un nuovo file HTML in `templates/` per il rendering della pagina.

### Modificare i Template HTML
1. Modifica i file in `templates/` per aggiornare il layout o aggiungere nuove funzionalità.
2. Usa le variabili passate da Flask per visualizzare i dati dinamicamente.

---

## Come Espandere il Progetto

### Aggiungere Nuove Tabelle
1. Aggiorna `schema.sql` con la definizione della nuova tabella.
2. Aggiorna `server.py` per includere nuove query e rotte.

### Aggiungere Nuove Pagine
1. Definisci una nuova rotta in `server.py`.
2. Crea un nuovo file HTML in `templates/`.
3. Aggiorna la home page (`index.html`) per includere un link alla nuova pagina.

### Migliorare le Statistiche
1. Scrivi nuove query SQL per calcolare statistiche aggiuntive.
2. Aggiungi queste statistiche alla pagina `/statistiche`.

---

## Tutorial: Creare un Progetto Simile

### Prerequisiti
- Python 3.x installato
- pip installato

### Passaggi

#### 1. Creare il Database
1. Scrivi il file `schema.sql` con le definizioni delle tabelle.
2. Esegui il file SQL per creare il database:
   ```bash
   sqlite3 astronomia.db < schema.sql
   ```

#### 2. Configurare Flask
1. Crea un file `server.py` con la configurazione di base:
   ```python
   from flask import Flask, render_template
   app = Flask(__name__)

   @app.route('/')
   def index():
       return render_template('index.html')

   if __name__ == '__main__':
       app.run(debug=True)
   ```

2. Installa Flask:
   ```bash
   pip install Flask
   ```

#### 3. Creare le Pagine
1. Crea una directory `templates/` e aggiungi i file HTML.
2. Usa Jinja2 per il rendering dinamico dei dati.

#### 4. Collegare il Database
1. Usa il modulo `sqlite3` per connetterti al database.
2. Scrivi funzioni per eseguire query e recuperare dati.

#### 5. Testare l'Applicazione
1. Avvia il server:
   ```bash
   python3 server.py
   ```
2. Apri il browser e verifica le pagine.

---

## Esempio di Codice SQL

Ecco un esempio di script SQL per creare le tabelle e popolare il database:

```sql
-- Creazione della tabella TELESCOPIO
CREATE TABLE TELESCOPIO (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL UNIQUE,
    posizione VARCHAR(255) NOT NULL,
    apertura FLOAT NOT NULL CHECK (apertura > 0),
    tipo VARCHAR(50) NOT NULL
);

-- Creazione della tabella CORPO_CELESTE
CREATE TABLE CORPO_CELESTE (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL UNIQUE,
    categoria VARCHAR(50) NOT NULL,
    magnitudine FLOAT NOT NULL,
    distanza_parsec FLOAT NOT NULL CHECK (distanza_parsec >= 0)
);

-- Inserimento dati di esempio
INSERT INTO TELESCOPIO (nome, posizione, apertura, tipo) VALUES
('Very Large Telescope', 'Cerro Paranal, Cile', 8.2, 'Riflettore');
```

---

## Conclusione
Questo progetto è un punto di partenza per creare applicazioni web basate su Flask con un database SQLite. Puoi espanderlo aggiungendo nuove funzionalità, migliorando l'interfaccia utente o integrando API esterne.
