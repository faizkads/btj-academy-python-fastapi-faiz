from pydantic import BaseModel, Field, EmailStr
from api.base.base_schemas import BaseResponse, PaginationMetaResponse

from models.note import NoteSchema

class CreateNoteRequest(BaseModel):
    title: str = Field(...,min_length=1, max_length=255)
    content: str = Field(...,min_length=6, max_length=500)

class CreateNoteResponse(BaseResponse):
    data: NoteSchema | None

class ReadOneNoteResponse(BaseResponse):
    data: NoteSchema | None

class NotePaginationResponse(BaseModel):
    records: list[NoteSchema]
    meta: PaginationMetaResponse

class ReadAllNoteResponse(BaseResponse):
    data: NotePaginationResponse

class UpdateNoteRequest(BaseModel):
    title: str = Field(...,min_length=1, max_length=255)
    content: str = Field(...,min_length=6, max_length=500)

class UpdateNoteResponse(BaseResponse):
    data: NoteSchema | None

class DeleteNoteResponse(BaseResponse):
    data: NoteSchema | None