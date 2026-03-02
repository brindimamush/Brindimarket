from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel, JSON
from pydantic import EmailStr

class Tenant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    slug: str = Field(unique=True, index=True)
    logo_url: Optional[str] = None
    primary_color: str = Field(default="#000000")
    domain: Optional[str] = None
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, index=True)
    hashed_password: str
    full_name: Optional[str] = None
    role: str = Field(default="customer") # admin, super_admin, customer
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    slug: str = Field(unique=True, index=True)
    parent_id: Optional[int] = Field(default=None, foreign_key="category.id")
    metadata: Optional[dict] = Field(default_factory=dict, sa_type=JSON)
    
    products: List["Product"] = Relationship(back_populates="category")

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    brand: Optional[str] = None
    description: Optional[str] = None
    category_id: int = Field(foreign_key="category.id")
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    category: Optional[Category] = Relationship(back_populates="products")
    variants: List["ProductVariant"] = Relationship(back_populates="product")

class ProductVariant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    sku: str = Field(unique=True, index=True)
    price: float
    stock: int = Field(default=0)
    weight: Optional[float] = None
    
    product: Optional[Product] = Relationship(back_populates="variants")
    order_items: List["OrderItem"] = Relationship(back_populates="variant")

class Attribute(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str # e.g., "Color", "Size"
    type: str

class AttributeValue(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    attribute_id: int = Field(foreign_key="attribute.id")
    variant_id: int = Field(foreign_key="productvariant.id")
    value: str

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    status: str = Field(default="pending") # pending, paid, shipped, delivered, cancelled
    total_amount: float
    currency: str = Field(default="ETB")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    items: List["OrderItem"] = Relationship(back_populates="order")

class OrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id")
    variant_id: int = Field(foreign_key="productvariant.id")
    quantity: int = Field(default=1)
    price_at_purchase: float
    
    order: Optional[Order] = Relationship(back_populates="items")
    variant: Optional[ProductVariant] = Relationship(back_populates="order_items")
