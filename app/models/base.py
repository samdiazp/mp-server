from sqlalchemy import inspect
from datetime import datetime
from sqlalchemy import DateTime, Column


class BaseModel:
    created_at: datetime = Column(DateTime, default=datetime.now)
    updated_at: datetime = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    def as_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
