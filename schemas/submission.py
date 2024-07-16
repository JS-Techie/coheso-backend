from datetime import datetime
import uuid

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class FieldDataBody(BaseModel):
    field_id: str = Field(default_factory=lambda: f"field--{uuid.uuid4()}")
    value: list[str]

class SubmissionRequestBody(BaseModel):
    submission_id: str
    form_version_id: str = Field(default_factory=lambda: f"form--{uuid.uuid4()}")
    data: list[FieldDataBody]
    createdOn: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + 'Z')