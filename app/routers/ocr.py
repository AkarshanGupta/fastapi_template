"""
OCR endpoints (requires ENABLE_OCR feature flag).
"""
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel
from typing import Dict, Any

from app.dependencies import get_settings, Settings
from app.decorators import feature_guard

router = APIRouter()


class OCRRequest(BaseModel):
    """OCR request model."""
    image_url: str = None
    language: str = "eng"


class OCRResponse(BaseModel):
    """OCR response model."""
    text: str
    confidence: float
    provider: str


@router.post("/ocr/process", response_model=OCRResponse)
async def process_ocr(
    file: UploadFile = File(...),
    settings: Settings = Depends(get_settings)
) -> Dict[str, Any]:
    """
    Process OCR on uploaded image file.
    
    Args:
        file: Uploaded image file
        settings: Application settings
        
    Returns:
        OCR result with extracted text
        
    Raises:
        HTTPException: If OCR feature is not enabled
    """
    # Check feature flag
    feature_guard(settings, "ENABLE_OCR")
    
    # Lazy import OCR service
    try:
        from app.services.ocr_service import process_image_ocr
    except ImportError:
        raise HTTPException(
            status_code=503,
            detail="OCR service is not available (dependencies not installed)"
        )
    
    # Read file content
    contents = await file.read()
    
    # Process OCR
    result = await process_image_ocr(contents, settings)
    
    return result


@router.get("/ocr/status")
async def ocr_status(settings: Settings = Depends(get_settings)) -> Dict[str, Any]:
    """
    Get OCR service status.
    
    Args:
        settings: Application settings
        
    Returns:
        OCR service status information
        
    Raises:
        HTTPException: If OCR feature is not enabled
    """
    # Check feature flag
    feature_guard(settings, "ENABLE_OCR")
    
    return {
        "enabled": True,
        "provider": settings.OCR_PROVIDER,
        "status": "ready"
    }


