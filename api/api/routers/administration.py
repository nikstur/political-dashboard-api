import os
from datetime import datetime, timezone
from secrets import token_hex
from typing import Dict, List, Optional, Tuple

from fastapi import APIRouter, Depends
from passlib.hash import bcrypt
from pydantic import BaseModel, Field
from starlette.exceptions import HTTPException
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from .. import models
from ..database import DBAdmin
from ..dependencies import admin_api_key_query, db_admin_conn

router = APIRouter()

DEV_CONFIG = bool(int(os.getenv("PDA_DEV_CONFIG", 0)))


class KeyRequestAdd(BaseModel):
    can_create_tokens: bool = Field(False)


@router.post(
    "/add_key",
    response_model=models.AdministrationAddKeyResponse,
    include_in_schema=DEV_CONFIG,
)
async def add_key(
    key_request_add: KeyRequestAdd,
    api_key: str = Depends(admin_api_key_query),
    db: DBAdmin = Depends(db_admin_conn),
):
    doc_count: int = await db.count("api_keys")
    new_identifier: int = doc_count + 1
    new_key_hash, new_api_key = generate_new_api_key(new_identifier)
    can_create_tokens = key_request_add.can_create_tokens
    created_by: int = int(api_key.split("-")[0])
    creation_date: datetime = datetime.now(timezone.utc)
    new_doc: Dict = {
        "_id": new_identifier,
        "hash": new_key_hash,
        "can_create_token": can_create_tokens,
        "created_by": created_by,
        "creation_date": creation_date,
    }
    response = await db.insert("api_keys", new_doc)

    response.pop("hash")
    response.update({"new_api_key": new_api_key})
    return response


def generate_new_api_key(new_identifier: int) -> Tuple[str, str]:
    new_key: str = token_hex(16)
    new_key_hash: str = bcrypt.using(rounds=12).hash(new_key)
    new_api_key: str = f"{new_identifier}-{new_key}"
    return (new_key_hash, new_api_key)


class KeyRequestDelete(BaseModel):
    identifier: int = Field(..., example=5)


@router.post(
    "/remove_key",
    response_model=models.AdministrationKeyResponse,
    include_in_schema=DEV_CONFIG,
)
async def remove_key(
    key_request_delete: KeyRequestDelete,
    api_key: str = Depends(admin_api_key_query),
    db: DBAdmin = Depends(db_admin_conn),
):
    identifier: int = key_request_delete.identifier
    if identifier in (1, 2):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Insufficient rights to access this resource",
        )
    else:
        doc: Optional[Dict] = await db.delete("api_keys", identifier)
        if doc:
            return doc
        else:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail="Resource does not exist"
            )


@router.get(
    "/keys",
    response_model=List[models.AdministrationKeyResponse],
    include_in_schema=DEV_CONFIG,
)
async def keys(
    api_key: str = Depends(admin_api_key_query), db: DBAdmin = Depends(db_admin_conn)
):
    docs: List[Dict] = await db.get_all("api_keys")
    return docs
