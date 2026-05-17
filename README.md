# Angewandte Programmierung - Notes API

Dieses Projekt ist eine kleine Notiz-Webanwendung aus dem Kurs "Angewandte Programmierung". Es besteht aus einem FastAPI-Backend, einer SQLite-Datenbank mit SQLModel und einem einfachen Streamlit-Frontend.

## Inhalt

- [Projektuebersicht](#projektuebersicht)
- [Technologien](#technologien)
- [Setup](#setup)
- [Starten](#starten)
- [Tests](#tests)
- [Projektstruktur](#projektstruktur)
- [API-Uebersicht](#api-uebersicht)
- [Kurz erklaert](#kurz-erklaert)

## Projektuebersicht

Die Anwendung verwaltet Notizen mit Titel, Inhalt, Kategorie, Erstellungsdatum und Tags.

Das Backend bietet REST-Endpunkte fuer:

- Notizen erstellen, lesen, aktualisieren und loeschen
- Notizen nach Kategorie, Suchbegriff, Tag und Datum filtern
- Statistiken zu Kategorien und Tags anzeigen
- genutzte Kategorien und Tags auflisten

Das Frontend ist eine Streamlit-App. Dort koennen neue Notizen erstellt und vorhandene Notizen angezeigt werden. Zusaetzlich enthaelt das Frontend eine kleine "Say No App", die Text von einer externen API abruft.

## Technologien

| Technologie | Zweck |
|-------------|-------|
| Python 3.12+ | Programmiersprache |
| FastAPI | REST-API |
| SQLModel | Datenbankmodelle und ORM |
| SQLite | lokale Datenbank `notes.db` |
| Pydantic | Request- und Response-Modelle |
| Streamlit | Web-Frontend |
| requests | HTTP-Aufrufe im Frontend und in Tests |
| pytest | automatisierte Tests |
| uv | Paketmanager und Runner |

## Setup

Voraussetzungen:

- Python 3.12 oder neuer
- `uv` installiert

Installation:

```bash
git clone <dein-repo-url>
cd "Angewandte Programmierung 1/AngewandteProgrammierung-I"
uv sync
```

## Starten

Backend starten:

```bash
uv run fastapi dev main.py
```

Die API laeuft danach unter:

- API: `http://127.0.0.1:8000`
- Swagger-Dokumentation: `http://127.0.0.1:8000/docs`

Frontend in einem zweiten Terminal starten:

```bash
uv run streamlit run frontend.py
```

Das Frontend laeuft standardmaessig unter:

- `http://localhost:8501`

## Tests

Die Tests in `test_notes.py` senden echte HTTP-Requests an die laufende FastAPI-App. Deshalb muss das Backend vorher gestartet sein.

Terminal 1:

```bash
uv run fastapi dev main.py
```

Terminal 2:

```bash
uv run pytest test_notes.py -v
```

Getestet werden unter anderem:

- CRUD-Funktionen fuer Notizen
- Filter nach Kategorie, Suchbegriff und Tag
- kombinierte Filter
- Fehlerfaelle mit `404` und `422`
- Statistik-, Kategorien- und Kategorie-Notizen-Endpunkte
- partielle Updates mit `PATCH`

## Projektstruktur

```text
AngewandteProgrammierung-I/
├── main.py                    # FastAPI-Backend mit SQLModel und SQLite
├── frontend.py                # Streamlit-Frontend
├── test_notes.py              # API-Tests mit requests und pytest
├── main_sqlmodel.py           # weitere SQLModel-Datei aus dem Kurs
├── pyproject.toml             # Projektkonfiguration und Dependencies
├── uv.lock                    # Lockfile fuer uv
├── notes.db                   # SQLite-Datenbank
├── data/
│   └── notes.json             # optionale Beispiel-Notizen fuer Migration
├── exploration/               # Kurs- und Experimentdateien
│   ├── apitest.py
│   ├── day4.py
│   ├── test_lenni.py
│   ├── test_main.py
│   └── test_main_client.py
├── work-log.md
└── README.md
```

## API-Uebersicht

### Allgemein

| Methode | URL | Beschreibung |
|---------|-----|--------------|
| `GET` | `/` | Hello-World-Antwort |
| `GET` | `/name/{name}` | Begruessung mit Name |
| `GET` | `/name/{name}/{number}` | Begruessung mit verdoppelter Zahl |
| `GET` | `/alter/{alter}` | Ausgabe eines Alters |
| `GET` | `/summe/{zahl1}/{zahl2}` | Summe aus zwei Zahlen |
| `GET` | `/queryparameters` | kleines Beispiel fuer Query-Parameter |

### Notes

| Methode | URL | Beschreibung |
|---------|-----|--------------|
| `GET` | `/notes` | Alle Notizen abrufen, optional mit Filtern |
| `POST` | `/notes` | Neue Notiz erstellen |
| `GET` | `/notes/stats` | Statistik zu Notizen, Kategorien und Tags |
| `GET` | `/notes/{note_id}` | Einzelne Notiz abrufen |
| `PUT` | `/notes/{note_id}` | Notiz vollstaendig ersetzen |
| `PATCH` | `/notes/{note_id}` | Notiz teilweise aktualisieren |
| `DELETE` | `/notes/{note_id}` | Notiz loeschen |
| `GET` | `/notes/category/{category}` | Legacy-Endpunkt fuer Notizen einer Kategorie |

Filter fuer `GET /notes`:

| Parameter | Beispiel |
|-----------|----------|
| `category` | `/notes?category=Work` |
| `search` | `/notes?search=Meeting` |
| `tag` | `/notes?tag=urgent` |
| `created_after` | `/notes?created_after=2025-01-01T00:00:00` |
| `created_before` | `/notes?created_before=2025-12-31T23:59:59` |

Beispiel fuer eine neue Notiz:

```json
{
  "title": "Vorlesung vorbereiten",
  "content": "Slides lesen und Beispielcode testen",
  "category": "Uni",
  "tags": ["python", "fastapi"]
}
```

### Tags

| Methode | URL | Beschreibung |
|---------|-----|--------------|
| `GET` | `/tags` | Alle verwendeten Tags abrufen |
| `GET` | `/tags/{tag_name}/notes` | Alle Notizen mit einem bestimmten Tag abrufen |

### Categories

| Methode | URL | Beschreibung |
|---------|-----|--------------|
| `GET` | `/categories` | Alle verwendeten Kategorien abrufen |
| `GET` | `/categories/{category_name}/notes` | Alle Notizen einer Kategorie abrufen |

## Kurz erklaert

### Datenbankmodell

In `main.py` gibt es drei SQLModel-Tabellen:

- `Note`: speichert Titel, Inhalt, Kategorie und Erstellungsdatum
- `Tag`: speichert eindeutige Tag-Namen
- `NoteTagLink`: verbindet Notizen und Tags als Many-to-Many-Beziehung

Dadurch kann eine Notiz mehrere Tags haben und ein Tag kann zu mehreren Notizen gehoeren.

### Validierung

FastAPI und Pydantic pruefen automatisch, ob Pflichtfelder im Request vorhanden sind. Wenn zum Beispiel `content` oder `category` beim Erstellen einer Notiz fehlt, antwortet die API mit `422 Unprocessable Entity`.

Tags werden zusaetzlich normalisiert:

- Leerzeichen am Anfang und Ende werden entfernt
- Tags werden klein geschrieben
- doppelte Tags werden entfernt
- Tags muessen mindestens zwei Zeichen lang sein
- pro Notiz sind maximal zehn Tags erlaubt

### Migration aus JSON

Beim Start liest `main.py` optional `data/notes.json` ein. Wenn die Datenbank noch leer ist, werden diese Beispiel-Notizen in `notes.db` uebernommen.

### Streamlit-Frontend

`frontend.py` ruft die FastAPI unter `http://127.0.0.1:8000` auf. Damit das Frontend funktioniert, muss das Backend also parallel laufen.
