from fastapi import APIRouter, Depends, Path, Request, Response, HTTPException
from api.base.base_schemas import BaseResponse, PaginationParams
from middlewares.authentication import get_user_id_from_access_token

from .schemas import (
    CreateNoteRequest, 
    CreateNoteResponse,
    ReadOneNoteResponse,
    NotePaginationResponse,
    ReadAllNoteResponse,
    UpdateNoteRequest,
    UpdateNoteResponse,
    DeleteNoteResponse
)
from .use_cases import CreateNote, ReadOneNote, UpdateNote, DeleteNote, ReadAllNote

router = APIRouter(prefix="/notes")
tag = "Notes"

@router.post("", response_model = CreateNoteResponse, tags = [tag])
async def create(
    request: Request,
    response: Response,
    data: CreateNoteRequest,
    token_user_id: int = Depends(get_user_id_from_access_token),
    create_note: CreateNote = Depends(CreateNote)
) -> CreateNoteResponse:
    try:
        resp_data = await create_note.execute(user_id = token_user_id, request = data)

        return CreateNoteResponse(
            status="success",
            message="succes adding new note",
            data=resp_data
        )
    except HTTPException as ex:
        response.status_code = ex.status_code
        return CreateNoteResponse(
            status="error",
            message=ex.detail
        )
    except Exception as e:
        response.status_code = 500
        message = "failed to add a new note"
        if hasattr(e,'message'):
            message = e.message
        elif hasattr(e,'detail'):
            message = e.detail

        return CreateNoteResponse(
            status="error",
            message=message
        )

@router.get("/{note_id}", response_model=ReadOneNoteResponse, tags=[tag])
async def read(
    request: Request,
    response: Response,
    token_user_id: int = Depends(get_user_id_from_access_token),
    note_id: int = Path(...,description=""),
    read_one: ReadOneNote = Depends(ReadOneNote)
) -> ReadOneNoteResponse:
    try:
        resp_data = await read_one.execute(user_id=token_user_id, note_id=note_id)

        return ReadOneNoteResponse(
            status="success",
            message="success reading a note",
            data=resp_data
        )
    except HTTPException as ex:
        response.status_code = ex.status_code
        return ReadOneNoteResponse(
            status="error",
            message=ex.detail,
        )
    except Exception as e:
        response.status_code = 500
        message = "failed to read user"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail

        return ReadOneNoteResponse(
            status="error",
            message=message,
        )

@router.get("", response_model=ReadAllNoteResponse, tags=[tag])
async def read_all(
    request: Request,
    response: Response,
    token_user_id: int = Depends(get_user_id_from_access_token),
    filter_user: bool = True,
    include_deleted: bool = False,
    page_params: PaginationParams = Depends(),
    read_all: ReadAllNote = Depends(ReadAllNote)
) -> ReadAllNoteResponse:
    print(token_user_id, filter_user,include_deleted,page_params)
    try:
        resp_data = await read_all.execute(
            user_id = token_user_id,
            filter_user = filter_user,
            include_deleted = include_deleted,
            page_params = page_params
        )

        return ReadAllNoteResponse(
            status="success",
            message="success read users",
            data=NotePaginationResponse(records=resp_data[0], meta=resp_data[1]),
        )

    except HTTPException as ex:
        response.status_code = ex.status_code
        return ReadAllNoteResponse(
            status="error",
            message=ex.detail,
        )
    except Exception as e:
        response.status_code = 500
        message = "failed to read notes"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail

        return ReadAllNoteResponse(
            status="error",
            message=message,
        )

@router.put("/{note_id}", response_model=UpdateNoteResponse, tags=[tag])
async def update(
    request: Request,
    response: Response,
    data: UpdateNoteRequest,
    token_user_id: int = Depends(get_user_id_from_access_token),
    note_id: int = Path(...,description=""),
    update_note: UpdateNote = Depends(UpdateNote)
) -> UpdateNoteResponse :
    try:
        resp_data = await update_note.execute(user_id=token_user_id, note_id=note_id, request=data)
        
        print(resp_data)
        return UpdateNoteResponse(
            status="success",
            message="success update note",
            data=resp_data,
        )
    except HTTPException as ex:
        response.status_code = ex.status_code
        return UpdateNoteResponse(
            status="error",
            message=ex.detail,
        )
    except Exception as e:
        response.status_code = 500
        message="failed to update note"
        if hasattr(e, 'message'):
            message = e.message
        elif hasattr(e, 'detail'):
            message = e.detail

        return UpdateNoteResponse(
            status="error",
            message=message,
        )

@router.delete("/{note_id}", response_model=DeleteNoteResponse, tags=[tag])
async def delete(
    request: Request,
    response: Response,
    token_user_id: int = Depends(get_user_id_from_access_token),
    note_id: int = Path(...,description=""),
    delete_note: DeleteNote = Depends(DeleteNote)
) -> DeleteNoteResponse:
    try:
        resp_data = await delete_note.execute(user_id=token_user_id, note_id=note_id)

        return DeleteNoteResponse(
            status="success",
            message="success deleting note",
            data=resp_data,
        )
    except HTTPException as ex:
        response.status_code = ex.status_code
        return DeleteNoteResponse(
            status="error",
            message=ex.detail,
        )
    except Exception as e:
        response.status_code = 500
        message = "failed to delete note"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail
        return DeleteNoteResponse(
            status="error",
            message=message,
        )