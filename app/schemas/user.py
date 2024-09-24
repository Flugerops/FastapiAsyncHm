from pydantic import BaseModel, ConfigDict
from typing import Optional


class UserData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    name: str