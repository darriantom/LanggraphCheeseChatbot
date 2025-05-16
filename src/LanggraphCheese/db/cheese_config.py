import os
from enum import Enum
from pydantic_settings import BaseSettings
from functools import lru_cache
from pydantic import BaseModel
from datetime import date
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Database settings
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_PORT: int
    PINECONE_INDEX: str
    
    class Config:
        case_sensitive = True

class CheeseData(BaseModel):
    showimage: Optional[str] = None
    name: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    itemcount_case: Optional[str] = None
    itemcount_each: Optional[str] = None
    dimension_case: Optional[str] = None
    dimension_each: Optional[str] = None
    weight_case: Optional[float] = None
    weight_each: Optional[float] = None
    image: Optional[str] = None
    related: Optional[str] = None
    price_case: Optional[float] = None
    price_each: Optional[float] = None
    price_per_lb: Optional[float] = None
    sku: Optional[str] = None
    wholesale: Optional[str] = None
    out_of_stock: Optional[bool] = None
    product_url: Optional[str] = None
    priceorder: Optional[int] = None
    popularityorder: Optional[int] = None

    class Config:
        from_attributes = True

class ModelType(str, Enum):
    gpt4o = 'gpt-4o'
    gpt4o_mini = 'gpt-4o-mini'
    embedding = 'text-embedding-ada-002'

@lru_cache()
def get_settings():

    return Settings(
        DB_HOST="mysql-1995017-jamesm1995017-4753.g.aivencloud.com",
        DB_USER=os.getenv("DB_USER"),
        DB_PASSWORD=os.getenv("DB_PASSWORD"),
        DB_NAME="defaultdb",
        DB_PORT=os.getenv("DB_PORT"),
        PINECONE_INDEX="cheese-index"
    )

settings = get_settings()