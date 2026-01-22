"""
Document upload and management API endpoints.
"""

from uuid import UUID

from fastapi import APIRouter, HTTPException, UploadFile, File, status

from core.dependencies import DbSession, CurrentUserId
from schemas.document import DocumentResponse, DocumentListResponse
from services.document_service import DocumentService

router = APIRouter()


@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
    user_id: CurrentUserId = None,
    db: DbSession = None,
) -> DocumentResponse:
    """
    Upload a document for compliance analysis.
    
    Accepts PDF, CSV, and JSON files up to 50MB.
    
    Args:
        file: The uploaded file.
        user_id: The authenticated user's ID.
        db: Database session.
    
    Returns:
        The created document information.
    
    Raises:
        HTTPException: If file type is invalid or file too large.
    """
    service = DocumentService(db)
    
    try:
        document = await service.upload_document(
            file=file,
            user_id=UUID(user_id),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    
    return DocumentResponse.model_validate(document)


@router.get("", response_model=DocumentListResponse)
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    user_id: CurrentUserId = None,
    db: DbSession = None,
) -> DocumentListResponse:
    """
    List all documents for the authenticated user.
    
    Args:
        skip: Number of records to skip (pagination).
        limit: Maximum number of records to return.
        user_id: The authenticated user's ID.
        db: Database session.
    
    Returns:
        List of documents with total count.
    """
    service = DocumentService(db)
    return await service.list_documents(
        user_id=UUID(user_id),
        skip=skip,
        limit=limit,
    )


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: UUID,
    user_id: CurrentUserId = None,
    db: DbSession = None,
) -> DocumentResponse:
    """
    Get a specific document by ID.
    
    Args:
        document_id: The document UUID.
        user_id: The authenticated user's ID.
        db: Database session.
    
    Returns:
        The document information.
    
    Raises:
        HTTPException: If document not found.
    """
    service = DocumentService(db)
    document = await service.get_document(
        document_id=document_id,
        user_id=UUID(user_id),
    )
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    
    return DocumentResponse.model_validate(document)


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: UUID,
    user_id: CurrentUserId = None,
    db: DbSession = None,
) -> None:
    """
    Delete a document.
    
    Args:
        document_id: The document UUID.
        user_id: The authenticated user's ID.
        db: Database session.
    
    Raises:
        HTTPException: If document not found.
    """
    service = DocumentService(db)
    deleted = await service.delete_document(
        document_id=document_id,
        user_id=UUID(user_id),
    )
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
