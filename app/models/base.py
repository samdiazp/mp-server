from sqlalchemy import inspect

class BaseModel:
    def as_dict(self):
         return {c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs}