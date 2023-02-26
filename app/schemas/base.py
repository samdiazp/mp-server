from typing import Any
from pydantic import BaseModel

class BasicResponse(BaseModel):
    ok: bool
    data: Any
