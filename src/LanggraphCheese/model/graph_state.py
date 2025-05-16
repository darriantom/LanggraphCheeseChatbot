from typing import List, Dict, Optional
from enum import Enum
from pydantic import BaseModel
from typing import Annotated
import operator

class DatabaseEnum(str, Enum):
    MYSQL = "mysql"
    VECTORDB = "vectordb"
    NoDB = "nodb"

class GraphState(BaseModel):
    history: List[Dict[str, str]]
    messages: Optional[str] = None
    database: Optional[DatabaseEnum] = DatabaseEnum.VECTORDB
    query: Optional[str] = None
    sql_query: Optional[str] = None
    raw_data: Optional[List[Dict]] = None
    visualization: Optional[Dict] = None
    # Rename the HITL fields to avoid conflicts
    requires_human_review: bool = False
    hitl_feedback_message: Optional[str] = None
    feedback: str = ''