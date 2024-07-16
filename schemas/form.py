from datetime import datetime
import uuid

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class CustomFieldDataRequestBody(BaseModel):
    field_id: str
    field_label: str
    field_type: str
    placeholder: Optional[str] = None
    required: bool
    options: Optional[List[Dict[str, str]]] = None


class FormDataRequestBody(BaseModel):
    form_id: str = Field(default_factory=lambda: f"form-{uuid.uuid4()}")
    version: str
    form_version_id: str = Field(default_factory=lambda: f"form--{uuid.uuid4()}--{FormDataRequestBody.version}")
    form_name: str
    form_description: str
    form_owner: str
    created_on: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + 'Z')
    fields: List[CustomFieldDataRequestBody]

