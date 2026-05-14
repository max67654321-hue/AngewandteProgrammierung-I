import requests
import streamlit as st


API_BASE_URL = "http://127.0.0.1:8000"
NO_API_URL = "https://naas.isalman.dev/no"
CATEGORIES = ["general", "work", "personal", "school", "ideas"]


def get_no_text():
    response = requests.get(NO_API_URL)
    data = response.json()
    return data["reason"]


def get_notes():
    response = requests.get(f"{API_BASE_URL}/notes", timeout=5)
    response.raise_for_status()
    return response.json()


def get_note(note_id):
    response = requests.get(f"{API_BASE_URL}/notes/{note_id}", timeout=5)
    if response.status_code == 200:
        return response.json()
    return None


def add_note(title, content, category, tags):
    note_payload = {
        "title": title,
        "content": content,
        "category": category,
        "tags": tags,
    }
    return requests.post(f"{API_BASE_URL}/notes", json=note_payload, timeout=5)


def text_to_tags(tags_text):
    tags = []

    for tag in tags_text.split(","):
        tag = tag.strip().lower()
        if tag:
            tags.append(tag)

    return tags


st.set_page_config(page_title="Notizen Frontend")
st.title("Notizen Frontend")


if "text1" not in st.session_state:
    st.session_state["text1"] = "value1"
    print("init Text1")

if "text2" not in st.session_state:
    st.session_state["text2"] = "value2"
    print("init Text2")


st.header("Say No App")

name = st.text_input("Name", placeholder="Name eingeben")
st.write(name)

if st.button("Text 1 aktualisieren"):
    st.session_state["text1"] = get_no_text()

st.write(st.session_state["text1"])

if st.button("Text 2 aktualisieren"):
    st.session_state["text2"] = get_no_text()

st.write(st.session_state["text2"])

with st.expander("Session State anzeigen"):
    st.write(st.session_state)


st.header("Neue Notiz erstellen")

with st.form("note_form"):
    title = st.text_input("Titel")
    content = st.text_area("Inhalt")
    category = st.selectbox("Kategorie", CATEGORIES)
    tags_text = st.text_input("Tags", placeholder="z.B. uni, test")

    save_clicked = st.form_submit_button("Speichern")

if save_clicked:
    tags = text_to_tags(tags_text)

    if title.strip() == "" or content.strip() == "":
        st.error("Titel und Inhalt müssen ausgefüllt sein.")
    else:
        response = add_note(title.strip(), content.strip(), category, tags)

        if response.status_code == 201:
            st.success("Notiz wurde erstellt.")
        else:
            st.error("Notiz konnte nicht erstellt werden.")
            st.write(response.text)


st.header("Notizen anzeigen")

try:
    notes = get_notes()
except Exception as error:
    notes = []
    st.error("API konnte nicht erreicht werden.")
    st.write(error)


if not notes:
    st.info("Keine Notizen gefunden.")
else:
    note_choices = {}

    for note in notes:
        label = f"{note['title']} (ID: {note['id']})"
        note_choices[label] = note["id"]

    selected_label = st.selectbox("Notiz auswählen", list(note_choices.keys()))
    selected_id = note_choices[selected_label]
    selected_note = get_note(selected_id)

    if selected_note:
        st.subheader(selected_note["title"])

        st.write("**Inhalt:**")
        st.write(selected_note["content"])

        st.write("**Kategorie:**")
        st.write(selected_note["category"])

        st.write("**Tags:**")
        if selected_note["tags"]:
            st.write(", ".join(selected_note["tags"]))
        else:
            st.write("-")

        st.write("**ID:**")
        st.write(selected_note["id"])

        if "created_at" in selected_note:
            st.write("**Erstellt:**")
            st.write(selected_note["created_at"])
