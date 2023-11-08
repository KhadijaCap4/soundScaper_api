from fastapi import APIRouter, HTTPException
from typing import List
from classes.schemas_dto import Music, MusicNoID
import uuid

router= APIRouter(
    prefix='/musics',
    tags=["Musics"]
)

musics = [
    Music(id=uuid.uuid4(), title="GLAIVE", artist="Booba", label="Tallac Records", genre="Hip Hop"),
    Music(id=uuid.uuid4(), title="Shallow", artist="Lady Gaga & Bradley Cooper", label="Interscope", genre="Pop rock"),
    Music(id=uuid.uuid4(), title="DKR", artist="Booba", label="Tallac Records", genre="Hip Hop"),
    Music(id=uuid.uuid4(), title="Someone like you", artist="Columbia", label="Tallac Records", genre="Pop"),
    Music(id=uuid.uuid4(), title="92i Veyron", artist="Booba", label="Tallac Records", genre="Hip Hop"),
    Music(id=uuid.uuid4(), title="Aya Nakamura", artist="La dot", label="Parlophone", genre="Pop/R&B")
]

@router.get('', response_model=List[Music])
async def get_music():
    return musics

@router.post('', response_model=Music, status_code=201)
async def create_music(givenTitle: MusicNoID):
    generatedId = uuid.uuid4()
    newMusic = Music(id=generatedId, title=givenTitle.title, artist=givenTitle.artist, label=givenTitle.label, genre=givenTitle.genre)  # Use givenTitle.title to access the title
    musics.append(newMusic)
    return newMusic

@router.get('/{music_id}', response_model=Music)
async def get_music_by_ID(music_id: uuid.UUID):  # Change data type to uuid.UUID
    for music in musics:
        if music.id == music_id:
            return music
    raise HTTPException(status_code=404, detail="Music not found")

@router.patch('/{music_id}', status_code=204)
async def modify_music_title(music_id: uuid.UUID, modifiedMusic: MusicNoID):
    for music in musics:
        if music.id == music_id:
            music.title = modifiedMusic.title
            return
    raise HTTPException(status_code=404, detail="Music not found")

@router.delete('/{music_id}', status_code=204)
async def delete_music(music_id: uuid.UUID):  # Change data type to uuid.UUID
    for music in musics:
        if music.id == music_id:
            musics.remove(music)
            return
    raise HTTPException(status_code=404, detail="Music not found")
