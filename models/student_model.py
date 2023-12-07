from datetime import datetime
from pydantic import BaseModel, Required

class UserModel(BaseModel):
    user_sub: Required[str]
    last_modified: datetime = datetime.utcnow()


