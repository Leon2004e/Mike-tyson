from pydantic import BaseModel
from typing import Optional, List

class Health(BaseModel):
    status: str = "ok"
