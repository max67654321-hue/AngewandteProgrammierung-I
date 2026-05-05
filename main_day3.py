

from datetime import datetime
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel, Session, create_engine, select, col, or_


###############################
### Database Models
###############################

class NoteTag(SQLModel, table=True):
    note_id: int | None = Field(default=None, foreign_key="note.id", primary_key=True)
    tag_id: int | None = Field(default=None, foreign_key="tag.id", primary_key=True)


class Tag(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

    notes: list["Note"] = Relationship(back_populates="tags", link_model=NoteTag)


class Note(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str
    category: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    tags: list[Tag] = Relationship(back_populates="notes", link_model=NoteTag)


engine = create_engine("sqlite:///notes.db")
SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


###############################
### FastAPI App
###############################

app = FastAPI(
    title="Note API Day 3",
    description="Note API with SQLite + SQLModel",
    version="2.0.0",
)


###############################
### API Models
###############################

class NoteCreate(BaseModel):
    title: str
    content: str
    category: str
    tags: list[str] = []


class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    category: str | None = None
    tags: list[str] | None = None


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: list[str]
    created_at: str

    class Config:
        from_attributes = True


###############################
### Helper Functions
###############################

def get_or_create_tags(tag_names: list[str], session: Session) -> list[Tag]:
    tag_objects = []
    seen = set()

    for tag_name in tag_names:
        tag_lower = tag_name.lower().strip()

        if not tag_lower or tag_lower in seen:
            continue

        seen.add(tag_lower)

        stmt = select(Tag).where(Tag.name == tag_lower)
        existing = session.exec(stmt).first()

        if existing:
            tag_objects.append(existing)
        else:
            new_tag = Tag(name=tag_lower)
            session.add(new_tag)
            tag_objects.append(new_tag)

    return tag_objects


def to_response(note: Note) -> NoteResponse:
    return NoteResponse(
        id=note.id,
        title=note.title,
        content=note.content,
        category=note.category,
        tags=[t.name for t in note.tags],
        created_at=note.created_at.isoformat(),
    )


###############################
### CRUD Endpoints
###############################

@app.post("/notes", status_code=201)
def create_note(note: NoteCreate, session: SessionDep) -> NoteResponse:
    db_note = Note(
        title=note.title,
        content=note.content,
        category=note.category,
    )

    db_note.tags = get_or_create_tags(note.tags, session)

    session.add(db_note)
    session.commit()
    session.refresh(db_note)

    return to_response(db_note)


@app.get("/notes")
def list_notes(
    session: SessionDep,
    category: str = None,
    search: str = None,
    tag: str = None,
    created_after: str = None,
    created_before: str = None,
) -> list[NoteResponse]:

    stmt = select(Note)

    if category:
        stmt = stmt.where(Note.category == category)

    if search:
        s = search.lower()
        stmt = stmt.where(
            or_(
                col(Note.title).ilike(f"%{s}%"),
                col(Note.content).ilike(f"%{s}%"),
            )
        )

    if tag:
        stmt = stmt.join(Note.tags).where(Tag.name == tag.lower())

    notes = session.exec(stmt).all()

    result = []
    for n in notes:
        created = n.created_at.isoformat()

        if created_after and created < created_after:
            continue

        if created_before and created > created_before:
            continue

        result.append(n)

    return [to_response(n) for n in result]


@app.get("/notes/{note_id}")
def get_note(note_id: int, session: SessionDep) -> NoteResponse:
    note = session.get(Note, note_id)

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return to_response(note)


@app.put("/notes/{note_id}")
def update_note(note_id: int, note_update: NoteCreate, session: SessionDep) -> NoteResponse:
    note = session.get(Note, note_id)

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note.title = note_update.title
    note.content = note_update.content
    note.category = note_update.category
    note.tags = get_or_create_tags(note_update.tags, session)

    session.add(note)
    session.commit()
    session.refresh(note)

    return to_response(note)


@app.patch("/notes/{note_id}")
def patch_note(note_id: int, note_update: NoteUpdate, session: SessionDep) -> NoteResponse:
    note = session.get(Note, note_id)

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    data = note_update.dict(exclude_unset=True)

    if "title" in data:
        note.title = data["title"]
    if "content" in data:
        note.content = data["content"]
    if "category" in data:
        note.category = data["category"]
    if "tags" in data:
        note.tags = get_or_create_tags(data["tags"], session)

    session.add(note)
    session.commit()
    session.refresh(note)

    return to_response(note)


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, session: SessionDep):
    note = session.get(Note, note_id)

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    session.delete(note)
    session.commit()


###############################
### Extra Endpoints
###############################

@app.get("/notes/stats")
def stats(session: SessionDep):
    notes = session.exec(select(Note)).all()

    cat = {}
    tags = {}

    for n in notes:
        cat[n.category] = cat.get(n.category, 0) + 1
        for t in n.tags:
            tags[t.name] = tags.get(t.name, 0) + 1

    top = [
        {"tag": k, "count": v}
        for k, v in sorted(tags.items(), key=lambda x: x[1], reverse=True)[:5]
    ]

    return {
        "total_notes": len(notes),
        "by_category": cat,
        "top_tags": top,
        "unique_tags_count": len(tags),
    }


@app.get("/tags")
def list_tags(session: SessionDep):
    return sorted([t.name for t in session.exec(select(Tag)).all()])


@app.get("/tags/{tag_name}/notes")
def notes_by_tag(tag_name: str, session: SessionDep):
    tag = session.exec(select(Tag).where(Tag.name == tag_name.lower())).first()

    if not tag:
        return []

    return [to_response(n) for n in tag.notes]


@app.get("/categories")
def categories(session: SessionDep):
    notes = session.exec(select(Note)).all()
    return sorted({n.category for n in notes})


@app.get("/categories/{category}/notes")
def notes_by_category(category: str, session: SessionDep):
    notes = session.exec(select(Note).where(Note.category == category)).all()
    return [to_response(n) for n in notes]