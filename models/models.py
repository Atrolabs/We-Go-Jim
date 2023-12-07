from datetime import datetime
from pydantic import BaseModel

class UserModel(BaseModel):
    user_sub: str
    last_modified: str = str(datetime.utcnow())
