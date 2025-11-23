"""
Items CRUD endpoints (works without database).
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.dependencies import get_settings, Settings

router = APIRouter()


# In-memory storage (for demo purposes, works without DB)
_items_storage: Dict[int, Dict[str, Any]] = {}
_next_id = 1


class ItemCreate(BaseModel):
    """Item creation model."""
    name: str
    description: Optional[str] = None
    price: float


class ItemUpdate(BaseModel):
    """Item update model."""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


class ItemResponse(BaseModel):
    """Item response model."""
    id: int
    name: str
    description: Optional[str]
    price: float
    created_at: str


@router.get("/items", response_model=List[ItemResponse])
async def list_items(settings: Settings = Depends(get_settings)) -> List[Dict[str, Any]]:
    """
    List all items.
    
    Args:
        settings: Application settings
        
    Returns:
        List of items
    """
    return list(_items_storage.values())


@router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int,
    settings: Settings = Depends(get_settings)
) -> Dict[str, Any]:
    """
    Get a specific item by ID.
    
    Args:
        item_id: Item identifier
        settings: Application settings
        
    Returns:
        Item data
        
    Raises:
        HTTPException: If item not found
    """
    if item_id not in _items_storage:
        raise HTTPException(status_code=404, detail="Item not found")
    return _items_storage[item_id]


@router.post("/items", response_model=ItemResponse, status_code=201)
async def create_item(
    item: ItemCreate,
    settings: Settings = Depends(get_settings)
) -> Dict[str, Any]:
    """
    Create a new item.
    
    Args:
        item: Item data
        settings: Application settings
        
    Returns:
        Created item
    """
    global _next_id
    
    new_item = {
        "id": _next_id,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "created_at": datetime.utcnow().isoformat(),
    }
    
    _items_storage[_next_id] = new_item
    _next_id += 1
    
    return new_item


@router.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item_update: ItemUpdate,
    settings: Settings = Depends(get_settings)
) -> Dict[str, Any]:
    """
    Update an existing item.
    
    Args:
        item_id: Item identifier
        item_update: Updated item data
        settings: Application settings
        
    Returns:
        Updated item
        
    Raises:
        HTTPException: If item not found
    """
    if item_id not in _items_storage:
        raise HTTPException(status_code=404, detail="Item not found")
    
    existing_item = _items_storage[item_id]
    
    if item_update.name is not None:
        existing_item["name"] = item_update.name
    if item_update.description is not None:
        existing_item["description"] = item_update.description
    if item_update.price is not None:
        existing_item["price"] = item_update.price
    
    return existing_item


@router.delete("/items/{item_id}", status_code=204)
async def delete_item(
    item_id: int,
    settings: Settings = Depends(get_settings)
) -> None:
    """
    Delete an item.
    
    Args:
        item_id: Item identifier
        settings: Application settings
        
    Raises:
        HTTPException: If item not found
    """
    if item_id not in _items_storage:
        raise HTTPException(status_code=404, detail="Item not found")
    
    del _items_storage[item_id]

