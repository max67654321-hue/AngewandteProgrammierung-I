import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


def get_notes():
    response = requests.get(f"{API_URL}/notes")
    response.raise_for_status()
    return response.json()


def create_note(title, content, category, tags):
    payload = {
        "title": title,
        "content": content,
        "category": category,
        "tags": tags,
    }
    response = requests.post(f"{API_URL}/notes", json=payload)
    return response


def parse_tags(tags_text):
    tags = []
    for tag in tags_text.split(","):
        clean_tag = tag.strip()
        if clean_tag:
            tags.append(clean_tag)
    return tags


st.title("Notizen App")


st.header("Alle Notizen")

try:
    notes = get_notes()
except requests.exceptions.RequestException as error:
    notes = []
    st.error(f"API nicht erreichbar: {error}")

if notes:
    note_titles = [note["title"] for note in notes]
    selected_title = st.selectbox("Notiz auswählen", note_titles)

    selected_note = None
    for note in notes:
        if note["title"] == selected_title:
            selected_note = note
            break

    if selected_note:
        st.write("Titel:", selected_note["title"])
        st.write("Inhalt:", selected_note["content"])
        st.write("Kategorie:", selected_note["category"])
        st.write("Tags:", ", ".join(selected_note["tags"]))
        st.write("ID:", selected_note["id"])
else:
    st.info("Keine Notizen vorhanden.")


st.header("Neue Notiz erstellen")

with st.form("create_note_form"):
    title = st.text_input("Titel")
    content = st.text_area("Inhalt")
    category = st.text_input("Kategorie", value="general")
    tags_text = st.text_input("Tags", placeholder="z.B. uni, test")

    submitted = st.form_submit_button("Erstellen")

if submitted:
    tags = parse_tags(tags_text)

    if not title or not content or not category:
        st.error("Titel, Inhalt und Kategorie dürfen nicht leer sein.")
    else:
        response = create_note(title, content, category, tags)

        if response.status_code == 201:
            st.success("Notiz wurde erstellt.")
            st.rerun()
        else:
            st.error(f"Fehler: {response.text}")
