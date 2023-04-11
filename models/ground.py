from typing import List
from pydantic import BaseModel
import user


class Ground(BaseModel):
    id: str
    title: str
    maker: user.User
    photos: str
    expires_in: str
    current_people: List(user.User)
