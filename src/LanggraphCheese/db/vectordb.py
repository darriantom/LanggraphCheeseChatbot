from langchain_openai import OpenAIEmbeddings
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import os
from dotenv import load_dotenv
from src.LanggraphCheese.db.cheese_config import settings, ModelType, CheeseData
from typing import List

load_dotenv()

class VectorDBService:
    def __init__(self):
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.dims = 1536
        self.spec = ServerlessSpec(cloud="aws", region="us-east-1")
        self.index = self._initialize_index()
        self.embed_model = OpenAIEmbeddings(
            model=ModelType.embedding,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

    def _initialize_index(self):
        existing_indexes = self.pc.list_indexes()
        
        if settings.PINECONE_INDEX not in [item["name"] for item in existing_indexes]:
            self.pc.create_index(
                name=settings.PINECONE_INDEX,
                dimension=self.dims,
                metric='cosine',
                spec=self.spec
            )
        return self.pc.Index(settings.PINECONE_INDEX)

    def _generate_vector_text(self, cheese) -> str:
        fields = [
            (cheese['name'], "name"),
            (cheese['brand'], "brand"),
            (cheese['department'], "category")
        ]
        return "\n".join([f"{label}: {value}" for value, label in fields if value])

    def query(self, query_text: str, top_k: int = 5) -> List[CheeseData]:
        vector = self.embed_model.embed_documents([query_text])[0]
        results = self.index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True
        )
        return [CheeseData(**match['metadata']) for match in results['matches']]

vector_db = VectorDBService()