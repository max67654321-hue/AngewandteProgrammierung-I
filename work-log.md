# Work Log

**Student Name:** 

Instructions: Fill out one log for each course day. Content to consider: Course Sessions + Assignment

## Template:

---

## 1. ✅ What did I accomplish?

_Reflect on the activities, exercises, and work you completed today._

**Guiding questions:**
- What topics or concepts did you work with?
- What exercises or projects did you complete?
- What tools or technologies did you use?
- What did you learn or practice?



---

## 2. 🚧 What challenges did I face?

_Describe any difficulties, obstacles, or confusing moments you encountered._

**Guiding questions:**
- What was difficult to understand?
- Where did you get stuck?
- What errors or problems did you face?
- What felt frustrating or confusing?




---

## 3. 💡 How did I overcome them?

_Explain how you overcame the challenges or what help you needed._

**Guiding questions:**
- What strategies did you try?
- Who or what helped you (instructor, classmates, documentation)?
- What did you learn from solving the problem?
- What questions do you still have?


---

## Week 1

### Day 1

#### 1. ✅ What did I accomplish?
```
- entwicklungsumgebung eingerichtet
- Git installiert und getestet
- VS Code installiert und Python extension eingerichtet
- uv installiert und version geprüft
- erstes FastAPI projekt erstellt
- main.py erstellt
- erste endpoints zusammen im kurs gemacht
- root endpoint gemacht
- status endpoint gemacht
- about endpoint gemacht
- API mit uv run fastapi dev gestartet
- endpoints in /docs getestet
- square endpoint gemacht
- student endpoint gemacht
- double endpoint gemacht
```

---

#### 2. 🚧 What challenges did I face?
```
- am anfang viele neue programme installiert
- terminal befehle waren noch ungewohnt
- verstehen was eine API ist war neu
- FastAPI syntax war neu
- verstehen wie @app.get funktioniert
- hausaufgabe musste ich alleine machen
- bei der hausaufgabe auf richtige pfade und funktionen achten
```

---

#### 3. 💡 How did I overcome them?
```
- setup schritt für schritt zusammen im kurs gemacht
- endpoints zusammen im kurs ausprobiert
- /docs benutzt um die API zu testen
- fehlermeldungen im terminal angeschaut
- beispiele aus dem kurs für die hausaufgabe benutzt
- hausaufgabe alleine fertig gemacht
```

---

### Day 2

#### 1. ✅ What did I accomplish?
```
- python basics wiederholt
- HTTP und JSON besprochen
- GET und POST unterschied gelernt
- Note Taking API angefangen
- notes endpoints gemacht
- daten in notes.json gespeichert
- endpoints in /docs getestet
- hausaufgabe mit category, filter und stats gemacht
```

---

#### 2. 🚧 What challenges did I face?
```
- viele neue sachen auf einmal
- GET und POST war am anfang ungewohnt
- Pydantic models waren neu
- load_notes und save_notes waren erstmal verwirrend
- category überall richtig einfügen
```

---

#### 3. 💡 How did I overcome them?
```
- beispiele aus dem kurs benutzt
- code schritt für schritt geschrieben
- endpoints in /docs getestet
- notes.json angeschaut
- hausaufgabe mit vorlage gemacht
```

---

### Day 3

#### 1. ✅ What did I accomplish?
- alles in plural bei benennung
- parameter sind optional
- jede uuid ist anders
- SQLModel mit python gemacht

#### 2. 🚧 What challenges did I face?
- neue imports gebraucht
- neue code stückchen gebraucht
- code wurde länger und unübersichtlicher

---

#### 3. 💡 How did I overcome them?
- schritt für schritt gemacht
- imports ergänzt
- code mit altem code verglichen
- doppelte endpoints vermieden
- besser verstanden wie FastAPI, SQLModel und SQLite zusammenarbeiten

---

## Week 2

### Day 4

#### 1. ✅ What did I accomplish
- requests benutzt um endpoints zu testen
- Faker benutzt für zufällige namen
- root endpoint getestet
- 404 error getestet
- greetings endpoint getestet
- is-adult endpoint getestet
- mehrere edge cases getestet
- tests mit uv run pytest ausgeführt
- gesehen ob tests passed oder failed sind

---

#### 2. 🚧 What challenges did I face?
- challenges größtenteils zusammen in der gruppe gemacht
- neue test datei gebraucht
- pytest syntax war erstmal ungewohnt
- edge cases waren teilweise schwer zu überlegen
- negative zahlen und falsche eingaben mussten extra getestet werden

---

#### 3. 💡 How did I overcome them?
- tests schritt für schritt geschrieben
- terminal ausgabe angeschaut
- failed tests verbessert
- mit verschiedenen zahlen getestet
- Faker für mehrere namen benutzt
- mehr edge cases hinzugefügt
- am ende mehrere tests erfolgreich durchlaufen lassen

---

### Day 5

#### 1. ✅ What did I accomplish?
- Pydantic Data Validation genauer kennengelernt
- verstanden, warum man Eingaben nicht einfach vertrauen sollte
- Mindestlängen, Maximallängen und Regex-Patterns ausprobiert
- HTTP 422 Fehler besser verstanden
- Eingaben wie title, category und tags validiert
- Tags bereinigt, kleingeschrieben und Duplikate entfernt
---

