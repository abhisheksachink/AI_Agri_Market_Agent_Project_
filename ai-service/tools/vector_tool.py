"""
Vector Tool - RAG (Retrieval-Augmented Generation) using FAISS.
"""

from langchain_core.tools import Tool
from typing import Dict, List, Optional, Any
import json
import numpy as np
from datetime import datetime

try:
    import faiss
    from sentence_transformers import SentenceTransformer
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False


class VectorTool:
    """
    Vector database tool for semantic search and RAG.
    """
    
    def __init__(self):
        self.faiss_available = FAISS_AVAILABLE
        if FAISS_AVAILABLE:
            self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            self.index = None
            self.documents = []
            self._init_index()
    
    def _init_index(self):
        """Initialize FAISS index."""
        if not self.faiss_available:
            return
        
        # Create sample agricultural context
        sample_docs = [
            "Tomato prices in Bihar are currently at Rs. 2800 per quintal",
            "Onion demand is high during monsoon season",
            "Wheat prices are stable in northern regions",
            "Rice production increases after harvesting season",
            "Mandi prices vary significantly by location and season",
            "Farmer should sell when prices are at peak",
            "Storage conditions affect crop quality and prices",
            "Government mandis provide better price discovery",
        ]
        
        self.documents = sample_docs
        embeddings = self.model.encode(sample_docs)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings, dtype=np.float32))
    
    async def semantic_search(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Search for semantically similar documents.
        """
        
        if not self.faiss_available or not self.index:
            return []
        
        # Encode query
        query_embedding = self.model.encode([query])[0]
        
        # Search
        distances, indices = self.index.search(
            np.array([query_embedding], dtype=np.float32),
            top_k
        )
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.documents):
                results.append({
                    "document": self.documents[idx],
                    "similarity": float(1 / (1 + distances[0][i])),  # Convert distance to similarity
                    "rank": i + 1
                })
        
        return results
    
    async def retrieve_historical_context(self, crop: str, state: str) -> Dict:
        """
        Retrieve historical context for a crop in a region.
        """
        
        query = f"{crop} prices trends {state}"
        results = await self.semantic_search(query)
        
        return {
            "crop": crop,
            "state": state,
            "query": query,
            "context": results,
            "timestamp": datetime.now().isoformat()
        }
    
    async def add_to_vectordb(self, documents: List[str]) -> Dict:
        """
        Add new documents to the vector database.
        """
        
        if not self.faiss_available:
            return {"error": "FAISS not available"}
        
        self.documents.extend(documents)
        embeddings = self.model.encode(documents)
        self.index.add(np.array(embeddings, dtype=np.float32))
        
        return {
            "status": "success",
            "documents_added": len(documents),
            "total_documents": len(self.documents)
        }


def create_vector_tool() -> Tool:
    """Create a LangChain Tool for vector operations."""
    
    vector_tool_impl = VectorTool()
    
    async def vector_tool_fn(
        action: str,
        query: Optional[str] = None,
        crop: Optional[str] = None,
        state: Optional[str] = None
    ) -> str:
        """
        Vector/RAG tool.
        
        Args:
            action: 'search', 'retrieve_context'
            query: Search query
            crop: Crop name
            state: State name
        """
        
        if action == "search" and query:
            results = await vector_tool_impl.semantic_search(query)
            result = {"results": results}
        
        elif action == "retrieve_context" and crop and state:
            result = await vector_tool_impl.retrieve_historical_context(crop, state)
        
        else:
            result = {"error": "Invalid parameters"}
        
        return json.dumps(result, indent=2, default=str)
    
    return Tool(
        name="vector_search",
        func=lambda action, query=None, crop=None, state=None:
            vector_tool_fn(action, query, crop, state),
        description="Semantic search and RAG. Actions: search, retrieve_context"
    )


if __name__ == "__main__":
    import asyncio
    
    async def test():
        vector_tool = VectorTool()
        results = await vector_tool.semantic_search("tomato prices Bihar")
        print(json.dumps(results, indent=2))
    
    asyncio.run(test())
