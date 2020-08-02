from secrets import token_hex
from typing import Dict

from fastapi import APIRouter, Depends
from passlib.hash import bcrypt
from pydantic import BaseModel, Field

from .. import models
from ..database import DBAdmin
from ..dependencies import admin_api_key_query, db_admin_conn

router = APIRouter()


class KeyRequest(BaseModel):
    can_create_tokens: bool = Field(False)


@router.post("/create_key", response_model=models.AdministrationCreateKeyResponse)
async def create_key(
    key_request: KeyRequest,
    api_key: str = Depends(admin_api_key_query),
    db: DBAdmin = Depends(db_admin_conn),
):

    doc_count: int = await db.count("api_keys")
    new_identifier: int = doc_count + 1
    new_key: str = token_hex(16)
    new_key_hash: str = bcrypt.using(rounds=12).hash(new_key)
    can_create_tokens = key_request.can_create_tokens
    created_by: int = int(api_key.split("-")[0])

    new_doc: Dict = {
        "identifier": new_identifier,
        "hash": new_key_hash,
        "can_create_token": can_create_tokens,
        "created_by": created_by,
    }

    await db.insert("api_keys", new_doc)
    new_api_key = f"{new_identifier}-{new_key}"

    new_doc.pop("_id")
    new_doc.pop("hash")
    new_doc.update({"new_api_key": new_api_key})
    return new_doc
