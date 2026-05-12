"""
- Streamlit Installieren
- Streamlit App "Hello, World!" erstellen und testen
- "Say no" - App als ersten Test erstellen
  - API Documentation: https://github.com/hotheadhacker/no-as-a-service
  - API Endpoint: https://naas.isalman.dev/no
  - Button in Streamlit, der bei Klick eine Anfrage an den API Endpoint sendet und die Antwort anzeigt

- Todos für Nachmittag:
  - Streamlit App mit 2 Funktionen von Notizen API
  - Funktion 1: Alle Notizen anzeigen
    - Liste von Titeln von Notizen anzeigen
    - Möglichkeit zu einem Titel den Inhalt, Tags, Category, etc. anzuzeigen
  - Funktion 2: Neue Notiz erstellen (Formular mit Titel und Inhalt, Button)
    - Erstellen einer neuen Notiz (Titel, Inhalt, Tags, Category)
    - Neu erstellte Notiz soll in Liste auftauchen

"""
import streamlit as st
import requests

 
URL = "https://naas.isalman.dev/no"
 
def request_no():
    response = requests.get(URL)
    response_json = response.json()
    return response_json["reason"]
 
 
#Initialisierung
if "text1" not in st.session_state:
    st.session_state["text1"] = "value1"
    print("init Text1")
 
if "text2" not in st.session_state:
    st.session_state["text2"] = "value2"
    print("init Text2")
 
name = st.text_input("Name", placeholder="Enter your name") #Daten in Streamlit bekommen
st.write(name)
 
if st.button("Neuer Text1"):
    st.session_state["text1"]=request_no()
 
st.write(st.session_state["text1"])
 
if st.button("Neuer Text2"):
    st.session_state["text2"]=request_no()
 
 
st.write(st.session_state["text2"])
 
 
with st.expander("Session state"):
    st.write(st.session_state)
 
 


####### Hausaufgabe 11.05 #######

API_URL = "http://127.0.0.1:8000"
NOTE_CATEGORIES = ["work", "personal", "school", "ideas", "general"]


def load_notes():
    # Holt alle Notizen aus der FastAPI Notes API.
    response = requests.get(f"{API_URL}/notes", timeout=5)
    response.raise_for_status()
    return response.json()


def create_note(title, content, category, tags):
    # Erstellt eine neue Notiz in der FastAPI Notes API.
    payload = {
        "title": title,
        "content": content,
        "category": category,
        "tags": tags
    }
    response = requests.post(f"{API_URL}/notes", json=payload, timeout=5)
    return response


def parse_tags(tags_text):
    # Aus "tag1, tag2" wird eine Liste ohne leere Eintraege.
    tags = []
    for tag in tags_text.split(","):
        clean_tag = tag.strip().lower()
        if clean_tag:
            tags.append(clean_tag)
    return tags


st.divider()
st.header("Notes API")

if "note_created_message" in st.session_state:
    st.success(st.session_state.pop("note_created_message"))


try:
    notes = load_notes()
except requests.exceptions.RequestException as error:
    notes = []
    st.error(f"Notes API nicht erreichbar: {error}")


st.subheader("Alle Notizen")

if notes:
    selected_note = st.selectbox(
        "Notiz auswaehlen",
        notes,
        format_func=lambda note: note["title"]
    )
    
    st.write(f"**Titel:** {selected_note['title']}")
    st.write(f"**Inhalt:** {selected_note['content']}")
    st.write(f"**Kategorie:** {selected_note['category']}")
    st.write(f"**Tags:** {', '.join(selected_note['tags']) if selected_note['tags'] else '-'}")
    st.write(f"**Erstellt:** {selected_note['created_at']}")
    st.write(f"**ID:** {selected_note['id']}")
else:
    st.info("Noch keine Notizen vorhanden.")


st.subheader("Neue Notiz erstellen")

with st.form("create_note_form"):
    new_title = st.text_input("Titel")
    new_content = st.text_area("Inhalt")
    new_category = st.selectbox("Kategorie", NOTE_CATEGORIES, index=4)
    new_tags_text = st.text_input("Tags", placeholder="z.B. school, exam")
    submitted = st.form_submit_button("Notiz erstellen")
    
    if submitted:
        new_tags = parse_tags(new_tags_text)
        
        if not new_title.strip() or not new_content.strip():
            st.error("Titel und Inhalt duerfen nicht leer sein.")
        else:
            response = create_note(
                title=new_title.strip(),
                content=new_content.strip(),
                category=new_category,
                tags=new_tags
            )
            
            if response.status_code == 201:
                st.session_state["note_created_message"] = "Neue Notiz wurde erstellt."
                st.rerun()
            else:
                st.error(f"Notiz konnte nicht erstellt werden: {response.text}")