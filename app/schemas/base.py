from typing import Any, Optional
from pydantic import BaseModel

class BasicResponse(BaseModel):
    ok: bool
    data: Optional[Any] = None
