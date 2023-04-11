from pydantic import BaseModel


class Photo(BaseModel):
    id: str
    title: str
    src: str
    thumbnail: str
    uploaded_at: str
