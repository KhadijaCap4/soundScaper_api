from fastapi import APIRouter, HTTPException
from typing import List
from classes.schemas_dto import Music, MusicNoID
import uuid

router= APIRouter(
    prefix='/musics',
    tags=["Musics"]
)

musics = [
    Music(id=uuid.uuid4(), title="GLAIVE"),
    Music(id=uuid.uuid4(), title="DKR"),
    Music(id=uuid.uuid4(), title="92i Veyron")
]

@router.get('/musics', response_model=List[Music])
async def get_music():
    return musics

@router.post('/musics', response_model=Music, status_code=201)
async def create_music(givenTitle: MusicNoID):
    generatedId = uuid.uuid4()
    newMusic = Music(id=generatedId, title=givenTitle.title)  # Use givenTitle.title to access the title
    musics.append(newMusic)
    return newMusic

@router.get('/musics/{music_id}', response_model=Music)
async def get_music_by_ID(music_id: uuid.UUID):  # Change data type to uuid.UUID
    for music in musics:
        if music.id == music_id:
            return music
    raise HTTPException(status_code=404, detail="Music not found")

@router.patch('/musics/{music_id}', status_code=204)
async def modify_music_title(music_id: uuid.UUID, modifiedMusic: MusicNoID):
    for music in musics:
        if music.id == music_id:
            music.title = modifiedMusic.title
            return
    raise HTTPException(status_code=404, detail="Music not found")

@router.delete('/musics/{music_id}', status_code=204)
async def delete_music(music_id: uuid.UUID):  # Change data type to uuid.UUID
    for music in musics:
        if music.id == music_id:
            musics.remove(music)
            return
    raise HTTPException(status_code=404, detail="Music not found")
