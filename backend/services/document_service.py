"""
Document service for file upload and management.
"""

import hashlib
import os
import uuid
from pathlib import Path
from uuid import UUID

import aiofiles
from fastapi import UploadFile
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from models.document import Document
from schemas.document import DocumentResponse, DocumentListResponse


class DocumentService:
    """Service class for document-related operations."""

    def __init__(self, db: AsyncSession) -> None:
        """
        Initialize the document service.

        Args:
            db: Async database session.
        """
        self.db = db
        self.upload_dir = Path(settings.upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def upload_document(
        self,
        file: UploadFile,
        user_id: UUID,
    ) -> Document:
        """
        Upload and store a document.

        Args:
            file: The uploaded file.
            user_id: The ID of the user uploading the file.

        Returns:
            The created Document object.

        Raises:
            ValueError: If the file type is not allowed.
        """
        # Validate file extension
        original_filename = file.filename or "unnamed"
        file_ext = original_filename.rsplit(".", 1)[-1].lower()

        if file_ext not in settings.allowed_extensions:
            raise ValueError(
                f"File type '{file_ext}' not allowed. "
                f"Allowed: {settings.allowed_extensions}"
            )

        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}_{original_filename}"
        user_dir = self.upload_dir / str(user_id)
        user_dir.mkdir(parents=True, exist_ok=True)
        file_path = user_dir / unique_filename

        # Read file content and calculate hash
        content = await file.read()
        content_hash = hashlib.sha256(content).hexdigest()
        file_size = len(content)

        # Check file size limit
        max_size_bytes = settings.max_upload_size_mb * 1024 * 1024
        if file_size > max_size_bytes:
            raise ValueError(
                f"File size exceeds maximum allowed "
                f"({settings.max_upload_size_mb}MB)"
            )

        # Save file to disk
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)

        # Create database record
        document = Document(
            user_id=user_id,
            filename=unique_filename,
            original_filename=original_filename,
            file_type=file_ext,
            file_path=str(file_path),
            file_size=file_size,
            content_hash=content_hash,
        )

        self.db.add(document)
        await self.db.commit()
        await self.db.refresh(document)

        return document

    async def get_document(
        self,
        document_id: UUID,
        user_id: UUID,
    ) -> Document | None:
        """
        Get a document by ID for a specific user.

        Args:
            document_id: The document UUID.
            user_id: The user's UUID.

        Returns:
            The Document object if found and owned by user, None otherwise.
        """
        result = await self.db.execute(
            select(Document).where(
                Document.id == document_id,
                Document.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_documents_by_ids(
        self,
        document_ids: list[UUID],
        user_id: UUID,
    ) -> list[Document]:
        """
        Get multiple documents by their IDs for a specific user.

        Args:
            document_ids: List of document UUIDs.
            user_id: The user's UUID.

        Returns:
            List of Document objects owned by the user.
        """
        result = await self.db.execute(
            select(Document).where(
                Document.id.in_(document_ids),
                Document.user_id == user_id,
            )
        )
        return list(result.scalars().all())

    async def list_documents(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> DocumentListResponse:
        """
        List all documents for a user.

        Args:
            user_id: The user's UUID.
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            DocumentListResponse with documents and total count.
        """
        # Get total count
        count_result = await self.db.execute(
            select(func.count()).select_from(Document).where(
                Document.user_id == user_id
            )
        )
        total = count_result.scalar_one()

        # Get documents
        result = await self.db.execute(
            select(Document)
            .where(Document.user_id == user_id)
            .order_by(Document.uploaded_at.desc())
            .offset(skip)
            .limit(limit)
        )
        documents = result.scalars().all()

        return DocumentListResponse(
            documents=[
                DocumentResponse.model_validate(doc) for doc in documents
            ],
            total=total,
        )

    async def delete_document(
        self,
        document_id: UUID,
        user_id: UUID,
    ) -> bool:
        """
        Delete a document.

        Args:
            document_id: The document UUID.
            user_id: The user's UUID.

        Returns:
            True if deleted, False if not found.
        """
        document = await self.get_document(document_id, user_id)
        if not document:
            return False

        # Delete file from disk
        file_path = Path(document.file_path)
        if file_path.exists():
            file_path.unlink()

        # Delete from database
        await self.db.delete(document)
        await self.db.commit()

        return True
