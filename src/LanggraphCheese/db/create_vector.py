import os
import json
import uuid
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

class CreateVectorDB:
    def __init__(self):
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.dims = 1536
        self.spec = ServerlessSpec(cloud="aws", region="us-east-1")
        self.index = self._initialize_index()
        self.embed_model = OpenAIEmbeddings(
            model="text-embedding-ada-002",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

    def _initialize_index(self):
        existing_indexes = self.pc.list_indexes()
        
        if "cheese-index" not in [item["name"] for item in existing_indexes]:
            self.pc.create_index(
                name="cheese-index",
                dimension=self.dims,
                metric='cosine',
                spec=self.spec
            )
        return self.pc.Index("cheese-index")

    def _generate_vector_text(self, cheese) -> str:
        fields = [
            (cheese['name'], "name"),
            (cheese['brand'], "brand"),
            (cheese['department'], "category")
        ]
        return "\n".join([f"{label}: {value}" for value, label in fields if value])

    def upsert_cheese(self, cheese):
        embedding_id = str(uuid.uuid4())
        # metadata = cheese.model_dump()
        metadata = {}
        metadata['showimage'] = cheese['showImage']
        metadata['name'] = cheese['name']
        metadata['brand'] = cheese['brand']
        metadata['category'] = cheese['department']
        metadata['image'] = cheese['images']
        metadata['itemcount_each'] = cheese['itemCounts']['EACH'] 
        metadata['dimension_each'] = cheese['dimensions']['EACH']
        metadata['weight_each'] = cheese['weights']['EACH']
        metadata['price_each'] = cheese['prices'].get('Each', "")
        if(cheese['itemCounts'].get('CASE', "")!=""):
            metadata['itemcount_case'] = cheese['itemCounts'].get('CASE', "")
        if(cheese['dimensions'].get('CASE', "")!=""):
            metadata['dimension_case'] = cheese['dimensions'].get('CASE', "")
        if(cheese['weights'].get('CASE', "")!=""):
            metadata['weight_case'] = cheese['weights'].get('CASE', "")
        if(cheese['prices'].get('Case', "")!=""):
            metadata['price_case'] = cheese['prices'].get('Case', "")
        metadata['related'] = cheese['relateds']
        metadata['sku'] = cheese['sku']
        metadata['price_per_lb'] = cheese['pricePer']
        metadata['product_url'] = cheese['href']
        metadata['wholesale'] = cheese['discount']
        metadata['out_of_stock'] = cheese['empty']
        metadata['priceorder'] = cheese['priceOrder']
        metadata['popularityorder'] = cheese['popularityOrder']
        vector = [{
            'id': embedding_id,
            'values': self.embed_model.embed_documents(self._generate_vector_text(cheese))[0],
            'metadata': metadata,
        }]
        self.index.upsert(vectors=vector, namespace='cheese')
        return embedding_id

vector_db = CreateVectorDB()

with open('cheese_product.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
        
        # Process each product in the JSON
for cheese in data:
    print(cheese['sku'])
    # mongodb.insert_cheese(cheese)
    vector_db.upsert_cheese(cheese)