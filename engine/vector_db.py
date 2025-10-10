"""
Vector Database Manager for BDM Copilot

Handles embeddings generation and vector storage using ChromaDB.
"""

import os
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional
import json

try:
    import chromadb
    from chromadb.config import Settings
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False

import streamlit as st


class VectorDatabase:
    """Manages vector embeddings and similarity search."""
    
    def __init__(self, db_path: str = "data/vectordb", model_name: str = "all-MiniLM-L6-v2"):
        self.db_path = Path(db_path)
        self.model_name = model_name
        self.client = None
        self.collection = None
        self.embeddings_model = None
        
        if not EMBEDDINGS_AVAILABLE:
            st.warning("⚠️ Vector embeddings not available. Install required packages for semantic search.")
            return
        
        self._initialize_database()
        self._load_embeddings_model()
    
    def _initialize_database(self):
        """Initialize ChromaDB client and collection."""
        try:
            # Create database directory if it doesn't exist
            self.db_path.mkdir(parents=True, exist_ok=True)
            
            # Initialize ChromaDB client
            self.client = chromadb.PersistentClient(
                path=str(self.db_path),
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name="dell_documents",
                metadata={"description": "Dell product documentation chunks"}
            )
            
        except Exception as e:
            st.error(f"Failed to initialize vector database: {str(e)}")
            self.client = None
            self.collection = None
    
    def _load_embeddings_model(self):
        """Load the sentence transformer model."""
        try:
            with st.spinner("Loading embeddings model..."):
                self.embeddings_model = SentenceTransformer(self.model_name)
        except Exception as e:
            st.error(f"Failed to load embeddings model: {str(e)}")
            self.embeddings_model = None
    
    def is_available(self) -> bool:
        """Check if vector database is properly initialized."""
        return (EMBEDDINGS_AVAILABLE and 
                self.client is not None and 
                self.collection is not None and 
                self.embeddings_model is not None)
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts."""
        if not self.embeddings_model:
            return []
        
        try:
            embeddings = self.embeddings_model.encode(texts, convert_to_numpy=True)
            return embeddings.tolist()
        except Exception as e:
            st.error(f"Failed to generate embeddings: {str(e)}")
            return []
    
    def add_documents(self, processed_docs: Dict[str, Any]) -> bool:
        """Add processed documents to the vector database."""
        if not self.is_available():
            st.warning("Vector database not available. Skipping embedding generation.")
            return False
        
        try:
            # Prepare data for vector storage
            documents = []
            metadatas = []
            ids = []
            
            chunk_counter = 0
            for doc_name, doc_data in processed_docs.items():
                for chunk in doc_data["chunks"]:
                    # Create unique ID for the chunk
                    chunk_id = f"{doc_name}_{chunk['chunk_id']}_{chunk_counter}"
                    
                    documents.append(chunk["text"])
                    metadatas.append({
                        "source_file": doc_name,
                        "source_title": chunk["source_title"],
                        "chunk_id": chunk["chunk_id"],
                        "page_range": f"Pages {chunk.get('start_page', 'unknown')}-{chunk.get('end_page', 'unknown')}",
                        "char_count": chunk["char_count"],
                        "start_char": chunk["start_char"],
                        "end_char": chunk["end_char"]
                    })
                    ids.append(chunk_id)
                    chunk_counter += 1
            
            if not documents:
                st.warning("No documents to add to vector database.")
                return False
            
            # Generate embeddings
            with st.spinner(f"Generating embeddings for {len(documents)} chunks..."):
                embeddings = self.generate_embeddings(documents)
            
            if not embeddings:
                st.error("Failed to generate embeddings.")
                return False
            
            # Add to ChromaDB
            with st.spinner("Storing in vector database..."):
                self.collection.add(
                    embeddings=embeddings,
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
            
            st.success(f"✅ Added {len(documents)} chunks to vector database!")
            return True
            
        except Exception as e:
            st.error(f"Failed to add documents to vector database: {str(e)}")
            return False
    
    def semantic_search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Perform semantic search using vector embeddings."""
        if not self.is_available():
            return []
        
        try:
            # Generate embedding for the query
            query_embedding = self.generate_embeddings([query])
            if not query_embedding:
                return []
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=max_results,
                include=["documents", "metadatas", "distances"]
            )
            
            # Format results
            search_results = []
            for i in range(len(results["documents"][0])):
                search_results.append({
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "similarity_score": 1 - results["distances"][0][i],  # Convert distance to similarity
                    "source_file": results["metadatas"][0][i]["source_file"],
                    "source_title": results["metadatas"][0][i]["source_title"]
                })
            
            return search_results
            
        except Exception as e:
            st.error(f"Semantic search failed: {str(e)}")
            return []
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector database."""
        if not self.is_available():
            return {"error": "Vector database not available"}
        
        try:
            count = self.collection.count()
            return {
                "total_chunks": count,
                "model_name": self.model_name,
                "database_path": str(self.db_path),
                "collection_name": self.collection.name
            }
        except Exception as e:
            return {"error": f"Failed to get stats: {str(e)}"}
    
    def clear_database(self) -> bool:
        """Clear all data from the vector database."""
        if not self.is_available():
            return False
        
        try:
            # Delete and recreate the collection
            self.client.delete_collection("dell_documents")
            self.collection = self.client.create_collection(
                name="dell_documents",
                metadata={"description": "Dell product documentation chunks"}
            )
            st.success("✅ Vector database cleared!")
            return True
        except Exception as e:
            st.error(f"Failed to clear database: {str(e)}")
            return False