#### 2. 🚧 What challenges did I face?
- Pydantic Validatoren waren am Anfang schwer zu verstehen
- HTTP 422 Fehlermeldungen musste ich erst richtig lesen lernen
- `extra="forbid"` und `default_factory=list` waren neue Konzepte
- beim Bereinigen von tags musste man auf leere Werte, Großbuchstaben und Duplikate achten

---

#### 3. 💡 How did I overcome them?
- Beispiele aus dem Kurs Schritt für Schritt übernommen
- bewusst falsche Eingaben geschickt und die 422 Fehlermeldungen angeschaut
- Tags mit verschiedenen Beispielen getestet
- Code mit den bisherigen Notes Models verglichen
- verstanden, dass Pydantic die Eingaben prüfen soll, bevor der Endpoint ausgeführt wird
- durch die Übungen besser verstanden, wie man eine API sicherer und sauberer macht

---

### Day 6

#### 1. ✅ What did I accomplish?
- Python Decorators kennengelernt
- gesehen, dass FastAPI Decorators für Endpoints benutzt
- eigene Datei `class_based_decorator.py` erstellt
- mit `icecream` gearbeitet
- `uv add icecream` benutzt
- weiter an der Test-Suite gearbeitet
- zusätzliche pytest-Datei heruntergeladen und ins Repository eingefügt
- Tests mit `uv run pytest` ausgeführt
- gesehen, welche Tests bestanden haben und welche noch fehlgeschlagen sind

---

#### 2. 🚧 What challenges did I face?
- Decorators waren am Anfang schwer zu verstehen
- es war ungewohnt, dass eine Funktion eine andere Funktion verändern kann
- Unterschied zwischen eigentlicher Programmlogik und Zusatzaufgaben war neu
- manche Tests sind zuerst fehlgeschlagen
- es war schwierig zu erkennen, welcher Endpoint oder welches Model angepasst werden musste
- ältere Aufgaben wie Datenbank-Backend und Validation mussten noch mit den Tests zusammenpassen

---

#### 3. 💡 How did I overcome them?
- Decorator-Beispiele Schritt für Schritt ausprobiert
- `icecream` genutzt, um Ausgaben besser zu verstehen
- Tests im Terminal ausgeführt und Fehlermeldungen gelesen
- fehlgeschlagene Tests einzeln angeschaut
- Code mit den bisherigen Aufgaben verglichen
- verstanden, dass Tests helfen, Fehler in der API schneller zu finden
- weiter daran gearbeitet, dass die komplette Test-Suite erfolgreich durchläuft
---

## Week 3

### Day 7

#### 1. ✅ What did I accomplish?
- Streamlit kennengelernt
- verstanden, dass Streamlit ein einfaches Frontend mit Python ermöglicht
- Streamlit im Projekt benutzt
- eine erste kleine Streamlit App getestet
- Eingabefelder, Buttons und Ausgaben ausprobiert
- mit `requests` eine externe API abgefragt
- verstanden, dass FastAPI als Backend und Streamlit als Frontend zusammenarbeiten können
- Aufgabe für `frontend.py` bekommen
---

#### 2. 🚧 What challenges did I face?
- Streamlit war neu für mich
- Frontend und Backend gleichzeitig zu verstehen war ungewohnt
- es war etwas verwirrend, zwei Terminals parallel zu nutzen
- die API muss laufen, damit das Frontend Daten abrufen kann
- Formular mit mehreren Eingaben musste richtig aufgebaut werden

---

#### 3. 💡 How did I overcome them?
- Beispiel aus der Präsentation Schritt für Schritt angeschaut
- erst einfache Texte und Eingaben in Streamlit getestet
- Button benutzt, um eine API-Anfrage auszulösen
- mit `requests.get()` Daten von einer API geholt
- verstanden, dass FastAPI und Streamlit parallel laufen müssen
- Dokumentation und Kursbeispiele als Hilfe benutzt
- `frontend.py` als Startpunkt für die Hausaufgabe vorbereitet
---

### Day 8

#### 1. ✅ What did I accomplish?
- Das Projekt strukturiert und aufgeräumt
- Die Aufgaben einzelner Dateien besser verstanden
- Prüfungsrelevante Dateien kontrolliert und sinnvoll benannt
- Das README verbessert und übersichtlicher gestaltet
- Alle Tests überprüft und erfolgreich ausgeführt
- Code verbessert und erneut getestet
---

#### 2. 🚧 What challenges did I face?
- Oft war es schwierig nachzuvollziehen, warum bestimmte Schritte notwendig sind
- Änderungen am Code waren nicht immer direkt verständlich
- Mir haben an einigen Stellen technische Grundlagen gefehlt
---

#### 3. 💡 How did I overcome them?
- KI benutzt um nach Erklärungen zu fragen 
- Ein besseres Verständnis für SQL-Datenbanken und deren Vorteile entwickelt
- Fehler gemeinsam analysiert und nachvollzogen
- Gezielt Fragen gestellt, wenn etwas unklar war
---

# 🎉 Congratulations! You did it! 🎓✨
